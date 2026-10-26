"""Architecture tests: the layers and the effects of decision 0001.

The rules come from ``records/decisions/0001-package-layout.md``: a
module imports only from its own layer or a lower one, imports form no
cycle (DSGN.7), and input and output, processes, the environment, and
other effects happen only in the modules the decision names (DSGN.16).
The reference is the decision record; the tests read the source with
``ast`` and execute none of it.

Effects are found in two ways. The direct scan looks at what a module's
own source does, with import aliases resolved (``import os as o`` is
still ``os``). The transitive scan follows calls by name to functions
of the package, so that a check that hashes files through
``core.corpus.corpus_hash`` reads files as surely as one that calls
``read_bytes``. Calls through values, such as the ``run`` function of
a registered check, are not followed; that is the scan's known limit.

The effect names are a denylist, which misses an effect it does not
name. The modules of ``checks``, which perform no effect, are also held
to an allowlist: each import, builtin name, and attribute name they use
is listed, or is a name the package defines (QA.8 part C, M3).
"""

from __future__ import annotations

import ast
import builtins
import unittest
from collections.abc import Iterator
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "govharness"
LAYERS = {
    "core": 0,
    "ledger": 1,
    "checks": 2,
    "derive": 2,
    "query": 2,
    "workflows": 3,
    "cli": 4,
    "__main__": 4,
}
CLI = "govharness.cli."
WORKFLOWS = "govharness.workflows."
MAIN = "govharness.__main__"
CORPUS = "govharness.core.corpus"
CHAIN = "govharness.ledger.chain"
GPG = "govharness.ledger.gpg"
REGISTER = "govharness.ledger.register"
SIGNATURES = "govharness.ledger.signatures"
LEDGER_CHECK = "govharness.checks.ledger"
REHEARSE = "govharness.workflows.rehearse"
SOLVE_STORE = "govharness.workflows.solve_store"
# Each effect, the calls or names that perform it, and where it may
# happen. A prefix ending in "." admits every module of a package.
READ_CALLS = {
    "read_text",
    "read_bytes",
    "iterdir",
    "glob",
    "rglob",
    "stat",
    "exists",
    "is_dir",
    "is_file",
    "resolve",
}
WRITE_CALLS = {
    "write_text",
    "write_bytes",
    "mkdir",
    "touch",
    "unlink",
    "rmdir",
    "rename",
    "symlink_to",
    "chmod",
    "open",
}
EXECUTE_CALLS = {"exec", "eval", "compile", "__import__", "import_module"}
EXECUTE_METHODS = {"exec_module", "import_module"}
MODULE_EFFECTS = {
    "subprocess": "process",
    "tempfile": "temporary",
    "shutil": "copy",
    "random": "random",
    "secrets": "random",
    "socket": "network",
    "urllib": "network",
    "http": "network",
    "ctypes": "interpreter",
}
EFFECTS: dict[str, tuple[str, ...]] = {
    # Corpus files are read in core/corpus.py; the ledger file in
    # ledger/chain.py; the signer configuration in ledger/gpg.py; input
    # files named on the command line in the cli; the entries of the
    # solve cache, and the solver source that versions them, in
    # workflows/solve_store.py (unit 0011).
    "read": (CORPUS, CHAIN, GPG, CLI, SOLVE_STORE),
    # Ledger appends, gpg's throwaway keyring, workflows under the root
    # passed to them, and the files the cli writes.
    "write": (CHAIN, GPG, WORKFLOWS, CLI),
    "process": (GPG,),
    # The solve cache reads the variables that name or disable it.
    "environment": (GPG, SOLVE_STORE),
    "temporary": (GPG, WORKFLOWS),
    "copy": (WORKFLOWS,),
    "print": (CLI, MAIN),
    # A ledger append records the time of the call by default.
    "clock": (CLI,),
    # A rehearsal runs the amendment script it is given.
    "execute": (REHEARSE,),
    # No module changes the interpreter's state, such as its recursion
    # limit (review 0001 made the built-in solver iterative), draws
    # random numbers, or opens a network connection.
    "interpreter": (),
    "random": (),
    "network": (),
}
# ledger/gpg.py encapsulates gpg: a caller of its functions signs or
# verifies ("gpg"), or reads the owner's signer configuration
# ("config"); the keyring, process, and environment stay inside it.
CONFIG_FUNCTIONS = {"read_config", "unalterable"}
# workflows/solve_store.py encapsulates the solve cache in the same way:
# a caller of its functions uses the cache ("cache"); the files and the
# environment variables stay inside it (unit 0011).
# Where each effect may happen, directly or through a call. The callers
# of gpg are the register (key checks), the signature check, signed
# appends, the ledger check of verify, and the layers above.
CALLERS = (WORKFLOWS, CLI, MAIN)
TRANSITIVE: dict[str, tuple[str, ...]] = {
    **{kind: (*places, MAIN) for kind, places in EFFECTS.items()},
    "read": (*EFFECTS["read"], *CALLERS),
    "write": (*EFFECTS["write"], *CALLERS),
    "temporary": (*EFFECTS["temporary"], *CALLERS),
    "copy": (*EFFECTS["copy"], *CALLERS),
    "execute": (*EFFECTS["execute"], CLI, MAIN),
    "gpg": (REGISTER, SIGNATURES, CHAIN, LEDGER_CHECK, *CALLERS),
    "config": (GPG, *CALLERS),
    "cache": (SOLVE_STORE, *CALLERS),
}


def module_name(path: Path) -> str:
    """Return the dotted name of a package source file.

    Parameters
    ----------
    path : Path
        A ``.py`` file under the package.

    Returns
    -------
    str
        Its module name; a package's ``__init__`` is the package.
    """
    rel = path.relative_to(PACKAGE.parent).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def modules() -> dict[str, ast.Module]:
    """Return the parsed source of every package module.

    Returns
    -------
    dict[str, ast.Module]
        Syntax tree by module name.
    """
    return {
        module_name(p): ast.parse(p.read_text(encoding="utf-8"))
        for p in sorted(PACKAGE.rglob("*.py"))
    }


def layer_of(name: str) -> int | None:
    """Return the layer of a module, or None for the root package.

    Parameters
    ----------
    name : str
        Module name.

    Returns
    -------
    int | None
        Layer number.
    """
    parts = name.split(".")
    return LAYERS[parts[1]] if len(parts) > 1 else None


def imported(tree: ast.Module, known: set[str]) -> Iterator[str]:
    """Yield the package modules a module imports.

    Parameters
    ----------
    tree : ast.Module
        Syntax tree of the importing module.
    known : set[str]
        Names of every package module.

    Yields
    ------
    str
        Each imported package module; ``from P import m`` yields
        ``P.m`` when that is a module, else ``P``.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("govharness"):
                    yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            if not node.module.startswith("govharness"):
                continue
            for alias in node.names:
                full = f"{node.module}.{alias.name}"
                yield full if full in known else node.module


def module_aliases(tree: ast.Module) -> dict[str, str]:
    """Return what each name bound by an import stands for.

    Parameters
    ----------
    tree : ast.Module
        Syntax tree of a module.

    Returns
    -------
    dict[str, str]
        Dotted name by local name: ``import os as o`` gives ``o: os``,
        and ``from subprocess import run`` gives ``run: subprocess.run``.
    """
    found: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                found[local] = alias.name if alias.asname else local
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                local = alias.asname or alias.name
                found[local] = f"{node.module}.{alias.name}"
    return found


def effects(node: ast.AST, aliases: dict[str, str] | None = None) -> set[str]:
    """Return the kinds of effect a piece of source performs itself.

    Parameters
    ----------
    node : ast.AST
        Syntax tree of a module or of one of its definitions.
    aliases : dict[str, str] | None
        Dotted names by local name; ``None`` takes them from ``node``.

    Returns
    -------
    set[str]
        Keys of ``EFFECTS``.
    """
    if aliases is None:
        aliases = module_aliases(node) if isinstance(node, ast.Module) else {}
    found: set[str] = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Import | ast.ImportFrom):
            names = (
                [a.name for a in sub.names]
                if isinstance(sub, ast.Import)
                else [sub.module or ""]
            )
            roots = {n.split(".")[0] for n in names}
            found |= {MODULE_EFFECTS[r] for r in roots if r in MODULE_EFFECTS}
            if isinstance(sub, ast.ImportFrom) and sub.module == "os":
                found.add("environment")
        if isinstance(sub, ast.Name):
            dotted = aliases.get(sub.id, "")
            root = dotted.split(".")[0]
            if root in MODULE_EFFECTS:
                found.add(MODULE_EFFECTS[root])
            if root == "os" and dotted != "os":
                found.add("environment")
        if isinstance(sub, ast.Attribute):
            owner = ""
            if isinstance(sub.value, ast.Name):
                owner = aliases.get(sub.value.id, sub.value.id)
            if owner == "os":
                found.add("write" if sub.attr == "fsync" else "environment")
            if sub.attr in {"now", "today", "utcnow"} or owner == "time":
                found.add("clock")
            if owner == "sys" and sub.attr in {"stdout", "stderr", "exit"}:
                found.add("print")
            if owner == "sys" and sub.attr.startswith("set"):
                found.add("interpreter")
        if isinstance(sub, ast.Call):
            func = sub.func
            # A path method by its name; calls of package functions are
            # followed by the transitive scan.
            method = func.attr if isinstance(func, ast.Attribute) else ""
            builtin = func.id if isinstance(func, ast.Name) else ""
            if method in READ_CALLS or builtin == "open":
                found.add("read")
            if method in WRITE_CALLS or builtin == "open":
                found.add("write")
            if builtin in {"print", "input"}:
                found.add("print")
            if builtin in EXECUTE_CALLS or method in EXECUTE_METHODS:
                found.add("execute")
    return found


# The checks compute on values they are given and perform no effect
# (decision 0001), so their own source is held to an allowlist rather
# than to the effect names above (QA.8 part C, M3): every import, every
# builtin name, and every attribute name outside those the package
# defines must be listed here. A name is listed only when using it
# reads, writes, runs, and opens nothing.
CHECKS_PACKAGE = "govharness.checks"
CHECK_IMPORTS = {
    "__future__.annotations",
    "collections.Counter",
    "collections.abc.Callable",
    "dataclasses.dataclass",
    "dataclasses.field",
    "hashlib",
    "itertools",
    "json",
    "pathlib.PurePosixPath",
    "re",
    "types.ModuleType",
    "typing.Any",
    "typing.TypeVar",
}
# The optional solver is found and imported by satlib alone.
CHECK_IMPORTS_IN = {
    "importlib.util": "govharness.checks.logic.satlib",
    "z3": "govharness.checks.logic.satlib",
}
CHECK_BUILTINS = {
    *("RecursionError", "UnicodeDecodeError", "ValueError"),
    *("all", "any", "bool", "bytes", "chr", "dict", "enumerate"),
    *("frozenset", "int", "isinstance", "len", "list", "max", "min"),
    *("next", "object", "range", "repr", "set", "sorted", "str", "sum"),
    *("tuple", "type", "zip"),
}
CHECK_ATTRIBUTES = {
    # str, bytes, and format
    *("decode", "encode", "endswith", "format", "format_map", "isdigit"),
    *("isupper", "join", "lower", "lstrip", "partition", "removeprefix"),
    *("removesuffix", "replace", "rsplit", "split", "splitlines"),
    *("startswith", "strip"),
    # list, dict, and set
    *("__getitem__", "add", "append", "copy", "count", "extend", "get"),
    *("index", "items", "pop", "setdefault", "update", "values"),
    # re and its matches
    *("DOTALL", "I", "IGNORECASE", "M", "MULTILINE", "Pattern"),
    *("compile", "end", "escape", "findall", "finditer", "fullmatch"),
    *("group", "match", "search", "span", "start", "sub"),
    # pathlib.PurePosixPath, which touches no file
    *("as_posix", "name", "parent", "parents", "parts"),
    # hashlib, json, and itertools
    *("hexdigest", "sha256", "loads", "combinations", "permutations"),
    # importlib.util.find_spec, and the z3 API (satlib only)
    *("util", "find_spec", "Bool", "Not", "Or", "Solver"),
    *("assert_and_track", "check", "eval", "get_version_string"),
    *("is_true", "model", "sat", "set", "unsat_core"),
}
# Names whose use performs an effect, never admitted through the names
# the package defines.
EFFECT_NAMES = READ_CALLS | WRITE_CALLS | EXECUTE_CALLS | EXECUTE_METHODS


def defined_names(parsed: dict[str, ast.Module]) -> set[str]:
    """Return the names the package defines, which attributes may use.

    Parameters
    ----------
    parsed : dict[str, ast.Module]
        Syntax tree by module name.

    Returns
    -------
    set[str]
        Names of functions, classes, methods, fields, module-level
        assignments, and attributes assigned on ``self``, less the
        names of effects.
    """
    found: set[str] = set()
    for tree in parsed.values():
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.ClassDef):
                found.add(node.name)
            targets: list[ast.expr] = []
            if isinstance(node, ast.Assign):
                targets = list(node.targets)
            elif isinstance(node, ast.AnnAssign):
                targets = [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    found.add(target.id)
                elif isinstance(target, ast.Attribute):
                    found.add(target.attr)
    return found - EFFECT_NAMES


def unlisted_uses(name: str, tree: ast.Module, defined: set[str]) -> list[str]:
    """Return the imports and names of a checks module the list lacks.

    Parameters
    ----------
    name : str
        Module name.
    tree : ast.Module
        Its syntax tree.
    defined : set[str]
        Names the package defines (``defined_names``).

    Returns
    -------
    list[str]
        One line per import, builtin name, or attribute name outside
        ``CHECK_IMPORTS``, ``CHECK_IMPORTS_IN``, ``CHECK_BUILTINS``,
        ``CHECK_ATTRIBUTES``, and ``defined``.
    """
    builtin = set(dir(builtins))
    found: list[str] = []

    def admitted(dotted: str) -> bool:
        """Return True when an import is listed for this module.

        Parameters
        ----------
        dotted : str
            The module, or ``module.name`` for a ``from`` import.

        Returns
        -------
        bool
            Whether the import is admitted.
        """
        return (
            dotted.startswith("govharness")
            or dotted in CHECK_IMPORTS
            or CHECK_IMPORTS_IN.get(dotted) == name
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [
                f"line {node.lineno}: import {a.name}"
                for a in node.names
                if not admitted(a.name)
            ]
        elif isinstance(node, ast.ImportFrom):
            found += [
                f"line {node.lineno}: from {node.module} import {a.name}"
                for a in node.names
                if not admitted(f"{node.module}.{a.name}")
            ]
        elif isinstance(node, ast.Name) and node.id in builtin:
            if node.id not in CHECK_BUILTINS:
                found.append(f"line {node.lineno}: builtin {node.id}")
        elif (
            isinstance(node, ast.Attribute)
            and node.attr not in CHECK_ATTRIBUTES | defined
        ):
            found.append(f"line {node.lineno}: attribute .{node.attr}")
    return found


def allowed(name: str, effect: str, table: dict | None = None) -> bool:
    """Return True when the decision lets a module perform an effect.

    Parameters
    ----------
    name : str
        Module name.
    effect : str
        Kind of effect.
    table : dict | None
        Places by effect; ``None`` is ``EFFECTS``, the direct rule.

    Returns
    -------
    bool
        Whether the module is, or lies in, a place the effect is
        confined to.
    """
    places = (EFFECTS if table is None else table).get(effect, ())
    return any(
        name.startswith(place) if place.endswith(".") else name == place
        for place in places
    )


def bindings(name: str, tree: ast.Module, known: set[str]) -> dict[str, str]:
    """Return what each name a module imports from the package names.

    Parameters
    ----------
    name : str
        Module name.
    tree : ast.Module
        Its syntax tree.
    known : set[str]
        Names of every package module.

    Returns
    -------
    dict[str, str]
        By local name: ``module:function`` for an imported function,
        or ``module`` for an imported module.
    """
    found: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in known | {
            "govharness"
        }:
            for alias in node.names:
                full = f"{node.module}.{alias.name}"
                target = (
                    full if full in known else f"{node.module}:{alias.name}"
                )
                found[alias.asname or alias.name] = target
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in known and alias.asname:
                    found[alias.asname] = alias.name
    return found


def call_graph(
    parsed: dict[str, ast.Module],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return the direct effects and the package calls of each function.

    A function is ``module:name`` for each top-level function or class
    (whose methods count as its body), and ``module:`` for the code of
    the module outside them.

    Parameters
    ----------
    parsed : dict[str, ast.Module]
        Syntax tree by module name.

    Returns
    -------
    tuple[dict[str, set[str]], dict[str, set[str]]]
        Direct effects by function, and called functions by function.
    """
    direct: dict[str, set[str]] = {}
    calls: dict[str, set[str]] = {}
    known = set(parsed)
    for name, tree in parsed.items():
        aliases = module_aliases(tree)
        bound = bindings(name, tree, known)
        defined = {
            n.name: n
            for n in tree.body
            if isinstance(n, ast.FunctionDef | ast.ClassDef)
        }
        rest = (
            [n for n in tree.body if n.name not in defined]
            if False
            else [
                n
                for n in tree.body
                if not isinstance(n, ast.FunctionDef | ast.ClassDef)
            ]
        )
        units = {
            **{f"{name}:{k}": v for k, v in defined.items()},
            f"{name}:": ast.Module(body=rest, type_ignores=[]),
        }
        for key, unit in units.items():
            direct[key] = effects(unit, aliases)
            calls[key] = set()
            for sub in ast.walk(unit):
                if not isinstance(sub, ast.Call):
                    continue
                func = sub.func
                if isinstance(func, ast.Name):
                    if func.id in defined:
                        calls[key].add(f"{name}:{func.id}")
                    elif ":" in bound.get(func.id, ""):
                        calls[key].add(bound[func.id])
                elif isinstance(func, ast.Attribute) and isinstance(
                    func.value, ast.Name
                ):
                    module = bound.get(func.value.id, "")
                    if module in known:
                        calls[key].add(f"{module}:{func.attr}")
    return direct, calls


def seen_from(caller: str, callee: str, found: set[str]) -> set[str]:
    """Return the effects of a callee as its caller performs them.

    Parameters
    ----------
    caller : str
        Module of the calling function.
    callee : str
        The called function, ``module:name``.
    found : set[str]
        Effects of the callee.

    Returns
    -------
    set[str]
        ``found``, except that a function of ``ledger/gpg.py`` called
        from another module is ``config`` or ``gpg``, and one of
        ``workflows/solve_store.py`` is ``cache``.
    """
    module, _, function = callee.partition(":")
    if module == caller or not found:
        return found
    if module == SOLVE_STORE:
        return {"cache"}
    if module != GPG:
        return found
    return {"config"} if function in CONFIG_FUNCTIONS else {"gpg"}


def transitive_effects(parsed: dict[str, ast.Module]) -> dict[str, set[str]]:
    """Return the effects of each module, its calls into the package
    included.

    Parameters
    ----------
    parsed : dict[str, ast.Module]
        Syntax tree by module name.

    Returns
    -------
    dict[str, set[str]]
        Effects by module name.
    """
    direct, calls = call_graph(parsed)
    total = {key: set(found) for key, found in direct.items()}
    changed = True
    while changed:
        changed = False
        for key, callees in calls.items():
            caller = key.partition(":")[0]
            for callee in callees:
                more = seen_from(caller, callee, total.get(callee, set()))
                if not more <= total[key]:
                    total[key] |= more
                    changed = True
    by_module: dict[str, set[str]] = {name: set() for name in parsed}
    for key, found in total.items():
        by_module[key.partition(":")[0]] |= found
    return by_module


def relative_imports(tree: ast.Module) -> list[int]:
    """Return the lines of a module's relative imports.

    Parameters
    ----------
    tree : ast.Module
        Syntax tree of a module.

    Returns
    -------
    list[int]
        Line numbers; the layer test reads only absolute imports.
    """
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.level
    ]


def import_graph() -> dict[str, set[str]]:
    """Return the imports between package modules.

    Returns
    -------
    dict[str, set[str]]
        Imported modules by importing module.
    """
    parsed = modules()
    known = set(parsed)
    return {name: set(imported(t, known)) for name, t in parsed.items()}


def find_cycle(graph: dict[str, set[str]]) -> list[str]:
    """Return one import cycle, or an empty list.

    Parameters
    ----------
    graph : dict[str, set[str]]
        Imported modules by importing module.

    Returns
    -------
    list[str]
        Modules of a cycle, the first repeated at the end.
    """
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str]:
        """Depth-first search that reports a back edge as a cycle.

        Parameters
        ----------
        node : str
            Module to search from.

        Returns
        -------
        list[str]
            A cycle through the node, or an empty list.
        """
        state[node] = 1
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            if state.get(nxt) == 1:
                return [*stack[stack.index(nxt) :], nxt]
            if nxt not in state and (cycle := visit(nxt)):
                return cycle
        stack.pop()
        state[node] = 2
        return []

    for node in sorted(graph):
        if node not in state and (cycle := visit(node)):
            return cycle
    return []


class Architecture(unittest.TestCase):
    """The package keeps the structure decision 0001 records."""

    def test_every_module_has_a_layer(self) -> None:
        """Behavior: every module lies in one of the decided packages.

        Reference: the layer table of decision 0001.
        """
        for name in modules():
            if name != "govharness":
                with self.subTest(name):
                    self.assertIn(name.split(".")[1], LAYERS)

    def test_no_import_from_a_higher_layer(self) -> None:
        """Behavior: a module imports only from its layer or below.

        Reference: decision 0001 and DSGN.7.
        """
        for name, targets in import_graph().items():
            for target in targets:
                with self.subTest(f"{name} -> {target}"):
                    own, other = layer_of(name), layer_of(target)
                    if own is not None and other is not None:
                        self.assertLessEqual(other, own)

    def test_no_import_cycle(self) -> None:
        """Behavior: the imports between modules form no cycle.

        Reference: decision 0001 and DSGN.7.
        """
        self.assertEqual(find_cycle(import_graph()), [])

    def test_cycle_detection_finds_a_cycle(self) -> None:
        """Behavior: the cycle search reports a known cycle.

        Reference: a hand-made graph a -> b -> a, so that a pass of the
        test above is evidence, not an artifact of the search.
        """
        self.assertEqual(find_cycle({"a": {"b"}, "b": {"a"}}), ["a", "b", "a"])

    def test_imports_are_absolute(self) -> None:
        """Behavior: no module imports relatively, so the layer test sees
        every import between modules.

        Reference: decision 0001; ``from ..cli import x`` would pass the
        layer test unseen.
        """
        for name, tree in modules().items():
            with self.subTest(name):
                self.assertEqual(relative_imports(tree), [])

    def test_effects_are_confined(self) -> None:
        """Behavior: each module performs itself only the effects its
        place allows.

        Reference: the effects column of decision 0001 and DSGN.16.
        """
        for name, tree in modules().items():
            for effect in effects(tree):
                with self.subTest(f"{name}: {effect}"):
                    self.assertTrue(allowed(name, effect))

    def test_effects_through_calls_are_confined(self) -> None:
        """Behavior: counting the package functions a module calls, only
        ``core.corpus``, ``ledger.chain``, the workflows, and the cli
        read or write files; ``checks`` and ``derive`` read and write
        nothing, and only the ledger check runs gpg.

        Reference: the effects column of decision 0001 and DSGN.16.
        """
        for name, found in transitive_effects(modules()).items():
            for effect in found:
                with self.subTest(f"{name}: {effect}"):
                    self.assertTrue(allowed(name, effect, TRANSITIVE))

    def test_effect_scan_finds_effects(self) -> None:
        """Behavior: the scan sees a write, a process, a print, a read,
        and an aliased environment read and process.

        Reference: hand-written sources holding one of each, so that a
        pass of the test above is evidence.
        """
        source = (
            "import subprocess\n"
            "p.write_text('x')\n"
            "print('y')\n"
            "q.read_bytes()\n"
        )
        self.assertEqual(
            effects(ast.parse(source)), {"process", "write", "print", "read"}
        )
        aliased = "import os as o\nimport subprocess as s\no.environ\n"
        self.assertEqual(
            effects(ast.parse(aliased)), {"environment", "process"}
        )
        self.assertEqual(
            effects(
                ast.parse(
                    "import random\nimport importlib\n"
                    "importlib.import_module('x')\n"
                )
            ),
            {"random", "execute"},
        )

    def test_checks_use_only_listed_names(self) -> None:
        """Behavior: every module of ``checks`` imports, and uses as
        builtins and attributes, only the names the allowlist admits
        or the package defines.

        Reference: decision 0001 (``checks`` reads and writes no file)
        and DSGN.16; QA.8 part C, M3, which found effects that the
        effect names above do not list.
        """
        parsed = modules()
        defined = defined_names(parsed)
        for name, tree in parsed.items():
            if name.startswith(CHECKS_PACKAGE):
                with self.subTest(name):
                    self.assertEqual(unlisted_uses(name, tree, defined), [])

    def test_allowlist_refuses_effects(self) -> None:
        """Behavior: each use the review appended to a checks module is
        refused, those the effect scan missed and its controls alike,
        and a use of ``re`` is admitted.

        Reference: QA.8 part C, M3: one line appended to
        ``checks/manifests.py`` per case.
        """
        defined = defined_names(modules())
        module = f"{CHECKS_PACKAGE}.manifests"
        refused = {
            "smtplib": "import smtplib\n",
            "ftplib": "import ftplib\n",
            "sqlite3": "import sqlite3\nsqlite3.connect('x')\n",
            "zipfile": "from zipfile import ZipFile\nZipFile('x')\n",
            "fileinput": "import fileinput\nfileinput.input()\n",
            "multiprocessing": "import multiprocessing\n",
            "threading": "import threading\nthreading.Thread()\n",
            "logging": "import logging\nlogging.FileHandler('x')\n",
            "stdin": "import sys\nsys.stdin.read()\n",
            "sys.path": "import sys\nsys.path.append('x')\n",
            "uuid": "import uuid\nuuid.uuid4()\n",
            "bound method": "f = path.read_text\nf()\n",
            "getattr": "getattr(path, 'read_text')()\n",
            "open": "open('x')\n",
            "subprocess": "import subprocess\n",
            "listdir": "import os\nos.listdir('.')\n",
            "Path.read_text": (
                "from pathlib import Path\nPath('x').read_text()\n"
            ),
            "builtins.open": "import builtins\nbuiltins.open('x')\n",
            "importlib": "import importlib\nimportlib.import_module('x')\n",
            "eval": "eval('1')\n",
            "gzip": "import gzip\ngzip.open('x')\n",
            "z3 outside satlib": "import z3\n",
        }
        for case, source in refused.items():
            with self.subTest(case):
                self.assertTrue(
                    unlisted_uses(module, ast.parse(source), defined)
                )
        clean = "import re\nre.compile('a').search(text).group(0)\n"
        self.assertEqual(unlisted_uses(module, ast.parse(clean), defined), [])

    def test_scan_follows_calls(self) -> None:
        """Behavior: a function that calls a reading function of another
        module reads; a call into ``ledger/gpg.py`` counts as gpg use,
        and one into ``workflows/solve_store.py`` as cache use.

        Reference: hand-written modules: ``c`` hashes through ``a``,
        ``d`` verifies through ``ledger.gpg``, ``e`` opens the solve
        cache and ``g`` calls ``e``, and ``r`` imports relatively.
        """
        parsed = {
            "a": ast.parse("def h(p):\n    return p.read_bytes()\n"),
            "c": ast.parse(
                "from a import h\ndef check(p):\n    return h(p)\n"
            ),
            GPG: ast.parse(
                "import subprocess\ndef verify():\n    subprocess.run([])\n"
            ),
            "d": ast.parse(
                f"from {GPG} import verify\ndef f():\n    verify()\n"
            ),
        }
        parsed[SOLVE_STORE] = ast.parse(
            "import os\ndef open_store():\n    return os.environ\n"
        )
        parsed["e"] = ast.parse(
            f"from {SOLVE_STORE} import open_store\n"
            "def f():\n    open_store()\n"
        )
        parsed["g"] = ast.parse("from e import f\ndef h():\n    f()\n")
        found = transitive_effects(parsed)
        self.assertEqual(found["c"], {"read"})
        self.assertEqual(found["d"], {"gpg"})
        self.assertEqual(found["e"], {"cache"})
        self.assertEqual(found["g"], {"cache"})
        relative = ast.parse("from ..cli import main\n")
        self.assertEqual(relative_imports(relative), [1])


if __name__ == "__main__":
    unittest.main()

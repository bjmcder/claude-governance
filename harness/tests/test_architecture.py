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
"""

from __future__ import annotations

import ast
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
    # Programs the environment runs; they import nothing from the
    # package (test_hooks_stand_alone).
    "hooks": 4,
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
HOOKS = "govharness.hooks."
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
    # files named on the command line in the cli.
    "read": (CORPUS, CHAIN, GPG, CLI, HOOKS),
    # Ledger appends, gpg's throwaway keyring, workflows under the root
    # passed to them, and the files the cli writes.
    # A hook opens its policy file, and the scan counts open() as a
    # write.
    "write": (CHAIN, GPG, WORKFLOWS, CLI, HOOKS),
    "process": (GPG,),
    "environment": (GPG, HOOKS),
    "temporary": (GPG, WORKFLOWS),
    "copy": (WORKFLOWS,),
    "print": (CLI, MAIN, HOOKS),
    # The guard compares the expiry of an authorization with the time
    # of each call (STND.HARN.29, unit 0008).
    "clock": (CLI, HOOKS),
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
        from another module is ``config`` or ``gpg``.
    """
    module, _, function = callee.partition(":")
    if module != GPG or caller == GPG or not found:
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

    def test_hooks_stand_alone(self) -> None:
        """Behavior: a hook imports nothing from the package.

        Reference: decision 0001; a hook is installed outside the work,
        where the package is not, so an import would fail closed on
        every call.
        """
        for name, targets in import_graph().items():
            if name.startswith(HOOKS):
                with self.subTest(name):
                    self.assertEqual(targets, set())

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

    def test_scan_follows_calls(self) -> None:
        """Behavior: a function that calls a reading function of another
        module reads; a call into ``ledger/gpg.py`` counts as gpg use.

        Reference: hand-written modules: ``c`` hashes through ``a``,
        ``d`` verifies through ``ledger.gpg``, and ``r`` imports
        relatively.
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
        found = transitive_effects(parsed)
        self.assertEqual(found["c"], {"read"})
        self.assertEqual(found["d"], {"gpg"})
        relative = ast.parse("from ..cli import main\n")
        self.assertEqual(relative_imports(relative), [1])


if __name__ == "__main__":
    unittest.main()

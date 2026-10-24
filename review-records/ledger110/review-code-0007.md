# Code review: unit 0007 (secret store)

Ran: test_guard + test_environment, 62 tests OK. 

## Findings

**Defect**
1. guard.py:399-420, 1124, 1141, 1175: the store is compared lexically, never resolved. If `<work>/secrets` is itself a symlink to another directory inside the work, `Read <work>/secrets/q` has real path `<work>/real/q`, which is in the work and not under `store`, so it passes. `Grep path=<work>/secrets` also passes (`holds_secrets` tests `within(policy.store, (real,))`). Verified. DoD 2 says "symbolic links resolved as for other paths"; a store that is a link is the case it names. The agent can create the link: `ln -s other secrets` and `mv secrets x` return no finding, because `secret_file` excludes the store directory itself (the sandbox may stop it; the guard does not). Fix: compare against `real_path(policy.store)` (and real secrets) in `secret_file` and `holds_secrets`; refer writes, moves, removals and chmod of the store directory.
2. guard.py:1174 etc.: a directory operand that holds the store passes. `cp -r secrets other` returns no finding, so the closed files land in the work and are then readable. `cp -r /etc other` is refused as out of bounds, so the store is weaker than the other bounds. Also `mv secrets other/s2`. Fix: for a read or write operand that is a directory containing the store (or the store), apply the `holds_secrets` rule.
3. guard.py:442-446: `holds_secrets` lets `os.listdir` raise `NotADirectoryError` (store is a file) or `PermissionError` (mode 000). Verified. `main` turns the exception into a denial, so it fails closed, but with an opaque "Unreadable call". Fix: catch `OSError`, return True when the store cannot be listed but exists.

**Should-fix**
4. Names the guard does not read as reads or writes pass: `find secrets -exec cat {} +`, `grep -r s secrets`, `source secrets/a`, `awk 1 secrets/a`, `dd if=secrets/a`, `install`, `rsync`, `python -c open(...)`, `tar cf - secrets`. `find /etc -exec` and `tar /etc` are caught by the bounds; the store variants are not (same directory-operand cause as 2). `grep -r s /etc` and `source /etc/passwd` also pass today, so these are existing limits. The coverage text does not list them.
5. Coverage text (claude_code.py STORE_GAPS) overclaims. "The sandbox keeps shell commands from reading..." holds only when the sandbox runs, and `failIfUnavailable` is `inputs.assured`. It also omits: shell commands the guard does not parse, a store that is a link, case-insensitive file systems (`Secrets/a` passes; verified, matters on macOS), and macOS where `denyWrite` takes no wildcard (the directory entry is used, so this is fine, but the claim "denies every write" is undocumented either way, as the DoD says).
6. Tests are missing: CLI `--secret-store` alone; `--secret ""`; Grep with `glob`; Grep on a subdirectory of the store or on a hidden file; a store that is a link, a file or unreadable (findings 1, 3); `cp -r secrets x`; `~` and `..` spellings; the `denyRead` list in `test_store_without_names`.

**Optional**
7. `read_policy` takes `str(data["store"])`; `null` becomes `"None"`, a relative path that never matches, so the store is silently off. Validate that it is a string, empty or absolute.
8. test_guard.py:531 `POLICY` (RUF012, mutable class attribute). No ruff config is in the tree, so I could not verify "ruff clean"; 30 errors show on the changed files under the defaults I have, 4 files would be reformatted. Not attributable to this unit without the project's config.

Style: numpy docstrings, naming and comment density match. The guard imports only the standard library (`grep` of imports verified), so the architecture rule holds.

## Criteria

| Criterion | Status | Evidence |
|---|---|---|
| 1 options, validation, unchanged without store, empty fields | Met | Inputs.__post_init__ rejects ``, `.`, `..`, `/`; test_names_refused, test_no_store_leaves_settings, test_command_options (exit 1 and message). `--secret-store` alone only via Inputs, not the CLI. |
| 2 files outside bounds, directory inside, file tools and shell, links | Partly | Verified refusals: `..`, `//`, trailing slash, relative, `./`, link to a file, link to the directory, quotes, globs, redirection, here-document, tee, cp, mv, rm, chmod, sed -i, `< file`. Gaps: findings 1, 2, 4. Directory and opened file pass. |
| 3 Grep and Glob | Mostly met | Grep with the store or an ancestor, a relative path, a link to the directory, and `glob` all refer; passes with only opened files or no store; Glob passes. Gaps: store as link, unlistable store (finding 1, 3). |
| 4 sandbox settings | Met as designed | `denyRead` `store/*` and `store/.*`, `allowRead` per file, `denyWrite` includes the store, no permission rule added (tested). Matches the stated documentation facts; cannot check them against the documentation without network. |
| 5 coverage rows | Partly | Rows carry the text and none becomes full (tested); the text overclaims (finding 5). |
| 6 tests, lint, imports | Partly | Tests pass; each criterion has a test; mutations I reasoned through (removing `secret_file` from check_read, or the `if policy.store` guard) fail a test. Ruff and `verify` not confirmed (no config; full discovery not completed). |

## Verdict

Not ready as is. The store check is correct for the file tools and for the common shell spellings, and fails closed on exceptions, but findings 1 and 2 are real bypasses of criterion 2 that the coverage text does not admit. Fix 1 to 3 and the text of finding 5, then add the tests of finding 6.

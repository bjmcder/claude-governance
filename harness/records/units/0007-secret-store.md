# Unit 0007: the secret store in the derived environment

The working bounds of STND.DFLT admit a file of the directory of STND.DFLT.29 only to an agent that an authorization permits to handle the secret it holds, and the Notes of STND.DFLT have a harness that derives an environment under STND.HARN.18 map those bounds. Until this unit the derived configuration treats `<work>/secrets` as part of the writable work.

## Definition of done

1. `environment` takes `--secret-store`, which states that the human owner provides the store of STND.DFLT.29, and `--secret NAME`, repeatable, which names a file of that store that an authorization permits the agent to handle and implies `--secret-store`. A name that is empty, `.` or `..`, or holds a slash exits 1 with a message. Without either option the managed settings are unchanged, and the guard's policy gains the fields `store` and `secrets`, empty.
2. With a store, the guard places each file under `<work>/secrets` outside the working bounds, for reading (read-bounds) and for writing (write-bounds), other than the named files. The directory itself stays within the bounds, so that listing it and confirming its permissions under STND.DFLT.30 pass. This holds for the file tools and for every path of a shell command that the guard reads, with symbolic links resolved as for other paths.
3. With a store, a Grep call whose search directory is the store or holds it reaches read-bounds while the store holds a file not named by `--secret`, and passes otherwise (STND.DFLT.31). Glob, which returns names, and a name of the store hold no secret (STND.DFLT.29), so a Glob call passes.
4. With a store, the managed settings deny the shell reads of the store's entries (`sandbox.filesystem.denyRead`, a pattern for the entries of the directory) and allow each named file (`allowRead`, which the documentation makes win as the narrower path), and deny the shell every write in the store (`denyWrite`, the directory), because the documentation does not state that a narrower allowance reopens a path for writing. No permission rule is added, because a deny or ask rule over the store would override an allow rule for a named file.
5. With a store, the coverage report's rows for read-bounds and write-bounds state the store's gaps. No row becomes full.
6. Each criterion has a test; every earlier test passes; ruff is clean on the changed files; the convention and architecture tests pass; the guard imports nothing from the package; `verify` passes.

## Record

- Facts relied on about Claude Code, from its documentation (settings reference, sandboxing, permissions; code.claude.com/docs/en): the sandbox keys `denyRead`, `allowRead`, `denyWrite`, and `allowWrite`; read rules where the narrower path wins; wildcards in `denyRead` and `allowRead` on every platform and in `allowWrite` and `denyWrite` on macOS only; `denyRead` does not stop the Read tool; permission rules decide deny, then ask, then allow, whatever their specificity; a hook's decision does not override a permission rule.

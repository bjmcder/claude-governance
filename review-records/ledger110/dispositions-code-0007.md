# Dispositions: unit 0007 code review

Review: review-code-0007.md.

| Finding | Disposition |
| --- | --- |
| Defect 1: the store compared as spelled; a store that is a link to another directory of the work passed | Fixed: `secret_file` and `holds_secrets` compare against the real paths of the store and the opened files. Test `test_store_is_a_link`. Creating the store as a link (`ln -s other secrets`) only moves what is closed, since the closed files are then those where the link leads. |
| Defect 2: `cp -r secrets other` and `mv secrets other/s2` passed | Fixed: a copy (`check_copied`), move, or removal (`check_removal`, `check_pattern`) that takes in the store while it holds a closed file reaches read-bounds or write-bounds. `chmod` of the store still passes, since STND.DFLT.30 has the agent restore its permissions. Test `test_directory_operands`. |
| Defect 3: `os.listdir` raising `NotADirectoryError` or `PermissionError` gave an opaque denial | Fixed: a store that exists but cannot be listed counts as holding a closed file. Test `test_unlistable_store`. |
| Should-fix: programs the guard does not parse (`find -exec cat`, `grep -r`, `source`, `awk`, `tar`, `rsync`, interpreters) | Admitted in the coverage text: such a program reaches the store only through the sandbox. Several pass today for other out-of-bounds paths as well; parsing them is outside this unit. |
| Should-fix: coverage overclaims while the sandbox is unavailable; case-insensitive file systems; store as link | Coverage text revised: "While the sandbox runs ..."; the case limit is stated; the link case is fixed. |
| Should-fix: missing tests | Added: `--secret-store` alone and `--secret ""`; Grep with a glob, on a directory under the store, and with a hidden closed file; a store that is a link, a file, or unlistable; `cp -r` and `mv` of the store; `denyRead` without names. |
| Optional: `read_policy` turns a null store into "None" | Fixed: a store that is not a string is refused. |
| Optional: RUF012 at test_guard.py | Fixed: the store policy is a module constant. |

## Final verification (verify-final.md)

| Finding | Disposition |
| --- | --- |
| B1: the denial of shell writes also blocks `chmod` of the store and shell removal of an opened secret | Kept the denial, which stops programs the guard does not read from renaming or overwriting a closed secret; stated in the write-bounds gap, the unit record (criteria 4 and 5), and decision 0002. The agent refers those actions; STND.DFLT.30 already has it refer what it is unable to restore. |
| B2: `cd secrets && cat token` is referred | No change: the guard resolves a relative path against every directory the line may run in, by design (decision 0002, review 0003); it refers and does not pass. |
| B3: the coverage test checks less than the audit claims | Fixed: the test asserts "While the sandbox runs", "ignores case", and the STND.DFLT.30 referral. |
| B4: ruff status unverified | Audit line 6 now states the two findings that ruff's defaults add and why each matches the surrounding code. |

import sys, re
sys.path.insert(0, "/home/claude/harness")
from pathlib import Path
from govharness.cli.reports import _logic_context
from govharness.checks.drafting.family import all_findings
root = Path(sys.argv[1]); pat = re.compile(sys.argv[2])
ctx = _logic_context(root, False)
f = all_findings(ctx)
for key, items in f.items():
    for it in items:
        s = str(it)
        if pat.search(s):
            print(key, s[:300])

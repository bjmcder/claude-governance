"""Run the harness command line: ``python -m govharness <command>``."""

import sys

from govharness.cli.main import main

sys.exit(main(sys.argv[1:]))

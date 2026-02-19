# ariadne-codegen – run `just --list` for recipes

# Format, typecheck, and test (run before PR)
check:
    hatch fmt --check
    hatch run types:check
    hatch test -c -py 3.10

# Tests with coverage (Python 3.10)
test:
    hatch test -c -py 3.10

# Tests across all Python versions
test-all:
    hatch test -a -p

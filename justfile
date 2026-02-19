# ariadne-codegen – run `just --list` for recipes

# Format, typecheck
check:
    hatch fmt --check
    hatch run types:check

# Tests with coverage (default Python 3.10)
test py="3.10":
    hatch test -c -py {{ py }}

# Tests across all Python versions
test-all:
    hatch test -a -p

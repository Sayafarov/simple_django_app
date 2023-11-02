set -e
black ./src --check # https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#check
isort ./src --check-only # https://pycqa.github.io/isort/
pycln ./src --check # https://hadialqattan.github.io/pycln/#/?id=-c-check-flag

mypy ./src # https://mypy.readthedocs.io/en/stable/
#!/bin/sh

# Python code auto-formatter
if [ "$(command -v autopep8 2>/dev/null)" != "" ]; then
    find . -name "*.py" -type f -exec autopep8 --in-place --aggressive {} \;
fi

# Python linter
if [ "$(command -v flake8 2>/dev/null)" != "" ]; then
    find . -name "*.py" -type f -exec flake8 --ignore E501,W504,E402 {} \; || true
fi

# Python type checker
if [ "$(command -v pyre 2>/dev/null)" != "" ]; then
    cd api || exit
    pyre check 2>/dev/null | grep -vi 'Undefined import'
    pyre analyze --no-verify 2>/dev/null
    cd "$OLDPWD" || exit
fi

# Shell linter
if [ "$(command -v shellcheck 2>/dev/null)" != "" ]; then
    find . -name "*.sh" -type f -exec shellcheck {} \;
fi

# Shell formatter
if [ "$(command -v shfmt 2>/dev/null)" != "" ]; then
    find . -name "*.sh" -type f -exec shfmt -p {} \; 1>/dev/null
fi

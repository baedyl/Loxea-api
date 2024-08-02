#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --remove-unused-variables --in-place --exclude=__init__.py --recursive app
black app
isort --force-single-line-imports app

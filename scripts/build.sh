#!/usr/bin/env bash

pushd libs/astx || exit
cp ../../README.md .
poetry build
popd || return

pushd libs/astx-transpilers || exit
cp ../../README.md .
poetry build
popd || return

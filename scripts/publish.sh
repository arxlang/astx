#!/usr/bin/env bash

pushd libs/astx || exit
poetry publish
popd || return

pushd libs/astx-transpilers || exit
poetry publish
popd || return

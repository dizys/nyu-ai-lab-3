#!/usr/bin/env bash

shell_dir=$(dirname "$0")

cd "$shell_dir"

rm -f ai-lab-3_zz2960.zip

zip -r ai-lab-3_zz2960.zip solving mdp README.md

#!/bin/bash
echo "$1: $([ "$(sha256sum "$1" | cut -d' ' -f1)" = "$2" ] && echo OK || echo FAILED)"

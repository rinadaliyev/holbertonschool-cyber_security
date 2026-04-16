#!/bin/bash
grep -m 1 "Linux version" "${1:-dmesg}"

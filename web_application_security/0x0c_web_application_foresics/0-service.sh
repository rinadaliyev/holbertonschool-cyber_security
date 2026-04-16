#!/bin/bash
awk '{print $6}' "${1:-auth.log}" | sort | uniq -c | sort -rn

#!/bin/bash
grep "Failed" "${1:-auth.log}" | sed 's/invalid user //' | awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i-1)}' | sort | uniq -c | sort -rn | head -n 1 | awk '{print $2}'

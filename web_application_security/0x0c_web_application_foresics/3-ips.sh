#!/bin/bash
grep "Accepted password for root" "${1:-auth.log}" | awk '{print $11}' | sort -u | wc -l

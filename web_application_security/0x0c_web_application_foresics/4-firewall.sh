#!/bin/bash
grep "COMMAND=/sbin/iptables" "${1:-auth.log}" | grep -E " -A | -I " | wc -l

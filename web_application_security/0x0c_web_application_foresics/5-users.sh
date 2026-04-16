#!/bin/bash
grep "new user" "${1:-auth.log}" | awk -F'name=' '{print $2}' | cut -d',' -f1 | sort | paste -sd "," -

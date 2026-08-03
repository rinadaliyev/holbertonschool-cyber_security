#!/bin/bash

# Check if file arguments are provided
if [ -z "$1" ]; then
  echo "Usage: $0 <ELF file>"
  exit 1
fi

file_name="$1"

# Check if the file exists
if [ ! -f "$file_name" ]; then
  echo "File not found: $file_name"
  exit 1
fi

# Check if the file is an ELF file
if ! file "$file_name" | grep -q "ELF"; then
  echo "Not an ELF file: $file_name"
  exit 1
fi

magic_number=$(readelf -h "$file_name" | grep "Magic:" | awk '{for(i=2; i<=NF; i++) printf "%s ", $i; print ""}' | sed 's/ $//')
class=$(readelf -h "$file_name" | grep "Class:" | awk '{print $2, $3}' | sed 's/ $//')
byte_order=$(readelf -h "$file_name" | grep "Data:" | awk '{print $4, $5}')
entry_point_address=$(readelf -h "$file_name" | grep "Entry point address:" | awk '{print $4}')

source ./messages.sh

display_elf_header_info

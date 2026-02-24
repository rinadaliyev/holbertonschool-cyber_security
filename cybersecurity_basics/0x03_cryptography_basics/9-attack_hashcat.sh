#!/bin/bash
hashcat -m 0 -a 0 "$1" wordlist1.txt wordlist2.txt

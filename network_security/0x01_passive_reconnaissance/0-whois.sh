#!/bin/bash
whois $1  | awk '/^Registrant/ || /^Admin/ || /^Tech/ {sub(":", ",") print}' > $1.csv

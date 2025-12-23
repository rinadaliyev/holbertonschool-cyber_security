#!/bin/bash
whois $1  | awk '/^Registrant/ || /^Admin/ || /^Tech/' > $1.csv

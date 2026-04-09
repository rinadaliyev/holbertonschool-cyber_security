#!/bin/bash
sudo nmap -sM -vv -p ftp,ssh,telnet,http,https $1

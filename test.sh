#!/bin/sh

export WINEPREFIX=/home/paul/mk-90/mk90emex_wine

cp smp0.bin ../mk90emex
cd ../mk90emex
gamescope -n -W 1580 -H 624 wine MK90.exe

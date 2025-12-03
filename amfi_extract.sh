#!/usr/bin/env bash

URL="https://www.amfiindia.com/spages/NAVAll.txt"
OUT=${1:-amfi_output.tsv}

curl -s -L "$URL" -o /tmp/nav.txt

awk -F ';' 'NR>1 { print $4 "\t" $5 }' /tmp/nav.txt > "$OUT"

echo "Extracted Scheme Name + NAV to $OUT"

#!/bin/bash
START=$(date +%s)

LOG_FILE=access.log
RES_FILE=res_bash.txt

echo "Total number of requests:" > "$RES_FILE"
wc -l "$LOG_FILE" | awk '{print $1}' >> "$RES_FILE"

echo -e "\nTotal number of requests by type:" >> "$RES_FILE"
awk '{print $6}' "$LOG_FILE" | tr -d \" | sed '/^.\{100\}./d' | \
sort | uniq -c | sort -rn | awk '{printf "%s - %d\n", $2, $1}' >> "$RES_FILE"

echo -e "\nTop 10 most frequent requests:" >> "$RES_FILE"
awk '{print $7}' "$LOG_FILE" | sed 's/^.*:\/\/[^\/]*//' | \
sort | uniq -c | sort -rnk1 | head | awk '{printf "PATH: %s\nNumber of requests: %d\n-\n", $2, $1}' >> "$RES_FILE"

echo -e "\nTop 5 largest requests with (4XX) error:" >> "$RES_FILE"
awk '{if ($9 ~ /4../) print $7, $9, $10, $1}' "$LOG_FILE" | \
sort -rnk3 | head -n 5 | awk '{printf "PATH: %s\nResponse code: %d\nSize: %d\nIP: %s\n-\n", $1, $2, $3, $4}' >> "$RES_FILE"

echo -e "\nTop 5 users by number of requests with (5XX) error:" >> "$RES_FILE"
awk '{if ($9 ~ /5../) print $1}' "$LOG_FILE" | \
sort | uniq -c | sort -rnk1 | head -n 5 | awk '{printf "IP: %s\nNumber of requests: %d\n-\n", $2, $1}' >> "$RES_FILE"

END=$(date +%s)
DIFF=$(($END - $START))
echo "It took $DIFF seconds"
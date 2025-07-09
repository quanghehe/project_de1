#!/bin/sh

echo ">>> Starting cron"
cron

echo ">>> Tailing cron log"
tail -f /var/log/cron.log

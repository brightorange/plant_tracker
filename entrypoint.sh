#!/bin/bash
set -e

DATA_DIR=/data

# a. move dummy data to the mounted volume (if not already there)
if [ -f /tmp/dummy.csv ]; then
  mkdir -p "$DATA_DIR"
  mv /tmp/dummy.csv "$DATA_DIR/dummy.csv"
fi

# b. erase dummy from temp (in case mv left nothing, still clean)
rm -f /tmp/dummy.csv

# c. run webapp using mounted folder as data location
export PLANT_TRACKER_DATA_DIR="$DATA_DIR"
cd /app
exec python3 -c "from app import app; app.run(host='0.0.0.0', port=80)"
#!/bin/bash

# Directories containing your video files
TRAIN_DIR="/raid/nthuy/SnapUGC/train"
TEST_DIR="/raid/nthuy/SnapUGC/test"

# Log directory
LOG_DIR="/raid/nthuy/SnapUGC/integrity_logs"
mkdir -p "$LOG_DIR"

# Function to check and remove corrupted videos
check_and_remove_corrupted() {
    local DIR=$1
    local LOG_FILE="$LOG_DIR/$(basename "$DIR")_corrupted.log"
    > "$LOG_FILE"  # Empty the log file

    find "$DIR" -type f -name "*.mp4" | while read -r FILE; do
        ffmpeg -v error -i "$FILE" -f null - 2>> "$LOG_FILE"
        if [ $? -ne 0 ]; then
            echo "Corrupted file detected: $FILE"
            rm "$FILE"
            echo "$FILE" >> "$LOG_FILE"
        fi
    done
}

# Check and remove corrupted files in both directories
check_and_remove_corrupted "$TRAIN_DIR"
check_and_remove_corrupted "$TEST_DIR"

echo "Corrupted file check and removal completed."

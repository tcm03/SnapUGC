#!/bin/bash

# Define absolute directories for videos
TRAIN_DIR="/root/hcmus/SnapUGC/data/train"
TEST_DIR="/root/hcmus/SnapUGC/data/test"

# Define the log directory under /raid/nthuy/SnapUGC
LOG_DIR="/root/hcmus/SnapUGC/integrity_logs"
TRAIN_LOG_DIR="$LOG_DIR/train"
TEST_LOG_DIR="$LOG_DIR/test"

# Create log directories if they don't exist
mkdir -p "$TRAIN_LOG_DIR"
mkdir -p "$TEST_LOG_DIR"

# Optional: change working directory to root so that relative paths aren't accidentally used
cd /

# Function to check and remove corrupted videos
check_and_remove_corrupted() {
    local DIR="$1"
    local LOG_DIR_FOR_THIS="$2"
    local LOG_FILE="$LOG_DIR_FOR_THIS/$(basename "$DIR")_corrupted.log"
    > "$LOG_FILE"  # Empty the log file

    # Use find with -print0 to ensure filenames are read correctly
    find "$DIR" -type f -name "*.mp4" -print0 | while IFS= read -r -d '' FILE; do
        # Ensure we have the absolute path for FILE
        ABS_FILE=$(realpath "$FILE")
        # Check for errors using ffmpeg
        ffmpeg -v error -i "$ABS_FILE" -f null - 2>> "$LOG_FILE"
        if [ $? -ne 0 ]; then
            echo "Corrupted file detected: $ABS_FILE"
            # rm "$ABS_FILE"
            echo "$ABS_FILE" >> "$LOG_FILE"
        fi
    done
}

# Process videos in both directories
echo "Processing training videos..."
check_and_remove_corrupted "$TRAIN_DIR" "$TRAIN_LOG_DIR"

echo "Processing testing videos..."
check_and_remove_corrupted "$TEST_DIR" "$TEST_LOG_DIR"

echo "Corrupted file check and removal completed."

#!/bin/bash

# Define directories
BASE_DIR="/raid/nthuy/SnapUGC"
TRAIN_DIR="$BASE_DIR/train_new"
TEST_DIR="$BASE_DIR/test_new"
LOG_DIR="$BASE_DIR/integrity_results"
TRAIN_LOG_DIR="$LOG_DIR/train"
TEST_LOG_DIR="$LOG_DIR/test"

# Create log directories if they don't exist
mkdir -p "$TRAIN_LOG_DIR"
mkdir -p "$TEST_LOG_DIR"

# Function to process videos in a given directory
process_videos() {
    local video_dir=$1
    local log_dir=$2

    # Find all .mp4 files and process them
    find "$video_dir" -type f -name "*.mp4" | while read -r video_file; do
        # Extract the base name of the video file
        base_name=$(basename "$video_file")
        # Define the corresponding log file path
        log_file="$log_dir/${base_name}.log"

        # Process the video file with ffmpeg to detect errors
        ffmpeg -v error -i "$video_file" -f null - 2> "$log_file"

        # Check if the log file is empty (no errors)
        if [ ! -s "$log_file" ]; then
            # Remove the empty log file
            rm "$log_file"
            echo "No errors found in $base_name"
        else
            echo "Errors detected in $base_name. See $log_file for details."
        fi
    done
}

# Process videos in both directories
echo "Processing training videos..."
process_videos "$TRAIN_DIR" "$TRAIN_LOG_DIR"

echo "Processing testing videos..."
process_videos "$TEST_DIR" "$TEST_LOG_DIR"

echo "Video integrity check completed."


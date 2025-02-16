import os
import csv
import subprocess
import datetime
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Logging configuration
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(log_dir, f"run_{timestamp}.log")

import logging
tcm_logger = logging.getLogger("tcm_logger")
tcm_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_filename, mode="w")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
tcm_logger.addHandler(file_handler)
tcm_logger.propagate = False

# Increase CSV field size limit
csv.field_size_limit(10**6)

def download_video_aria2c(row, output_dir, max_retries=5):
    """Download a single video using aria2c."""
    video_id, _, _, _, _, _, link = row
    output_path = os.path.join(output_dir, f"{video_id}.mp4")

    if os.path.exists(output_path):
        tcm_logger.info(f"[SKIP] Video {video_id} already exists.")
        return False

    retries = 0
    while retries < max_retries:
        try:
            # Construct the aria2c command
            command = [
                "aria2c",
                "--dir", output_dir,
                "--out", f"{video_id}.mp4",
                "--max-connection-per-server=16",
                "--min-split-size=1M",
                "--file-allocation=none",
                link
            ]
            # Execute the command
            result = subprocess.run(command, check=True, capture_output=True)
            tcm_logger.info(f"[SUCCESS] Downloaded {video_id} to {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            retries += 1
            tcm_logger.warning(f"[ERROR] Attempt {retries} failed for {video_id}: {e}")
        except FileNotFoundError:
            tcm_logger.error("aria2c is not installed or not found in system PATH.")
            return False

    tcm_logger.error(f"[FAILED] Could not download {video_id} after {max_retries} attempts.")
    return False

def process_file(input_file, output_dir, num_videos, num_workers):
    """Process metadata file and ensure at least num_videos are downloaded."""
    os.makedirs(output_dir, exist_ok=True)
    existing_files = set(f[:-4] for f in os.listdir(output_dir) if f.endswith(".mp4"))

    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # Skip header row
        rows = [row for row in reader if row[0] not in existing_files]

    total_videos = len(rows)
    required_videos = min(num_videos, total_videos)
    downloaded_videos = 0
    remaining_rows = rows.copy()

    if not remaining_rows:
        tcm_logger.info(f"[SKIP] All requested videos already exist in {output_dir}. Nothing to download.")
        return

    while downloaded_videos < required_videos and remaining_rows:
        needed_videos = required_videos - downloaded_videos
        to_download = remaining_rows[:needed_videos]

        tcm_logger.info(f"Starting batch download... Need {needed_videos} more videos.")

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_video = {executor.submit(download_video_aria2c, row, output_dir): row for row in to_download}

            for future in as_completed(future_to_video):
                row = future_to_video[future]
                try:
                    success = future.result()
                    if success:
                        downloaded_videos += 1
                except Exception as e:
                    tcm_logger.error(f"Unexpected error with video {row[0]}: {e}")

        remaining_rows = remaining_rows[needed_videos:]

    if downloaded_videos >= required_videos:
        tcm_logger.info(f"[COMPLETED] Successfully downloaded {downloaded_videos} new videos.")
    else:
        tcm_logger.warning(f"[PARTIAL] Only {downloaded_videos} videos downloaded out of {required_videos} required.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="snapugc",
        description="Download SnapUGC dataset."
    )
    parser.add_argument('--train_file', type=str, required=True, help="Path to the sanitized training file")
    parser.add_argument('--test_file', type=str, required=True, help="Path to the sanitized testing file")
    parser.add_argument('--train_dir', type=str, required=False, default="train", help="Path to the train directory (of clips)")
    parser.add_argument('--test_dir', type=str, required=False, default="test", help="Path to the test directory (of clips)")
    parser.add_argument('--num_workers', type=int, required=False, default=16, help="Number of workers to use for downloading")

    args = parser.parse_args()

    tcm_logger.info("Starting download for training set...")
    process_file(args.train_file, args.train_dir, 40000, num_workers=args.num_workers)

    tcm_logger.info("Starting download for testing set...")
    process_file(args.test_file, args.test_dir, 10000, num_workers=args.num_workers)

    tcm_logger.info("All downloads completed.")

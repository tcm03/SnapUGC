from huggingface_hub import snapshot_download, HfApi, login
import os
import random
import time

MY_HF_TOKEN=None
login(token=MY_HF_TOKEN)


def download_with_backoff():
    max_retries = 100
    base_wait_time = 60  # Start with a 1-minute wait time

    for attempt in range(max_retries):
        try:
            # Your download logic here
            for shard in range(4):
                repo_id = f"tcm03/SnapUGC_{shard}"
                local_dir = f"./SnapUGC_{shard}"
                os.makedirs(local_dir, exist_ok=True)
                snapshot_download(repo_id=repo_id, local_dir=local_dir, repo_type="dataset")
            break  # Exit loop if successful
        except Exception as e:
            if '429' in str(e):  # Check if it's a rate limit error
                wait_time = base_wait_time * (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
		raise  # Re-raise other exceptions

download_with_backoff()

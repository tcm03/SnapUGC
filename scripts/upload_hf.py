from huggingface_hub import HfApi

# Initialize the HfApi instance
api = HfApi()

# Define your repository ID and local folder path
repo_id = "tcm03/SnapUGC"
folder_path = "/root/hcmus/SnapUGC/data"

# Upload the folder with a specified number of worker threads
api.upload_large_folder(
    repo_id=repo_id,
    folder_path=folder_path,
    repo_type="dataset",  # Specify the repository type
    num_workers=20        # Adjust the number of workers based on your system's capabilities
)
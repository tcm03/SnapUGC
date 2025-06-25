import argparse
import os
import shutil
import json
from typing import List
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from huggingface_hub import HfApi

def split_dataset_dir(
    parent_path: str,
    dataset_name: str,
    dataset_dir: str,
    num_shards: int,
    prefix: str
) -> None:
    filenames: List[str] = os.listdir(dataset_dir)
    total_files = len(filenames)

    def copy_file(fileidx: int, shard_idx: int) -> None:
        if fileidx + shard_idx >= total_files:
            return
        shard_name: str = f"{dataset_name}_{shard_idx}"
        shard_dataset_dir: str = os.path.join(parent_path, shard_name, prefix)
        filename: str = filenames[fileidx + shard_idx]
        src_path: str = os.path.join(dataset_dir, filename)
        dest_path: str = os.path.join(shard_dataset_dir, filename)
        shutil.copy(src_path, dest_path)

    with ThreadPoolExecutor() as executor:
        futures = []
        with tqdm(total=total_files, desc=f"Sharding {dataset_dir}") as pbar:
            for fileidx in range(0, total_files, num_shards):
                for shard_idx in range(num_shards):
                    futures.append(executor.submit(copy_file, fileidx, shard_idx))
            for future in as_completed(futures):
                pbar.update(1)

def split_folder(
    folder_path: str,
    max_folder_files: int
) -> None:
    if not os.path.exists(folder_path):
        raise ValueError(f"Folder {folder_path} does not exist.")
    if not os.path.isdir(folder_path):
        raise ValueError(f"Path {folder_path} is not a directory.")

    files: List[str] = os.listdir(folder_path)
    num_files: int = len(files)
    num_folders: int = (num_files + max_folder_files - 1) // max_folder_files

    def move_file(file_name: str, folder_path_new: str) -> None:
        src_path: str = os.path.join(folder_path, file_name)
        dest_path: str = os.path.join(folder_path_new, file_name)
        shutil.move(src_path, dest_path)

    with ThreadPoolExecutor() as executor:
        futures = []
        with tqdm(total=num_files, desc=f"Splitting {folder_path} into smaller subfolders") as pbar:
            for i in range(num_folders):
                new_folder_name: str = f"{os.path.basename(folder_path)}_{i}"
                folder_path_new: str = os.path.join(folder_path, new_folder_name)
                os.makedirs(folder_path_new, exist_ok=True)

                start_idx: int = i * max_folder_files
                end_idx: int = min(start_idx + max_folder_files, num_files)
                for j in range(start_idx, end_idx):
                    file_name: str = files[j]
                    futures.append(executor.submit(move_file, file_name, folder_path_new))
            for future in as_completed(futures):
                pbar.update(1)

def split_dataset(
    dataset_path: str, 
    num_shards: int,
    folder_max_files: int,
    dataset_name = None
) -> None:

    train_dir: str = os.path.join(dataset_path, "train")
    if not os.path.exists(train_dir):
        raise ValueError(f"Train directory {train_dir} does not exist.")
    test_dir: str = os.path.join(dataset_path, "test")
    if not os.path.exists(test_dir):
        raise ValueError(f"Test directory {test_dir} does not exist.")

    # split dataset into multiple shards
    dataset_parent, ds_name = os.path.split(dataset_path)
    if dataset_name is None:
        dataset_name: str = ds_name
    for i in range(num_shards):
        shard_name: str = dataset_name + f"_{i}"
        shard_path: str = os.path.join(dataset_parent, shard_name)
        os.makedirs(shard_path, exist_ok=True)
        shard_train_dir: str = os.path.join(shard_path, "train")
        os.makedirs(shard_train_dir, exist_ok=True)
        shard_test_dir: str = os.path.join(shard_path, "test")
        os.makedirs(shard_test_dir, exist_ok=True)
    
    split_dataset_dir(dataset_parent, dataset_name, train_dir, num_shards, "train")
    split_dataset_dir(dataset_parent, dataset_name, test_dir, num_shards, "test")

    # split each shard's large folders into multiple subfolders
    for i in range(num_shards):
        shard_name: str = dataset_name + f"_{i}"
        shard_path: str = os.path.join(dataset_parent, shard_name)
        split_folder(os.path.join(shard_path, "train"), folder_max_files)
        split_folder(os.path.join(shard_path, "test"), folder_max_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="sharding",
        description="Shard the SnapUGC dataset for Huggingface dataset storage."
    )
    parser.add_argument('--dataset_path', type=str, required=True, help="Path to the dataset that has train and test folders.")
    parser.add_argument('--num_shards', type=int, required=True, help="Number of shards to split the dataset.")
    parser.add_argument('--folder_max_files', type=int, required=True, help="Maximum number of files in each subfolder.")
    parser.add_argument('--dataset_name', type=str, required=False, default="SnapUGC", help="Name of the dataset.")

    args = parser.parse_args()

    # WARNING: Make sure there is enough storage before running this dataset splitting
    # split_dataset(
    #     dataset_path=args.dataset_path,
    #     num_shards=args.num_shards,
    #     folder_max_files=args.folder_max_files,
    #     dataset_name=args.dataset_name
    # )
    
    # UPLOAD DATASET SHARDS
    api = HfApi()
    for shard in range(args.num_shards):
        print(f"\nUPLOADING SHARD {shard}...\n")
        repo_name = f"SnapUGC_{shard}"
        # api.create_repo(repo_name, repo_type="dataset", exist_ok=True)
        folder_path = os.path.join(os.getcwd(), f"SnapUGC_{shard}")
        api.upload_large_folder(
            repo_id=f"tcm03/{repo_name}",
            repo_type="dataset",
            folder_path=folder_path,
        )
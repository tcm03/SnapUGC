import os
import random
import shutil
from sklearn.model_selection import train_test_split

FULL_PATH = "/root/hcmus/SnapUGC/data"
MINI_PATH = "/root/hcmus/SnapUGC/data_mini"
TINY_PATH = "/root/hcmus/SnapUGC/data_tiny"
RANDOM_STATE = 42

if __name__ == "__main__":

    # train + val mini
    train_full_path = os.path.join(FULL_PATH, "train")
    train_full_file_paths = []
    for file_name in os.listdir(train_full_path):
        file_path = os.path.join(train_full_path, file_name)
        train_full_file_paths.append(file_path)
    sample_size = max(1, len(train_full_file_paths) // 10)
    train_mini_file_paths = random.sample(train_full_file_paths, sample_size)
    train_mini_path = os.path.join(MINI_PATH, "train")
    val_mini_path = os.path.join(MINI_PATH, "val")
    os.makedirs(train_mini_path, exist_ok = True)
    os.makedirs(val_mini_path, exist_ok = True)
    train_mini_file_paths, val_mini_file_paths = train_test_split(
        train_mini_file_paths, 
        train_size = 0.9, 
        random_state = RANDOM_STATE
    )
    for file_path in train_mini_file_paths:
        shutil.copy(file_path, train_mini_path)
    for file_path in val_mini_file_paths:
        shutil.copy(file_path, val_mini_path)
    print("--- DONE TRAIN MINI ---")

    # test mini
    test_full_path = os.path.join(FULL_PATH, "test")
    test_full_file_paths = []
    for file_name in os.listdir(test_full_path):
        file_path = os.path.join(test_full_path, file_name)
        test_full_file_paths.append(file_path)
    sample_size = max(1, len(test_full_file_paths) // 10)
    test_mini_file_paths = random.sample(test_full_file_paths, sample_size)
    test_mini_path = os.path.join(MINI_PATH, "test")
    os.makedirs(test_mini_path, exist_ok = True)
    for file_path in test_mini_file_paths:
        shutil.copy(file_path, test_mini_path)
    print("--- DONE TEST MINI ---")

    # train + val tiny
    sample_size = 48
    train_tiny_file_paths = random.sample(train_full_file_paths, sample_size)
    train_tiny_path = os.path.join(TINY_PATH, "train")
    val_tiny_path = os.path.join(TINY_PATH, "val")
    os.makedirs(train_tiny_path, exist_ok = True)
    os.makedirs(val_tiny_path, exist_ok = True)
    train_tiny_file_paths, val_tiny_file_paths = train_test_split(
        train_tiny_file_paths, 
        train_size = 0.5, 
        random_state = RANDOM_STATE
    )
    for file_path in train_tiny_file_paths:
        shutil.copy(file_path, train_tiny_path)
    for file_path in val_tiny_file_paths:
        shutil.copy(file_path, val_tiny_path)
    print("--- DONE TRAIN TINY ---")

    # test tiny
    sample_size = 24
    test_tiny_file_paths = random.sample(test_full_file_paths, sample_size)
    test_tiny_path = os.path.join(TINY_PATH, "test")
    os.makedirs(test_tiny_path, exist_ok = True)
    for file_path in test_tiny_file_paths:
        shutil.copy(file_path, test_tiny_path)
    print("--- DONE TEST TINY ---")

import os
import csv
import argparse
import json
from constants import *
import random
import shutil

def get_input_prompt() -> str:
    return "<image>\nThis video is a SnapChat video on one of many categories. The engagement rate defined for each such video is based on the average watch time and how long viewers stay engaged before skipping. The higher the average watch time and lower the skip rate, the more engaged the video is. The final prediction label is either 0 (not engaged), 1 (neutral), or 2 (engaged). Please predict one of the three labels for this video, based on its contents only."

def get_output_response(label: str) -> str:
    # return f"The engagement label of the video is {label}."
    if label == '0':
        return "The engagement level is 0 (not engaged)"
    elif label == '1':
        return "The engagement level is 1 (neutral)"
    elif label == '2':
        return "The engagement level is 2 (engaged)"
    assert False, "Invalid label"
    return "N/A"

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_label(
    nawp: int,
    quartile1: int,
    quartile3: int
) -> str:
    if nawp <= quartile1:
        return "0"
    if nawp >= quartile3:
        return "2"
    return "1"

def get_file_name(
    path: str
) -> str:
    if '/' in path:
        return path.split('/')[-1].strip()
    return path

def prepare_json_data(
    raw_file: str,
    data_dir: str,
    output_json_path: str,
    **kwargs
):
    output_dir = kwargs.get("output_dir", None)
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        
    data_json = []
    quartile1 = kwargs.get("quartile1", DEFAULT_QUARTILE1)
    quartile3 = kwargs.get("quartile3", DEFAULT_QUARTILE3)
    prefix = kwargs.get("prefix", "data")
    min_duration = kwargs.get("min_duration", DEFAULT_MIN_DURATION)
    max_duration = kwargs.get("max_duration", DEFAULT_MAX_DURATION)
    print(f"Preparing {prefix} json file...")
    with open(raw_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # Skip header row
        data_files = os.listdir(data_dir)
        num_samples = 0
        for row in reader:
            if row[1] == '' or row[2] == '' or row[3] == '':
                print(f"Empty row found: {row[0]}")
                continue
            if not is_float(row[1]) or not row[2].isdigit() or not row[3].isdigit():
                print(f"Non-numeric row found: {row[0]}")
                continue
            vid = str(row[0])
            duration = float(row[1])
            if f"{vid}.mp4" in data_files and min_duration <= int(duration) <= max_duration:
                nawp = int(row[3])
                label = get_label(nawp, quartile1, quartile3)
                full_path = f"{prefix}/{vid}.mp4"
                data_json.append({
                    "video": full_path,
                    "label": label,
                    "conversations": [
                        {
                            "from": "human",
                            "value": get_input_prompt()
                        },
                        {
                            "from": "gpt",
                            "value": get_output_response(label)
                        }
                    ]
                })
                num_samples += 1
        print(f"Number of {prefix} samples prepared: {num_samples}")
    data_json_label = {
        "0": [],
        "1": [],
        "2": []
    }
    for data_item in data_json:
        label = data_item["label"]
        data_json_label[label].append(data_item)

    max_samples_test = kwargs.get("max_samples_test", None)
    if max_samples_test is not None:
        # test split
        max_samples_test = min(max_samples_test, len(data_json))
        sample_test_json = []
        split_sizes = [max_samples_test // 3, max_samples_test // 3, max_samples_test - 2 * max_samples_test // 3] # equal split
        for i, label in enumerate(["0", "1", "2"]):
            sub_sample = random.sample(data_json_label[label], split_sizes[i])
            sample_test_json = sample_test_json + sub_sample

        print(f"Number of test samples selected: {len(sample_test_json)}")

        with open(output_json_path, "w", encoding="utf-8") as file:
            json.dump(sample_test_json, file, indent=4)

        print(f"Done dumping to {output_json_path}")

        if output_dir is not None:
            dest_dir = os.path.join(output_dir, "test")
            print(f"copying sampled data to {dest_dir}...")
            os.makedirs(dest_dir, exist_ok=True)
            for item in sample_test_json:
                file_name = get_file_name(item["video"])
                file_path = os.path.join(data_dir, file_name)
                shutil.copy(file_path, dest_dir)
            print(f"Done copying sampled data to {dest_dir}")

        return

    max_samples_train = kwargs.get("max_samples_train", None)
    max_samples_val = kwargs.get("max_samples_val", None)
    if max_samples_train is not None and max_samples_val is not None:
        # train + val split
        if max_samples_train + max_samples_val > len(data_json):
            assert False, "Train + val split size is greater than original dataset"
        split_train_sizes = [max_samples_train // 3, max_samples_train // 3, max_samples_train - 2 * max_samples_train // 3]
        split_val_sizes = [max_samples_val // 3, max_samples_val // 3, max_samples_val - 2 * max_samples_val // 3]
        sample_train_json = []
        sample_val_json = []
        for i, label in enumerate(["0", "1", "2"]):
            sub_sample = random.sample(data_json_label[label], split_train_sizes[i] + split_val_sizes[i])
            sub_sample_val = random.sample(sub_sample, split_val_sizes[i])
            sub_sample_val_paths = [item["video"] for item in sub_sample_val]
            sub_sample_train = []
            for item in sub_sample:
                if item["video"] not in sub_sample_val_paths:
                    sub_sample_train.append(item)
            sample_train_json = sample_train_json + sub_sample_train
            sample_val_json = sample_val_json + sub_sample_val
        
        print(f"Number of train samples selected: {len(sample_train_json)}")
        print(f"Number of val samples selected: {len(sample_val_json)}")

        with open(output_json_path, "w", encoding="utf-8") as file:
            json.dump(sample_train_json, file, indent=4)
        print(f"Done dumping to {output_json_path}")

        if output_dir is not None:
            dest_dir = os.path.join(output_dir, "train")
            print(f"copying sampled data to {dest_dir}...")
            os.makedirs(dest_dir, exist_ok=True)
            for item in sample_train_json:
                file_name = get_file_name(item["video"])
                file_path = os.path.join(data_dir, file_name)
                shutil.copy(file_path, dest_dir)
            print(f"Done copying sampled data to {dest_dir}")
        
        output_val_json_path = kwargs.get("output_val_json_path", None)
        if output_val_json_path is None:
            assert False, "Missing output path of validation json file"
        with open(output_val_json_path, "w", encoding="utf-8") as file:
            json.dump(sample_val_json, file, indent=4)
        print(f"Done dumping to {output_val_json_path}")

        if output_dir is not None:
            dest_dir = os.path.join(output_dir, "val")
            print(f"copying sampled data to {dest_dir}...")
            os.makedirs(dest_dir, exist_ok=True)
            for item in sample_val_json:
                file_name = get_file_name(item["video"])
                file_path = os.path.join(data_dir, file_name)
                shutil.copy(file_path, dest_dir)
            print(f"Done copying sampled data to {dest_dir}")

        return

    

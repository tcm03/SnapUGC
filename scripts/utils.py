import os
import csv
import argparse
import json
from constants import *
import random

def get_input_prompt() -> str:
    return "<image>\nThis video is a SnapChat video on one of many categories. The engagement rate defined for each such video is based on the average watch time and how long viewers stay engaged before skipping. The higher the average watch time and lower the skip rate, the more engaged the video is. The final prediction label is either 0 (not engaged), 1 (neutral), or 2 (engaged). Please predict one of the three labels for this video, based on its contents only."

def get_output_response(label: str) -> str:
    return f"The engagement label of the video is {label}."

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

def prepare_json_data(
    raw_file: str,
    data_dir: str,
    output_json_path: str,
    **kwargs
):
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

    max_samples = kwargs.get("max_samples", None)
    sample_data_json = data_json
    if max_samples is not None:
        sample_data_json = random.sample(data_json, min(max_samples, len(sample_data_json)))

    print(f"Number of {prefix} samples selected: {len(sample_data_json)}")

    with open(output_json_path, "w", encoding="utf-8") as file:
        json.dump(sample_data_json, file, indent=4)

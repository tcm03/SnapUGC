import csv
import os
import numpy as np
import pandas as pd

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

csv.field_size_limit(10**6)

if __name__ == "__main__":
    nawps = []
    with open("train_out_sanitized.txt", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # Skip header row
        data_files = os.listdir("data/train")
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
            if f"{vid}.mp4" in data_files:
                nawp = int(row[3])
                nawps.append(nawp)
                # label = get_label(nawp, quartile1, quartile3)
                # full_path = f"{prefix}/{vid}.mp4"
                # data_json.append({
                #     "video": full_path,
                #     "label": label,
                #     "conversations": [
                #         {
                #             "from": "human",
                #             "value": get_input_prompt()
                #         },
                #         {
                #             "from": "gpt",
                #             "value": get_output_response(label)
                #         }
                #     ]
                # })
                num_samples += 1
        print(f"Number of samples prepared: {num_samples}")

    p_33 = np.percentile(nawps, 25)
    p_66 = np.percentile(nawps, 75)
    print(p_33)
    print(p_66)

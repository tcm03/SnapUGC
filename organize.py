import csv
import argparse

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

def get_input_prompt() -> str:
    return "<image>\nThis video is a SnapChat video on one of many categories. The engagement rate defined for each such video is based on the average watch time and how long viewers stay engaged before skipping. The higher the average watch time and lower the skip rate, the more engaged the video is. The final prediction label is either 0 (not engaged), 1 (neutral), or 2 (engaged). Please predict one of the three labels for this video, based on its contents only."

def get_output_response(label: str) -> str:
    return f"The engagement label of the video is {label}."

def prepare_train_json(
    raw_train: str,
    train_dir: str,
    train_json_path: str,
    quartile1: int,
    quartile3: int
):
    train_json = []
    with open(raw_train, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # Skip header row
        train_dir_files = os.listdir(train_dir)
        for row in reader:
            if row[1] == '' or row[2] == '' or row[3] == '':
                print(f"Empty row found: {row[0]}")
                continue
            if not is_float(row[1]) or not row[2].isdigit() or not row[3].isdigit():
                print(f"Non-numeric row found: {row[0]}")
                continue
            vid = str(row[0])
            if f"{vid}.mp4" in train_dir_files:
                nawp = int(row[3])
                label = get_label(nawp, quartile1, quartile3)
                train_json.append({
                    "video": f"train/{vid}.mp4",
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
            
    with open(train_json_path, "w", encoding="utf-8") as file:
        json.dump(train_json, file, indent=4)


def prepare_test_json(
    raw_test: str,
    test_dir: str,
    test_json_path: str,
    quartile1: int,
    quartile3: int
):
    test_json = []
    with open(raw_test, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # Skip header row
        test_dir_files = os.listdir(test_dir)
        for row in reader:
            if row[1] == '' or row[2] == '' or row[3] == '':
                print(f"Empty row found: {row[0]}")
                continue
            if not is_float(row[1]) or not row[2].isdigit() or not row[3].isdigit():
                print(f"Non-numeric row found: {row[0]}")
                continue
            vid = str(row[0])
            if f"{vid}.mp4" in test_dir_files:
                nawp = int(row[3])
                label = get_label(nawp, quartile1, quartile3)
                test_json.append({
                    "video": f"test/{vid}.mp4",
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
            
    with open(test_json_path, "w", encoding="utf-8") as file:
        json.dump(test_json, file, indent=4)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="organize",
        description="Split SnapUGC into training and testing sets, and label clips based on statistical quartiles."
    )
    parser.add_argument('--raw_train', type=str, required=True, help="Path to the raw training file")
    parser.add_argument('--raw_test', type=str, required=True, help="Path to the raw testing file")
    parser.add_argument('--train_json', type=str, required=True, help="Path to the training json file")
    parser.add_argument('--test_json', type=str, required=True, help="Path to the testing json file")
    parser.add_argument('--train_dir', type=str, required=False, default="train", help="Path to the train directory (of clips)")
    parser.add_argument('--test_dir', type=str, required=False, default="test", help="Path to the test directory (of clips)")
    parser.add_argument('--quartile1', type=int, required=False, default=32769, help="First quartile for labeling")
    parser.add_argument('--quartile3', type=int, required=False, default=98323, help="Third quartile for labeling")
    # parser.add_argument('--num_workers', type=int, required=False, default=16, help="Number of workers to use for downloading")
    
    args = parser.parse_args()  # Parse the arguments
    prepare_train_json(args.raw_train, args.train_dir, args.train_json, args.quartile1, args.quartile3)
    prepare_test_json(args.raw_test, args.test_dir, args.test_json, args.quartile1, args.quartile3)
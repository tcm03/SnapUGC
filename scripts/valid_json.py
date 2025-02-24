import argparse
import json
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="valid_json.py",
        description="Validate metadata in the JSON file"
    )
    parser.add_argument('--json_file', type=str, required=True, help="Path to the input JSON file")
    parser.add_argument('--folder_path', type=str, required=True, help="Path to the folder containing the videos")
    args = parser.parse_args()

    with open(args.json_file, "r", encoding = 'utf-8') as file:
        data = json.load(file)
        for item in data:
            video_path = os.path.join(args.folder_path, item["video"])
            # check if this path exists
            if not os.path.exists(video_path):
                print(f"Video path {video_path} does not exist")

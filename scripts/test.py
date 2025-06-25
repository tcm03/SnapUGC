import json
import os

INPUT_JSON = "SnapUGC_0/snapugc0_test_engcaption.json"
OUTPUT_JSON = "SnapUGC_0/snapugc0_test_engcaption_image.json"

def main():
    with open(INPUT_JSON, "r") as f:
        data = json.load(f)
    for item in data:
        item["conversations"][0]["value"] = "<image>\n"
    with open(OUTPUT_JSON, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()
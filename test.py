import os
import csv
from typing import List, Optional

def main():
    titles: List[Optional[str]] = []
    descriptions: List[Optional[str]] = []
    with open("train_out_sanitized.txt", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        header = next(reader)
        for i, row in enumerate(reader):
            title: str = row[4]
            description: str = row[5]
            if title:
                titles.append(title)
            if description:
                descriptions.append(description)
    first_titles: str = '\n'.join(titles[:5])
    first_descriptions: str = '\n'.join(descriptions[:5])
    print(f"There are {len(titles)} titles, first few are:{first_titles}")
    print(f"There are {len(descriptions)} descriptions, first few are:{first_descriptions}")

if __name__ == "__main__":
    main()
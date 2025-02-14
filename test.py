import csv
import argparse
import numpy as np
import pandas as pd

csv.field_size_limit(10**6)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'val',
        description="Validate the data"
    )
    parser.add_argument('--input_file', type=str, required=True, help='Path to input file to validate.')
    parser.add_argument('--output_file', type=str, default="describe.csv", help='Path to output file for describe.')
    args = parser.parse_args()

    ecr_scores = []
    nwap_scores = []
    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)  # Store header row
        rows = list(reader)
        for row in rows:
            ecr = int(row[2])
            nwap = int(row[3])
            ecr_scores.append(ecr)
            nwap_scores.append(nwap)
    ecr_scores_np = np.array(ecr_scores)
    nwap_scores_np = np.array(nwap_scores)
    df_describe = pd.DataFrame({'ecr': ecr_scores_np, 'nwap': nwap_scores_np})
    df_describe.describe().to_csv(args.output_file, sep='\t')
    print(df_describe['ecr'].nunique())
    print(df_describe['nwap'].nunique())

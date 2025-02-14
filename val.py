import csv
import argparse

csv.field_size_limit(10**6)

def validate_row(row):
    edge_case = False
    if len(row) < 7:
        edge_case = True
    else:
        for i in [0, 1, 2, 3, 6]:
            if row[i] == '':
                edge_case = True
                break
    if edge_case:
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'val',
        description="Validate the data"
    )
    parser.add_argument('--input_file', type=str, required=True, help='Path to input file to validate.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('--output_file', type=str, help='Optional path to the output file for problematic lines.')
    args = parser.parse_args()

    edge_rows = []
    with open(args.input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)  # Store header row
        rows = list(reader)
        for row in rows:
            if validate_row(row) is False:
                if args.verbose:
                    for s in row:
                        print(len(s), end = ' ')
                    print()
                edge_rows.append(row)

    if args.verbose:
        print(f'Len edge rows: {len(edge_rows)}')
    if args.output_file is not None:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(header)  # Write header row
            writer.writerows(edge_rows)
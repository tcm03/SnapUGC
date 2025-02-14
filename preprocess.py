import argparse

# Preprocess the input file to handle unmatched quotes
def preprocess_file(input_file, sanitized_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(sanitized_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            # Replace unmatched quotes
            if line.count('"') % 2 != 0:
                line = line.replace('"', '')  # Remove all quotes if unbalanced

            line = line.strip() + '\n'
            outfile.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="preprocess",
        description="Preprocess SnapUGC dataset: Raw SnapUGC contains so many unfiltered characters and the format rule isn't consistent."
    )
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input file")
    parser.add_argument('--output_file', type=str, required=True, help="Path to the sanitized output file")
    
    args = parser.parse_args()  # Parse the arguments

    # Call the preprocess function with the parsed arguments
    preprocess_file(args.input_file, args.output_file)

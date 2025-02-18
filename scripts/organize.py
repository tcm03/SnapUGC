import argparse
from constants import *
from utils import prepare_json_data

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
    parser.add_argument('--min_duration', type=int, required=False, default=DEFAULT_MIN_DURATION, help="Minimum duration of clips to consider")
    parser.add_argument('--max_duration', type=int, required=False, default=DEFAULT_MAX_DURATION, help="Maximum duration of clips to consider")
    parser.add_argument('--max_samples_train', type=int, required=False, default=None, help="Maximum number of training samples to consider")
    parser.add_argument('--max_samples_test', type=int, required=False, default=None, help="Maximum number of testing samples to consider")
    parser.add_argument('--quartile1', type=int, required=False, default=DEFAULT_QUARTILE1, help="First quartile for labeling")
    parser.add_argument('--quartile3', type=int, required=False, default=DEFAULT_QUARTILE3, help="Third quartile for labeling")
    # parser.add_argument('--num_workers', type=int, required=False, default=16, help="Number of workers to use for downloading")
    
    args = parser.parse_args()  # Parse the arguments
    prepare_json_data(
        raw_file = args.raw_train, 
        data_dir = args.train_dir, 
        output_json_path = args.train_json, 
        quartile1 = args.quartile1, 
        quartile3 = args.quartile3, 
        prefix="train",
        min_duration = args.min_duration,
        max_duration = args.max_duration,
        max_samples = args.max_samples_train
    )
    prepare_json_data(
        raw_file = args.raw_test, 
        data_dir = args.test_dir, 
        output_json_path = args.test_json, 
        quartile1 = args.quartile1, 
        quartile3 = args.quartile3, 
        prefix="test",
        min_duration = args.min_duration,
        max_duration = args.max_duration,
        max_samples = args.max_samples_test
    )
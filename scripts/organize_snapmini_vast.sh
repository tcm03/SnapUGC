RAW_TRAIN_PATH="/root/hcmus/SnapUGC/train_out_sanitized.txt"
RAW_TEST_PATH="/root/hcmus/SnapUGC/test_out_sanitized.txt"
TRAIN_JSON_PATH="/root/hcmus/SnapUGC/snapugc_mini_train.json"
VAL_JSON_PATH="/root/hcmus/SnapUGC/snapugc_mini_val.json"
TEST_JSON_PATH="/root/hcmus/SnapUGC/snapugc_mini_test.json"
TRAIN_DIR="/root/hcmus/SnapUGC/data/train"
TEST_DIR="/root/hcmus/SnapUGC/data/test"
OUTPUT_DIR="/root/hcmus/SnapUGC/data_mini"

python scripts/organize.py \
--raw_train $RAW_TRAIN_PATH \
--raw_test $RAW_TEST_PATH \
--train_json $TRAIN_JSON_PATH \
--val_json $VAL_JSON_PATH \
--test_json $TEST_JSON_PATH \
--train_dir $TRAIN_DIR \
--test_dir $TEST_DIR \
--output_dir $OUTPUT_DIR \
--min_duration 0 \
--max_duration 65 \
--max_samples_train 9645 \
--max_samples_val 1072 \
--max_samples_test 1462 \

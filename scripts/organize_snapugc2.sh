RAW_TRAIN_PATH="/root/hcmus/SnapUGC/train_out_sanitized.txt"
RAW_TEST_PATH="/root/hcmus/SnapUGC/test_out_sanitized.txt"
TRAIN_JSON_PATH="/root/hcmus/SnapUGC/SnapUGC_2/snapugc2_train.json"
VAL_JSON_PATH="/root/hcmus/SnapUGC/SnapUGC_2/snapugc2_val.json"
TEST_JSON_PATH="/root/hcmus/SnapUGC/SnapUGC_2/snapugc2_test.json"
TRAIN_DIR="/root/hcmus/SnapUGC/SnapUGC_2/train"
TEST_DIR="/root/hcmus/SnapUGC/SnapUGC_2/test"
OUTPUT_DIR="/root/hcmus"

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
--max_samples_train 24297 \
--max_samples_val 2429 \
--max_samples_test 3646 \

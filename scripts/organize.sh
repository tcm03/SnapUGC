RAW_TRAIN_PATH="/media02/nthuy/data/SnapUGC/train_out_sanitized.csv"
RAW_TEST_PATH="/media02/nthuy/data/SnapUGC/test_out_sanitized.csv"
TRAIN_JSON_PATH="/raid/nthuy/SnapUGC/snapugc_train.json"
TEST_JSON_PATH="/raid/nthuy/SnapUGC/snapugc_test.json"
TRAIN_DIR="/raid/nthuy/SnapUGC/train"
TEST_DIR="/raid/nthuy/SnapUGC/test"

python scripts/organize.py \
--raw_train $RAW_TRAIN_PATH \
--raw_test $RAW_TEST_PATH \
--train_json $TRAIN_JSON_PATH \
--test_json $TEST_JSON_PATH \
--train_dir $TRAIN_DIR \
--test_dir $TEST_DIR
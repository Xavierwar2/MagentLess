set -x

# 创建一个api_key.sh文件放在script目录下，文件内容按照以下格式填写：
# export OPENAI_API_KEY=
# export OPENAI_BASE_URL=
# export OPENAI_MODEL=
# export OPENAI_EMBED_URL=
source script/api_key.sh

export PYTHONPATH=`pwd`
export TARGET_ID=
export NJ=50
export NUM_SETS=2
export NUM_SAMPLES_PER_SET=2
export NUM_REPRODUCTION=0
export FOLDER_NAME=darkreader_test #会生成在results/下
export SWEBENCH_LANG=typescript
export PROJECT_FILE_LOC="structure"
export DATASET=local_json
export LOCAL_DATASET_FILE="data/ts/darkreader__darkreader_dataset.jsonl"
export SPLIT=test

# Optional: restrict this run to selected cases.
# RUN_CASES_FILE accepts one case per line, e.g. darkreader/darkreader:pr-6747
# RUN_INSTANCE_IDS accepts comma-separated ids, e.g. darkreader__darkreader-6747,darkreader__darkreader-7241
export RUN_CASES_FILE=${RUN_CASES_FILE:-}
export RUN_INSTANCE_IDS=${RUN_INSTANCE_IDS:-}
export ORIGINAL_LOCAL_DATASET_FILE=$LOCAL_DATASET_FILE
export FILTERED_DATASET_FILE="results/$FOLDER_NAME/selected_dataset.jsonl"

if [ -n "$RUN_CASES_FILE" ] || [ -n "$RUN_INSTANCE_IDS" ]; then
    mkdir -p "results/$FOLDER_NAME"
    python script/filter_dataset.py
    export LOCAL_DATASET_FILE=$FILTERED_DATASET_FILE
    export TARGET_ID=
fi

# 需要先执行一遍：
mkdir -p "repo" "structure"
python script/generate_structure.py

./script/localization1.1.sh
./script/localization1.2.sh
./script/localization1.3.sh
./script/localization1.4.sh
./script/localization2.1.sh
./script/localization3.1.sh
./script/localization3.2.sh

./script/repair.sh

# 注释掉的部分仅适用SWE-BENCH数据集，不需要执行
#./script/selection1.1.sh
#./script/selection1.2.sh
#./script/selection1.3.sh
#./script/selection2.1.sh
#./script/selection2.2.sh
#./script/selection2.3.sh
#./script/selection2.4.sh
./script/selection3.1.sh

# 这个评估也是不适用的，还是用我们自己的
#./script/evaluation.sh

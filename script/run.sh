set -x

# api_key.sh
export OPENAI_API_KEY=sk-IcBy9O6Rxj51SOOHAemuRQsJOvToRQVatlpqyN3RTeqXR3uC
export OPENAI_BASE_URL=https://api.aipaibox.com/v1
export OPENAI_MODEL=gpt-5.4
export OPENAI_EMBED_URL=https://api.aipaibox.com/v1/embeddings
# source script/api_key.sh

export PYTHONPATH=`pwd`
export TARGET_ID=
export NJ=50
export NUM_SETS=2
export NUM_SAMPLES_PER_SET=2
export NUM_REPRODUCTION=0
export FOLDER_NAME=darkreader_test
export SWEBENCH_LANG=typescript
export PROJECT_FILE_LOC="structure"
export DATASET=local_json
export LOCAL_DATASET_FILE="data/ts/darkreader__darkreader_dataset.jsonl"
export SPLIT=test

# mkdir -p "repo" "structure"
# python script/generate_structure.py

./script/localization1.1.sh
./script/localization1.2.sh
./script/localization1.3.sh
./script/localization1.4.sh
./script/localization2.1.sh
./script/localization3.1.sh
./script/localization3.2.sh

./script/repair.sh

#./script/selection1.1.sh
#./script/selection1.2.sh
#./script/selection1.3.sh
#./script/selection2.1.sh
#./script/selection2.2.sh
#./script/selection2.3.sh
#./script/selection2.4.sh
./script/selection3.1.sh

#./script/evaluation.sh

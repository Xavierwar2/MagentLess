import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.append('.')

from tqdm import tqdm

from get_repo_structure.get_repo_structure import (
    get_project_structure_from_scratch,
    repo_to_top_folder,
)

PLAYGROUND = 'playground'
OUT_DIR = 'structure'
LANGUAGE = 'typescript'


def load_dataset():
    dataset_file = os.environ.get('LOCAL_DATASET_FILE')
    if dataset_file:
        with open(dataset_file, 'r') as fin:
            return [json.loads(line) for line in fin if line.strip()]

    with open(f'data/{LANGUAGE}_verified.jsonl', 'r') as fin:
        return [json.loads(line) for line in fin if line.strip()]


def ensure_structure(data):
    repo_name = f'{data["org"]}/{data["repo"]}'
    instance_id = data['instance_id']
    commit_id = data['base']['sha']
    repo_dir = repo_to_top_folder.get(repo_name)
    if repo_dir is None:
        raise RuntimeError(f'Unsupported repository for structure generation: {repo_name}')

    repo_path = Path('repo') / repo_dir
    if not repo_path.exists():
        raise FileNotFoundError(
            f'Missing local repo checkout for {repo_name}: expected {repo_path}. '
            'Please clone the repository into ./repo first.'
        )

    output_file = Path(OUT_DIR) / f'{instance_id}.json'
    if output_file.exists() and os.environ.get('SKIP_EXISTING_STRUCTURE', '1') == '1':
        return 'skipped'

    structure = get_project_structure_from_scratch(
        repo_name=repo_name,
        commit_id=commit_id,
        instance_id=instance_id,
        repo_playground=PLAYGROUND,
    )
    with open(output_file, 'w') as fout:
        json.dump(structure, fout)
    return 'generated'


def main():
    dataset = load_dataset()
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    by_repo = defaultdict(list)
    for item in dataset:
        by_repo[f'{item["org"]}/{item["repo"]}'].append(item)

    print(f'Loaded {len(dataset)} instances from LOCAL_DATASET_FILE={os.environ.get("LOCAL_DATASET_FILE", "<default>")}')
    print(f'Preparing structures for {len(by_repo)} repositories')

    generated = 0
    skipped = 0
    for item in tqdm(dataset):
        status = ensure_structure(item)
        if status == 'generated':
            generated += 1
        else:
            skipped += 1

    print(f'Structure generation finished: generated={generated}, skipped={skipped}, out_dir={OUT_DIR}')


if __name__ == '__main__':
    main()

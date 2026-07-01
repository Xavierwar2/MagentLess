import json
import os
from pathlib import Path


def normalize_case_id(value):
    value = value.strip()
    if not value:
        return None
    if "__" in value and "-" in value:
        return value
    if ":pr-" in value:
        repo, number = value.split(":pr-", 1)
        org, name = repo.split("/", 1)
        return f"{org}__{name}-{number}"
    if "/pull/" in value:
        repo, number = value.split("/pull/", 1)
        org, name = repo.split("/", 1)
        return f"{org}__{name}-{number}"
    raise ValueError(f"Unsupported case id format: {value}")


def load_selected_ids():
    selected = []

    ids = os.environ.get("RUN_INSTANCE_IDS", "")
    for item in ids.replace(";", ",").split(","):
        instance_id = normalize_case_id(item)
        if instance_id:
            selected.append(instance_id)

    cases_file = os.environ.get("RUN_CASES_FILE", "")
    if cases_file:
        with open(cases_file, "r", encoding="utf-8") as fin:
            for line in fin:
                instance_id = normalize_case_id(line)
                if instance_id:
                    selected.append(instance_id)

    return list(dict.fromkeys(selected))


def main():
    input_file = Path(os.environ["LOCAL_DATASET_FILE"])
    output_file = Path(os.environ["FILTERED_DATASET_FILE"])
    selected_ids = load_selected_ids()

    if not selected_ids:
        raise RuntimeError("Set RUN_CASES_FILE or RUN_INSTANCE_IDS before filtering.")

    rows = []
    with input_file.open("r", encoding="utf-8") as fin:
        for line in fin:
            if not line.strip():
                continue
            row = json.loads(line)
            if row["instance_id"] in selected_ids:
                rows.append(row)

    found = {row["instance_id"] for row in rows}
    missing = [instance_id for instance_id in selected_ids if instance_id not in found]
    if missing:
        raise RuntimeError(
            f"Selected ids not found in {input_file}: {', '.join(missing)}"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as fout:
        for row in rows:
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Filtered dataset: {len(rows)} instances -> {output_file}")


if __name__ == "__main__":
    main()

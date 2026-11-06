#!/usr/bin/env python3
"""Group tab-delimited MeSH annotations by dataset accession as JSON."""

import argparse
import csv
import json
from pathlib import Path


DIRECTORY = Path(__file__).resolve().parent


def convert(input_path: Path, output_path: Path) -> None:
    """Preserve annotation values and row order within each accession."""
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must differ.")

    annotations = {}
    with input_path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source, delimiter="\t")
        if reader.fieldnames != ["accession", "mesh_term", "curie"]:
            raise ValueError("Expected TSV columns: accession, mesh_term, curie.")
        for row in reader:
            if None in row or any(not value for value in row.values()):
                raise ValueError(f"Invalid annotation at line {reader.line_num}.")
            annotations.setdefault(row["accession"], []).append(
                {"term": row["mesh_term"], "curie": row["curie"]}
            )

    output_path.write_text(
        json.dumps(annotations, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path,
        default=DIRECTORY / "dataset-MeSH-approved-annotations.txt",
        help="Input annotation TSV file.",
    )
    parser.add_argument(
        "--output", type=Path,
        default=DIRECTORY / "dataset-MeSH-approved-annotations.json",
        help="Output JSON file.",
    )
    args = parser.parse_args()
    convert(args.input, args.output)


if __name__ == "__main__":
    main()

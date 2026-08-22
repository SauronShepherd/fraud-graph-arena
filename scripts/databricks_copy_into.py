from __future__ import annotations
import argparse

def main() -> int:
    parser = argparse.ArgumentParser(description="Retired unsafe post-load COPY INTO path")
    parser.parse_args()
    raise SystemExit("post-load COPY INTO is retired; use scripts/import_databricks_candidate.py")

if __name__ == "__main__": raise SystemExit(main())

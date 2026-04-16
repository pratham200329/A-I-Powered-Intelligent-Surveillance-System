import argparse
from pathlib import Path

from data_pipeline.feature_store import FeatureStore
from ml_models.train_all import train_all_models


def main() -> None:
    parser = argparse.ArgumentParser(description="Train all ML models for visitor behavior analysis")
    parser.add_argument("--dataset", type=str, default="data/behavior_dataset.csv", help="CSV dataset path")
    parser.add_argument("--from-db", action="store_true", help="Build dataset from existing visit logs in DB")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)

    if args.from_db:
        df = FeatureStore().logs_dataframe()
        if df.empty:
            raise RuntimeError("No logs available in database to train from")
        dataset_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(dataset_path, index=False)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    metrics = train_all_models(dataset_path)
    print("Training complete")
    print(metrics)


if __name__ == "__main__":
    main()

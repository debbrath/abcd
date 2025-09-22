# scripts/batch_convert.py
# Example to convert the 3 datasets (after you download/unzip them into ./data)
from pathlib import Path
from scripts.convert_to_sqlite import csv_to_sqlite


DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)


pairs = [
# Update filenames if the Kaggle downloads have different names
(DATA_DIR / "heart.csv", "heart_disease.db", "heart_disease"),
(DATA_DIR / "cancer.csv", "cancer.db", "cancer"),
(DATA_DIR / "diabetes.csv", "diabetes.db", "diabetes"),
]


for csv_path, db_name, table_name in pairs:
 if csv_path.exists():
  csv_to_sqlite(str(csv_path), db_name, table_name)
else:
  print(f"Missing {csv_path}. Please download from Kaggle and place it in ./data/")
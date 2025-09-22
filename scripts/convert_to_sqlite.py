# scripts/convert_to_sqlite.py
import argparse
import pandas as pd
from sqlalchemy import create_engine




def csv_to_sqlite(csv_path: str, db_path: str, table_name: str, if_exists: str = "replace"):
    print(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Rows: {len(df)}, Columns: {list(df.columns)}")
    engine = create_engine(f"sqlite:///{db_path}")
    print(f"Writing to {db_path} -> table: {table_name}")
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--table", required=True)
    args = parser.parse_args()
    csv_to_sqlite(args.csv, args.db, args.table)
import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE = BASE_DIR / "backend" / "database" / "camara.db"

CSV = (
    BASE_DIR
    / "dados_importacao"
    / "BDRTEST-2"
    / "proposicoes-2020.csv"
)

print("Banco:", DATABASE)
print("CSV:", CSV)

df = pd.read_csv(
    arquivo,
    sep=";",
    engine="python",
    low_memory=False
)

print(df.columns)

print(df.head())
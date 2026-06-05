import pandas as pd
import sqlite3
import glob

conn = sqlite3.connect("database/camara.db")

arquivos = glob.glob("database/csv/*.csv")

for arquivo in arquivos:

    print(f"Importando {arquivo}")

    df = pd.read_csv(
    arquivo,
    sep=';',
    encoding='utf-8',
    low_memory=False
)

    df.to_sql(
        "Despesas",
        conn,
        if_exists="append",
        index=False
    )

print("Importação concluída!")
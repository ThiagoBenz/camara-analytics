import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

DATABASE = BASE_DIR / "database" / "camara.db"

CSV_DIR = (
    BASE_DIR.parent
    / "dados_importacao"
    / "BDRTEST-2"
)

conn = sqlite3.connect(DATABASE)

arquivos = sorted(
    CSV_DIR.glob("votacoesOrientacoes-*.csv")
)

for arquivo in arquivos:

    ano = arquivo.stem.split("-")[-1]

    print(f"Importando {ano}...")

    df = pd.read_csv(
        arquivo,
        sep=";",
        engine="python",
        on_bad_lines="skip"
    )

    df = df.rename(columns={

        "idVotacao": "id_votacao",

        "siglaBancada": "siglaBancada",

        "orientacao": "orientacao"

    })

    colunas = [

        "id_votacao",

        "siglaBancada",

        "orientacao"

    ]

    df = df[colunas]

    df["siglaBancada"] = (
        df["siglaBancada"]
        .fillna("")
        .astype(str)
    )

    df["orientacao"] = (
        df["orientacao"]
        .fillna("")
        .astype(str)
    )

    print(f"{len(df)} registros")

    df.to_sql(
        "VotOrientacoes",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
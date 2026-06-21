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

# Retomar somente de 2023 em diante
anos = [2023, 2024, 2025, 2026]

arquivos = [
    CSV_DIR / f"votacoesVotos-{ano}.csv"
    for ano in anos
]

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

        "deputado_id": "id_deputado",

        "voto": "voto"

    })

    colunas = [

        "id_votacao",

        "id_deputado",

        "voto"

    ]

    df = df[colunas]

    # Corrigir id_deputado

    df["id_deputado"] = pd.to_numeric(
        df["id_deputado"],
        errors="coerce"
    )

    # Remover linhas sem deputado

    df = df.dropna(
        subset=["id_deputado"]
    )

    df["id_deputado"] = (
        df["id_deputado"]
        .astype(int)
    )

    df["voto"] = (
        df["voto"]
        .fillna("")
        .astype(str)
    )

    print(f"{len(df)} registros")

    df.to_sql(
        "VotVotos",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
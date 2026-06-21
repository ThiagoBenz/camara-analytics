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
    CSV_DIR.glob("eventosPresencaDeputados-*.csv")
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

        "idEvento": "id_evento",

        "idDeputado": "id_deputado",

        "dataHoraInicio": "data_hora_inicio_evento"

    })

    df["data_evento"] = (
        pd.to_datetime(
            df["data_hora_inicio_evento"],
            errors="coerce"
        )
        .dt.date
        .astype(str)
    )

    colunas = [

        "id_evento",

        "id_deputado",

        "data_evento",

        "data_hora_inicio_evento"

    ]

    df = df[colunas]

    print(f"{len(df)} registros")

    df.to_sql(
        "PresencaDeputados",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
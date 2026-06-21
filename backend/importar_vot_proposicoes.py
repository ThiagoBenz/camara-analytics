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
    CSV_DIR.glob("votacoesObjetos-*.csv")
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

        "data": "data_votacao",

        "descricao": "descricao_votacao",

        "proposicao_id": "proposicao_id",

        "proposicao_siglaTipo":
            "proposicao_siglaTipo",

        "proposicao_numero":
            "proposicao_numero",

        "proposicao_ano":
            "proposicao_ano",

        "proposicao_ementa":
            "proposicao_ementa",

        "proposicao_titulo":
            "proposicao_titulo"

    })

    colunas = [

        "id_votacao",

        "data_votacao",

        "descricao_votacao",

        "proposicao_id",

        "proposicao_siglaTipo",

        "proposicao_numero",

        "proposicao_ano",

        "proposicao_ementa",

        "proposicao_titulo"

    ]

    df = df[colunas]

    print(f"{len(df)} registros")

    df.to_sql(
        "VotProposicoes",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
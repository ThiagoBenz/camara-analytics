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

arquivos = sorted(CSV_DIR.glob("proposicoesTemas-*.csv"))

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

        "siglaTipo": "sigla_tipo_proposicao",

        "numero": "numero_proposicao",

        "ano": "ano_proposicao",

        "codTema": "cod_tema",

        "tema": "tema",

        "relevancia": "relevancia"

    })

    colunas = [

        "sigla_tipo_proposicao",

        "numero_proposicao",

        "ano_proposicao",

        "cod_tema",

        "tema",

        "relevancia"

    ]

    df = df[colunas]

    print(f"{len(df)} registros")

    df.to_sql(
        "PropTemas",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
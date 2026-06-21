import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

DATABASE = BASE_DIR / "backend" / "database" / "camara.db"

CSV_DIR = (
    BASE_DIR
    / "dados_importacao"
    / "BDRTEST-2"
)

conn = sqlite3.connect(DATABASE)

anos = [2020, 2022, 2023, 2024, 2025, 2026]

for ano in anos:    

    print(f"Importando {ano}...")

    arquivo = CSV_DIR / f"proposicoesAutores-{ano}.csv"

    df = pd.read_csv(
        arquivo,
        sep=";",
        engine="python",
        on_bad_lines="skip"
    )

    df = df.rename(columns={

        "idProposicao": "id_proposicao",

        "idDeputadoAutor": "id_deputado",

        "codTipoAutor": "cod_tipo_autor",

        "tipoAutor": "tipo_autor",

        "ordemAssinatura": "ordem_assinatura",

        "proponente": "proponente"

    })

    colunas = [

        "id_proposicao",

        "id_deputado",

        "cod_tipo_autor",

        "tipo_autor",

        "ordem_assinatura",

        "proponente"

    ]

    df = df[colunas]

    print(f"{len(df)} registros")

    df.to_sql(
        "PropAutores",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
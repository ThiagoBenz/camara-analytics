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

for ano in range(2022, 2027):
    print(f"Importando {ano}...")

    arquivo = CSV_DIR / f"proposicoes-{ano}.csv"

    df = pd.read_csv(
    arquivo,
    sep=";",
    engine="python",
    quotechar='"',
    on_bad_lines="skip"
)   

    df = df.rename(columns={

        "id": "id_proposicao",

        "siglaTipo": "sigla_tipo_proposicao",

        "numero": "numero_proposicao",

        "ano": "ano_proposicao",

        "codTipo": "cod_tipo_proposicao",

        "descricaoTipo": "descricao_tipo_proposicao",

        "ementa": "ementa",

        "ementaDetalhada": "ementa_detalhada",

        "keywords": "keywords",

        "dataApresentacao": "data_apresentacao",

        "urlInteiroTeor": "url_inteiro_teor",

        "ultimoStatus_dataHora":
            "ultimo_status_data_hora",

        "ultimoStatus_descricaoTramitacao":
            "ultimo_status_descricao_tramitacao",

        "ultimoStatus_descricaoSituacao":
            "ultimo_status_descricao_situacao",

        "ultimoStatus_idSituacao":
            "ultimo_status_id_situacao",

        "ultimoStatus_regime":
            "ultimo_status_regime",

        "ultimoStatus_apreciacao":
            "ultimo_status_apreciacao"

    })

    colunas = [

        "id_proposicao",

        "sigla_tipo_proposicao",

        "numero_proposicao",

        "ano_proposicao",

        "cod_tipo_proposicao",

        "descricao_tipo_proposicao",

        "ementa",

        "ementa_detalhada",

        "keywords",

        "data_apresentacao",

        "url_inteiro_teor",

        "ultimo_status_data_hora",

        "ultimo_status_descricao_tramitacao",

        "ultimo_status_descricao_situacao",

        "ultimo_status_id_situacao",

        "ultimo_status_regime",

        "ultimo_status_apreciacao"

    ]

    df = df[colunas]

    df.to_sql(
        "Proposicoes",
        conn,
        if_exists="append",
        index=False
    )

    print(f"{len(df)} registros")

conn.close()

print("Concluído.")
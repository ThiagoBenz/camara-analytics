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

arquivos = sorted(CSV_DIR.glob("votacoes-*.csv"))

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

        "id": "id_votacao",

        "data": "data_votacao",

        "dataHoraRegistro":
            "dataHoraRegistro_votacao",

        "idEvento":
            "id_evento",

        "aprovacao":
            "aprovacao",

        "votosSim":
            "votosSim",

        "votosNao":
            "votosNao",

        "votosOutros":
            "votosOutros",

        "descricao":
            "descricao_votacao",

        "ultimaAberturaVotacao_dataHoraRegistro":
            "ultimaAberturaVotacao_dataHoraRegistro",

        "ultimaAberturaVotacao_descricao":
            "ultimaAberturaVotacao_descricao",

        "ultimaApresentacaoProposicao_dataHoraRegistro":
            "ultimaApresentacaoProposicao_dataHoraRegistro",

        "ultimaApresentacaoProposicao_descricao":
            "ultimaApresentacaoProposicao_descricao",

        "ultimaApresentacaoProposicao_idProposicao":
            "id_proposicao"

    })

    colunas = [

        "id_votacao",

        "data_votacao",

        "dataHoraRegistro_votacao",

        "id_evento",

        "aprovacao",

        "votosSim",

        "votosNao",

        "votosOutros",

        "descricao_votacao",

        "ultimaAberturaVotacao_dataHoraRegistro",

        "ultimaAberturaVotacao_descricao",

        "ultimaApresentacaoProposicao_dataHoraRegistro",

        "ultimaApresentacaoProposicao_descricao",

        "id_proposicao"

    ]

    df = df[colunas]

    # ==========================
    # Corrigir campos obrigatórios
    # ==========================

    df["aprovacao"] = (
        pd.to_numeric(
            df["aprovacao"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    df["votosSim"] = (
        pd.to_numeric(
            df["votosSim"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    df["votosNao"] = (
        pd.to_numeric(
            df["votosNao"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    df["votosOutros"] = (
        pd.to_numeric(
            df["votosOutros"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    df["id_evento"] = (
        pd.to_numeric(
            df["id_evento"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    df["id_proposicao"] = (
        pd.to_numeric(
            df["id_proposicao"],
            errors="coerce"
        )
    )

    print(f"{len(df)} registros")

    df.to_sql(
        "Votacao",
        conn,
        if_exists="append",
        index=False
    )

conn.close()

print("Concluído.")
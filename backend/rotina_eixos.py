#!/usr/bin/env python3
"""Rotina para carregar deputados e classificar eixos temáticos a partir das despesas.

Uso:
    .venv/bin/python rotina_eixos.py
    .venv/bin/python rotina_eixos.py --force
"""

from __future__ import annotations

import argparse
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

from eixos_mapping import EIXOS_KEYWORDS


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database" / "camara.db"
DEPUTADOS_SQL = BASE_DIR / "database" / "Deputados.sql"


DEPUTADOS_SCHEMA = """
CREATE TABLE IF NOT EXISTS Deputados (
    id_dep INTEGER NOT NULL PRIMARY KEY,
    uri_dep TEXT NOT NULL,
    nome_civil_dep TEXT NOT NULL,
    cpf_dep TEXT NOT NULL,
    sexo_dep TEXT NOT NULL,
    redeSocial_dep TEXT,
    data_nascimento_dep TEXT,
    escolaridade_dep TEXT,
    ultimoStatus_siglaPartido TEXT,
    ultimoStatus_siglaUf TEXT,
    ultimoStatus_situacao TEXT
)
"""


DEPUTADO_EIXO_SCHEMA = """
CREATE TABLE IF NOT EXISTS DeputyEixo (
    id_deputado INTEGER PRIMARY KEY,
    nome TEXT,
    partido TEXT,
    uf TEXT,
    eixo TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    total_gasto REAL NOT NULL DEFAULT 0
)
"""


def normalize(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\W+", " ", text.lower())


def ensure_columns(conn: sqlite3.Connection) -> None:
    existing = {row[1] for row in conn.execute("PRAGMA table_info(DeputyEixo)").fetchall()}
    required = {
        "nome": "TEXT",
        "partido": "TEXT",
        "uf": "TEXT",
        "eixo": "TEXT",
        "score": "INTEGER",
        "total_gasto": "REAL",
    }

    for column, column_type in required.items():
        if column not in existing:
            conn.execute(f"ALTER TABLE DeputyEixo ADD COLUMN {column} {column_type}")


def ensure_base_tables(conn: sqlite3.Connection) -> None:
    conn.execute(DEPUTADOS_SCHEMA)
    conn.execute(DEPUTADO_EIXO_SCHEMA)
    ensure_columns(conn)


def load_deputados(conn: sqlite3.Connection, force: bool = False) -> None:
    count = conn.execute("SELECT COUNT(*) FROM Deputados").fetchone()[0]
    if count > 0 and not force:
        return

    if not DEPUTADOS_SQL.exists():
        return

    conn.execute("DELETE FROM Deputados")
    conn.executescript(DEPUTADOS_SQL.read_text(encoding="utf-8"))
    conn.commit()


def keyword_score(text: str) -> dict[str, int]:
    normalized = normalize(text)
    scores: dict[str, int] = {}
    for eixo, keywords in EIXOS_KEYWORDS.items():
        total = 0
        for keyword in keywords:
            total += len(re.findall(r"\b" + re.escape(keyword.lower()) + r"\b", normalized))
        scores[eixo] = total
    return scores


def classify_from_despesas(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM DeputyEixo")

    expenses = conn.execute(
        """
        SELECT
            nuDeputadoId,
            txNomeParlamentar,
            sgPartido,
            sgUF,
            vlrLiquido,
            txtDescricao,
            txtDescricaoEspecificacao,
            txtFornecedor,
            txtPassageiro,
            txtTrecho
        FROM Despesas
        WHERE nuDeputadoId IS NOT NULL
        """
    ).fetchall()

    deputados: dict[int, dict[str, object]] = defaultdict(lambda: {
        "nome": "",
        "partido": "",
        "uf": "",
        "total_gasto": 0.0,
        "corpus_parts": [],
    })

    for row in expenses:
        deputado_id = int(row[0])
        data = deputados[deputado_id]
        data["nome"] = row[1] or data["nome"]
        data["partido"] = row[2] or data["partido"]
        data["uf"] = row[3] or data["uf"]
        data["total_gasto"] = float(data["total_gasto"]) + float(row[4] or 0)
        data["corpus_parts"].append(
            " ".join(part or "" for part in row[5:])
        )

    batch = []
    total = len(deputados)

    for index, (deputado_id, data) in enumerate(deputados.items(), start=1):
        corpus = " ".join(data["corpus_parts"])
        scores = keyword_score(corpus)
        eixo, score = max(scores.items(), key=lambda item: item[1])
        if score == 0:
            eixo = "Nao classificado"

        batch.append(
            (
                deputado_id,
                data["nome"],
                data["partido"],
                data["uf"],
                eixo,
                score,
                float(data["total_gasto"]),
            )
        )

        if len(batch) >= 100:
            conn.executemany(
                """
                INSERT OR REPLACE INTO DeputyEixo (id_deputado, nome, partido, uf, eixo, score, total_gasto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                batch,
            )
            conn.commit()
            print(f"Classificados {index}/{total} deputados...")
            batch.clear()

    if batch:
        conn.executemany(
            """
            INSERT OR REPLACE INTO DeputyEixo (id_deputado, nome, partido, uf, eixo, score, total_gasto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            batch,
        )
        conn.commit()

    print(f"Classificados {total}/{total} deputados.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerar rotina de eixos com base nas despesas")
    parser.add_argument("--force", action="store_true", help="Recarrega a tabela Deputados mesmo se já houver dados")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DATABASE))
    try:
        ensure_base_tables(conn)
        load_deputados(conn, force=args.force)
        classify_from_despesas(conn)
    finally:
        conn.close()

    print("Rotina de eixos concluida.")


if __name__ == "__main__":
    main()

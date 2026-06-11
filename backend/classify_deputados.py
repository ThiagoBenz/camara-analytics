#!/usr/bin/env python3
"""Script simples para classificar deputados por eixo temático baseado em palavras-chave.

Cria/atualiza tabela `DeputadoEixo(id_deputado INTEGER, eixo TEXT, score INTEGER)`
"""
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

from eixos_mapping import EIXOS_KEYWORDS, DEFAULT_TOP_N


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "camara.db"


def normalize(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\W+", " ", text.lower())


def tokenize(text: str):
    return [t for t in normalize(text).split() if t]


def classify():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Ensure table exists
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS DeputyEixo (
            id_deputado INTEGER PRIMARY KEY,
            eixo TEXT,
            score INTEGER
        )
        """
    )

    # Gather proposicoes per deputado
    cur.execute("SELECT DISTINCT id_deputado FROM PropAutores WHERE id_deputado IS NOT NULL")
    deputados = [r[0] for r in cur.fetchall()]

    eixo_keywords_lower = {e: [k.lower() for k in kw] for e, kw in EIXOS_KEYWORDS.items()}

    results = []

    for id_dep in deputados:
        # fetch proposicao ids for this deputy
        cur.execute("SELECT id_proposicao FROM PropAutores WHERE id_deputado = ?", (id_dep,))
        prop_ids = [r[0] for r in cur.fetchall() if r[0] is not None]

        text_parts = []
        for pid in prop_ids:
            cur.execute("SELECT ementa, ementa_detalhada, sigla_tipo_proposicao, numero_proposicao, ano_proposicao FROM Proposicoes WHERE id_proposicao = ?", (pid,))
            row = cur.fetchone()
            if not row:
                continue
            ementa = row[0] or ""
            detalhada = row[1] or ""
            text_parts.append(ementa)
            text_parts.append(detalhada)
            # try to load PropTemas for this proposicao
            sigla, numero, ano = row[2], row[3], row[4]
            if sigla is not None and numero is not None and ano is not None:
                cur.execute(
                    "SELECT tema FROM PropTemas WHERE sigla_tipo_proposicao = ? AND numero_proposicao = ? AND ano_proposicao = ?",
                    (sigla, numero, ano),
                )
                temas = [r[0] for r in cur.fetchall() if r[0]]
                text_parts.extend(temas)

        full_text = " ".join(text_parts)
        if not full_text.strip():
            continue

        counts = defaultdict(int)
        nf = normalize(full_text)

        # simple substring counting for each keyword
        for eixo, keywords in eixo_keywords_lower.items():
            total = 0
            for kw in keywords:
                total += len(re.findall(r"\b" + re.escape(kw) + r"\b", nf))
            counts[eixo] = total

        # pick best eixo
        best_eixo, best_score = None, 0
        for eixo, score in counts.items():
            if score > best_score:
                best_score = score
                best_eixo = eixo

        if best_eixo is None:
            continue

        results.append((id_dep, best_eixo, best_score))

    # write results
    cur.execute("DELETE FROM DeputyEixo")
    cur.executemany("INSERT OR REPLACE INTO DeputyEixo (id_deputado, eixo, score) VALUES (?, ?, ?)", results)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    classify()
    print("Classificação concluída.")

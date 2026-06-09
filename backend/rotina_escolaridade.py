#!/usr/bin/env python3
"""
Rotina para processar e classificar deputados federais por nível de escolaridade.
Associa os gastos totais a partir do CPF do deputado na tabela Despesas.

Uso:
    python3 rotina_escolaridade.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database" / "camara.db"

ESCOLARIDADE_SCHEMA = """
CREATE TABLE IF NOT EXISTS DeputyEscolaridade (
    id_deputado INTEGER PRIMARY KEY,
    nome TEXT,
    partido TEXT,
    uf TEXT,
    escolaridade_original TEXT,
    escolaridade_limpa TEXT,
    grupo_escolaridade TEXT NOT NULL,
    total_gasto REAL NOT NULL DEFAULT 0
)
"""

# Mapeamento para limpeza de strings (correção de encoding) e agrupamento
ESCOLARIDADE_MAP = {
    'Doutorado': ('Doutorado', 'Pós-Graduação'),
    'Doutorado Incompleto': ('Doutorado Incompleto', 'Pós-Graduação'),
    'Ensino Fundamental': ('Ensino Fundamental', 'Ensino Fundamental'),
    'Ensino MÃ©dio': ('Ensino Médio', 'Ensino Médio'),
    'Ensino MÃ©dio Incompleto': ('Ensino Médio Incompleto', 'Ensino Médio'),
    'Mestrado': ('Mestrado', 'Pós-Graduação'),
    'Mestrado Incompleto': ('Mestrado Incompleto', 'Pós-Graduação'),
    'PrimÃ¡rio Incompleto': ('Primário Incompleto', 'Ensino Fundamental'),
    'PÃ³s-GraduaÃ§Ã£o': ('Pós-Graduação', 'Pós-Graduação'),
    'SecundÃ¡rio': ('Secundário', 'Ensino Médio'),
    'SecundÃ¡rio Incompleto': ('Secundário Incompleto', 'Ensino Médio'),
    'Superior': ('Superior', 'Ensino Superior'),
    'Superior Incompleto': ('Superior Incompleto', 'Ensino Superior Incompleto'),
}


def normalize_cpf(cpf_val) -> str:
    """Normaliza o CPF vindo do banco de dados para string de 11 dígitos."""
    if cpf_val is None:
        return ""
    if isinstance(cpf_val, float):
        cpf_str = str(int(cpf_val))
    else:
        cpf_str = str(cpf_val).split('.')[0].strip()
    return cpf_str.zfill(11)


def clean_escolaridade(raw_value: str | None) -> tuple[str, str]:
    """Retorna (escolaridade_limpa, grupo_escolaridade)."""
    if not raw_value:
        return "Desconhecido", "Desconhecido"
    
    val = raw_value.strip()
    if val in ESCOLARIDADE_MAP:
        return ESCOLARIDADE_MAP[val]
    
    return val, "Outros"


def run() -> None:
    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("Criando tabela DeputyEscolaridade...")
    cur.execute(ESCOLARIDADE_SCHEMA)
    conn.commit()

    print("Carregando gastos agregados por CPF...")
    # Agrega os gastos na tabela Despesas usando o CPF normalizado
    expenses_query = "SELECT cpf, SUM(vlrLiquido) FROM Despesas WHERE cpf IS NOT NULL GROUP BY cpf"
    expenses_rows = cur.execute(expenses_query).fetchall()
    
    expenses_by_cpf = {}
    for row in expenses_rows:
        raw_cpf, total_gasto = row[0], row[1]
        norm_cpf = normalize_cpf(raw_cpf)
        if norm_cpf:
            expenses_by_cpf[norm_cpf] = float(total_gasto or 0)

    print("Carregando deputados da tabela Deputados...")
    deputados_query = """
        SELECT 
            id_dep, 
            nome_civil_dep, 
            cpf_dep, 
            escolaridade_dep, 
            ultimoStatus_siglaPartido, 
            ultimoStatus_siglaUf
        FROM Deputados
    """
    deputados_rows = cur.execute(deputados_query).fetchall()

    batch = []
    mapped_count = 0
    total_deputados = len(deputados_rows)

    for row in deputados_rows:
        id_dep = row['id_dep']
        nome = row['nome_civil_dep']
        cpf = normalize_cpf(row['cpf_dep'])
        esc_raw = row['escolaridade_dep']
        partido = row['ultimoStatus_siglaPartido']
        uf = row['ultimoStatus_siglaUf']

        # Limpeza e mapeamento
        esc_limpa, grupo = clean_escolaridade(esc_raw)

        # Associa gastos usando CPF
        total_gasto = expenses_by_cpf.get(cpf, 0.0)
        if cpf in expenses_by_cpf:
            mapped_count += 1

        batch.append((
            id_dep,
            nome,
            partido,
            uf,
            esc_raw,
            esc_limpa,
            grupo,
            total_gasto
        ))

    print(f"Salvando dados... (Gastos vinculados a {mapped_count}/{total_deputados} deputados via CPF)")
    
    cur.execute("DELETE FROM DeputyEscolaridade")
    cur.executemany(
        """
        INSERT OR REPLACE INTO DeputyEscolaridade (
            id_deputado, nome, partido, uf, escolaridade_original, escolaridade_limpa, grupo_escolaridade, total_gasto
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        batch
    )
    conn.commit()
    conn.close()

    print("Rotina finalizada com sucesso!")


if __name__ == "__main__":
    run()

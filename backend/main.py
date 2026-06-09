from fastapi import FastAPI
import sqlite3
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database" / "camara.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def home():
    return {"message": "API funcionando"}


@app.get("/deputados")
def listar_deputados():

    conn = get_connection()

    query = """
    SELECT DISTINCT txNomeParlamentar
    FROM Despesas
    WHERE txNomeParlamentar IS NOT NULL
    ORDER BY txNomeParlamentar
    """

    deputados = [dict(row) for row in conn.execute(query).fetchall()]

    conn.close()

    return deputados





@app.get("/ranking-gastos")
def ranking_gastos():

    conn = get_connection()

    cursor = conn.cursor()

   
    query = """
    SELECT
        txNomeParlamentar,
        MAX(sgPartido) AS sgPartido,
        MAX(sgUF) AS sgUF,
        SUM(vlrLiquido) AS total_gasto
    FROM Despesas
    GROUP BY txNomeParlamentar
    ORDER BY total_gasto DESC
    """

    cursor.execute(query)

    dados = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return dados





@app.get("/categorias-gastos")
def categorias_gastos():

    conn = get_connection()

    query = """
    SELECT
        txtDescricao,
        ROUND(SUM(vlrLiquido), 2) AS total_gasto
    FROM Despesas
    GROUP BY txtDescricao
    ORDER BY total_gasto DESC
    """

    resultado = conn.execute(query).fetchall()
    conn.close()

    return [dict(row) for row in resultado]





@app.get("/deputado-gastos/{nome}")
def gastos_deputado(nome: str):

    conn = get_connection()

    query = """
    SELECT
        txtDescricao,
        ROUND(SUM(vlrLiquido), 2) AS total_gasto
    FROM Despesas
    WHERE txNomeParlamentar = ?
    GROUP BY txtDescricao
    ORDER BY total_gasto DESC
    """

    gastos = [
        dict(row)
        for row in conn.execute(query, (nome,)).fetchall()
    ]

    conn.close()

    return gastos


@app.get("/eixos-deputados")
def eixos_deputados():
    """Retorna lista de deputados com eixo, score e dados agregados de despesas."""
    conn = get_connection()
    query = """
    SELECT
        de.id_deputado,
        de.nome,
        de.partido,
        de.uf,
        de.eixo,
        de.score,
        de.total_gasto
    FROM DeputyEixo de
    ORDER BY de.score DESC, de.total_gasto DESC
    """
    try:
        resultado = conn.execute(query).fetchall()
        return [dict(row) for row in resultado]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


@app.get("/eixos-resumo")
def eixos_resumo():
    """Retorna contagem de deputados por eixo."""
    conn = get_connection()
    query = """
    SELECT eixo, COUNT(*) AS total_deputados, COALESCE(SUM(score), 0) AS score_total, COALESCE(SUM(total_gasto), 0) AS gasto_total
    FROM DeputyEixo
    GROUP BY eixo
    ORDER BY total_deputados DESC, score_total DESC
    """
    try:
        resultado = conn.execute(query).fetchall()
        return [dict(row) for row in resultado]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


@app.get("/escolaridade-resumo")
def escolaridade_resumo():
    """Retorna contagem, gastos totais e médios por grupo de escolaridade."""
    conn = get_connection()
    query = """
    SELECT 
        grupo_escolaridade, 
        COUNT(*) AS total_deputados, 
        SUM(total_gasto) AS gasto_total, 
        AVG(total_gasto) AS gasto_medio
    FROM DeputyEscolaridade
    GROUP BY grupo_escolaridade
    ORDER BY total_deputados DESC
    """
    try:
        resultado = conn.execute(query).fetchall()
        return [dict(row) for row in resultado]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


@app.get("/escolaridade-deputados")
def escolaridade_deputados(grupo: str = None):
    """Retorna lista de deputados pertencentes a um grupo específico ou todos."""
    conn = get_connection()
    query = """
    SELECT 
        id_deputado, 
        nome, 
        partido, 
        uf, 
        escolaridade_original, 
        escolaridade_limpa, 
        grupo_escolaridade, 
        total_gasto
    FROM DeputyEscolaridade
    """
    params = []
    if grupo:
        query += " WHERE grupo_escolaridade = ?"
        params.append(grupo)
    query += " ORDER BY total_gasto DESC"
    try:
        resultado = conn.execute(query, params).fetchall()
        return [dict(row) for row in resultado]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


@app.get("/nuvem-palavras/{eixo}")
def nuvem_palavras(eixo: str, top: int = 50):
    """Gera nuvem simples (top palavras) para o eixo informado com base nas despesas dos deputados classificados.
    Retorna JSON: [{"word": ..., "count": ...}, ...]
    """
    import re
    from collections import Counter

    conn = get_connection()

    # coletar despesas relacionadas aos deputados marcados com esse eixo
    sql = """
    SELECT d.txtDescricao, d.txtDescricaoEspecificacao, d.txtFornecedor, d.txtPassageiro, d.txtTrecho
    FROM Despesas d
    JOIN DeputyEixo de ON de.id_deputado = d.nuDeputadoId
    WHERE de.eixo = ?
    """

    texts = []
    try:
        for row in conn.execute(sql, (eixo,)).fetchall():
            texts.append(" ".join([row[0] or "", row[1] or "", row[2] or "", row[3] or "", row[4] or ""]))
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()

    if not texts:
        return []

    combined = " ".join(texts).lower()
    words = re.findall(r"\b[\wà-ú]+\b", combined)
    stopwords = set(["de", "da", "do", "e", "o", "a", "dos", "das", "para", "com", "em", "por", "na", "no"])
    filtered = [w for w in words if w not in stopwords and len(w) > 2]

    counts = Counter(filtered).most_common(top)

    return [{"word": w, "count": c} for w, c in counts]


@app.get("/teste")
def teste():

    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row

    query = """
    SELECT * FROM Despesas LIMIT 1
    """

    resultado = conn.execute(query).fetchall()

    dados = [dict(row) for row in resultado]

    conn.close()

    return dados


@app.get("/correlacao-fornecedor-deputado/{nome}")
def deputado_fornecedores(nome: str):

    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        txtFornecedor,
        txtCNPJCPF,
        ROUND(SUM(vlrLiquido), 2) AS total_gasto
    FROM Despesas
    WHERE txNomeParlamentar = ?
      AND txtFornecedor IS NOT NULL
      AND txtFornecedor <> ''
    GROUP BY txtFornecedor, txtCNPJCPF
    ORDER BY total_gasto DESC
    """

    resultado = conn.execute(query, (nome,)).fetchall()

    conn.close()

    return [dict(row) for row in resultado]

from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATABASE = "database/camara.db"


@app.get("/")
def home():
    return {"message": "API funcionando"}


@app.get("/deputados")
def listar_deputados():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

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

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

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

    conn = sqlite3.connect("database/camara.db")
    conn.row_factory = sqlite3.Row

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

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

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





@app.get("/teste")
def teste():

    conn = sqlite3.connect(DATABASE)
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

    conn = sqlite3.connect(DATABASE)
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





    
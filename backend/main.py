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





@app.get("/dashboard")
def dashboard():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        (SELECT COUNT(DISTINCT txNomeParlamentar)
         FROM Despesas) AS total_deputados,

        (SELECT COUNT(DISTINCT sgPartido)
         FROM Despesas
         WHERE sgPartido IS NOT NULL) AS total_partidos,

        (SELECT COUNT(DISTINCT txtFornecedor)
         FROM Despesas
         WHERE txtFornecedor IS NOT NULL
           AND txtFornecedor <> '') AS total_fornecedores,

        (SELECT ROUND(SUM(vlrLiquido), 2)
         FROM Despesas) AS total_despesas
    """

    resultado = conn.execute(query).fetchone()

    conn.close()

    return dict(resultado)




# RETORNA O DEPUTADO COM MAIS GASTOS E O PARTIDO COM MAIS GASTOS
@app.get("/dashboard-destaques")
def dashboard_destaques():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    deputado_query = """
    SELECT
        txNomeParlamentar,
        sgPartido,
        ROUND(SUM(vlrLiquido), 2) AS total_gasto
    FROM Despesas
    WHERE txNomeParlamentar IS NOT NULL
    GROUP BY txNomeParlamentar, sgPartido
    ORDER BY total_gasto DESC
    LIMIT 1
    """

    partido_query = """
    SELECT
        sgPartido,
        ROUND(SUM(vlrLiquido), 2) AS total_gasto
    FROM Despesas
    WHERE sgPartido IS NOT NULL
    GROUP BY sgPartido
    ORDER BY total_gasto DESC
    LIMIT 1
    """

    deputado = conn.execute(deputado_query).fetchone()
    partido = conn.execute(partido_query).fetchone()

    conn.close()

    return {
        "deputado": dict(deputado),
        "partido": dict(partido)
    }





# RETORNA DADOS DOS FORNECEDORES MAIS USADOS POR DEPUTADOS FEDERAIS
@app.get("/dashboard-fornecedores")
def dashboard_fornecedores():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    maior_recebedor_query = """
    SELECT
        txtFornecedor,
        txtCNPJCPF,
        ROUND(SUM(vlrLiquido), 2) AS total_recebido
    FROM Despesas
    WHERE txtFornecedor IS NOT NULL
      AND txtFornecedor <> ''
    GROUP BY txtFornecedor, txtCNPJCPF
    ORDER BY total_recebido DESC
    LIMIT 1
    """

    mais_utilizado_query = """
    SELECT
        txtFornecedor,
        txtCNPJCPF,
        COUNT(DISTINCT txNomeParlamentar) AS deputados
    FROM Despesas
    WHERE txtFornecedor IS NOT NULL
      AND txtFornecedor <> ''
    GROUP BY txtFornecedor, txtCNPJCPF
    ORDER BY deputados DESC
    LIMIT 1
    """

    top5_query = """
    SELECT
        txtFornecedor,
        ROUND(SUM(vlrLiquido), 2) AS total_recebido
    FROM Despesas
    WHERE txtFornecedor IS NOT NULL
      AND txtFornecedor <> ''
    GROUP BY txtFornecedor
    ORDER BY total_recebido DESC
    LIMIT 5
    """

    maior_recebedor = conn.execute(maior_recebedor_query).fetchone()
    mais_utilizado = conn.execute(mais_utilizado_query).fetchone()
    top5 = conn.execute(top5_query).fetchall()

    conn.close()

    return {
        "maior_recebedor": dict(maior_recebedor),
        "mais_utilizado": dict(mais_utilizado),
        "top5": [dict(row) for row in top5]
    }




    
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

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Deputados LIMIT 20")

    deputados = [dict(row) for row in cursor.fetchall()]

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


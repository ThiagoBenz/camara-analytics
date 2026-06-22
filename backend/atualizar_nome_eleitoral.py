import pandas as pd
import sqlite3

DATABASE = "backend/database/camara.db"

ARQUIVO = (
    "dados_importacao/BDRTEST-2/"
    "deputados_completo_api_legis57.csv"
)

conn = sqlite3.connect(DATABASE)

df = pd.read_csv(

    ARQUIVO,

    sep=";",

    encoding="utf-8",

    low_memory=False

)

for _, linha in df.iterrows():

    conn.execute(

        """

        UPDATE Deputados

        SET nome_eleitoral_dep = ?

        WHERE id_dep = ?

        """,

        (

            linha["ultimoStatus.nomeEleitoral"],

            linha["id"]

        )

    )

conn.commit()

conn.close()

print("Nome eleitoral atualizado.")
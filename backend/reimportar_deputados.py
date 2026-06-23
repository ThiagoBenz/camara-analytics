import pandas as pd
import sqlite3

DATABASE = "backend/database/camara.db"

ARQUIVO = (
    "dados_importacao/BDRTEST-2/"
    "deputados_completo_api_legis57.csv"
)

conn = sqlite3.connect(DATABASE)

# =====================
# Ler CSV
# =====================

df = pd.read_csv(

    ARQUIVO,

    sep=";",

    encoding="utf-8",

    low_memory=False

)

# =====================
# Renomear colunas
# =====================

df = df.rename(

    columns={

        "id": "id_dep",

        "uri": "uri_dep",

        "nomeCivil": "nome_civil_dep",

        "cpf": "cpf_dep",

        "sexo": "sexo_dep",

        "redeSocial": "redeSocial_dep",

        "dataNascimento": "data_nascimento_dep",

        "escolaridade": "escolaridade_dep",

        "ultimoStatus.siglaPartido":

            "ultimoStatus_siglaPartido",

        "ultimoStatus.siglaUf":

            "ultimoStatus_siglaUf",

        "ultimoStatus.situacao":

            "ultimoStatus_situacao"

    }

)

# =====================
# Manter somente
# as colunas usadas
# =====================

df = df[[

    "id_dep",

    "uri_dep",

    "nome_civil_dep",

    "cpf_dep",

    "sexo_dep",

    "redeSocial_dep",

    "data_nascimento_dep",

    "escolaridade_dep",

    "ultimoStatus_siglaPartido",

    "ultimoStatus_siglaUf",

    "ultimoStatus_situacao"

]]

# =====================
# Inserir no banco
# =====================

df.to_sql(

    "Deputados",

    conn,

    if_exists="append",

    index=False

)

conn.close()

print("601 deputados importados.")
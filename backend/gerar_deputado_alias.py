import sqlite3
import pandas as pd

from difflib import SequenceMatcher


DATABASE = "backend/database/camara.db"


# ======================================
# Conexão
# ======================================

conn = sqlite3.connect(DATABASE)


# ======================================
# Deputados
# ======================================

deputados = pd.read_sql("""

SELECT

    id_dep,

    nome_civil_dep

FROM Deputados

ORDER BY nome_civil_dep

""", conn)


# ======================================
# Nomes parlamentares
# ======================================

parlamentares = pd.read_sql("""

SELECT DISTINCT

    txNomeParlamentar

FROM Despesas

WHERE

    txNomeParlamentar NOT LIKE 'LID.%'

ORDER BY txNomeParlamentar

""", conn)


# ======================================
# Lista de resultados
# ======================================

alias = []


# ======================================
# Função auxiliar
# ======================================

def limpar_nome(nome):

    ignorar = {

        "DA",

        "DE",

        "DO",

        "DAS",

        "DOS",

        "E"

    }

    palavras = [

        p.upper()

        for p in nome.split()

        if p.upper() not in ignorar

    ]

    return palavras


# ======================================
# Geração automática
# ======================================

for _, dep in deputados.iterrows():

    nome_civil = dep["nome_civil_dep"]

    palavras_civil = limpar_nome(nome_civil)

    primeiro_civil = palavras_civil[0]

    ultimo_civil = palavras_civil[-1]

    melhor_nome = None

    melhor_score = 0


    for parlamentar in parlamentares["txNomeParlamentar"]:

        palavras_parlamentar = limpar_nome(parlamentar)

        primeiro_parlamentar = palavras_parlamentar[0]

        # ==========================
        # Regra 1
        # Primeiro nome obrigatório
        # ==========================

        if primeiro_civil != primeiro_parlamentar:

            continue


        score = SequenceMatcher(

            None,

            nome_civil.upper(),

            parlamentar.upper()

        ).ratio()


        # ==========================
        # Regra 2
        # Bônus se sobrenome bater
        # ==========================

        if ultimo_civil in parlamentar.upper():

            score += 0.15


        if score > melhor_score:

            melhor_score = score

            melhor_nome = parlamentar


    # ==========================
    # Regra 3
    # Confiança mínima
    # ==========================

    if melhor_score >= 0.70:

        alias.append({

            "id_dep":

            dep["id_dep"],

            "nome_civil":

            nome_civil,

            "nome_parlamentar":

            melhor_nome,

            "confianca":

            round(

                min(

                    melhor_score,

                    1

                ) * 100,

                2

            )

        })


# ======================================
# DataFrame
# ======================================

alias = pd.DataFrame(alias)


# ======================================
# Remover duplicados
# ======================================

alias = alias.drop_duplicates()


# ======================================
# Salvar tabela
# ======================================

alias.to_sql(

    "DeputadoAlias",

    conn,

    if_exists="replace",

    index=False

)


conn.close()


print(

    f"{len(alias)} deputados associados."

)
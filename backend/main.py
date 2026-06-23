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

TIPOS_EVENTO_RELEVANTES = [
    "Reunião Deliberativa",
    "Sessão Deliberativa",
    "Audiência Pública e Deliberação",
    "Reunião de Instalação e Eleição",
    "Reunião de Comparecimento de Ministro(a)",
]

SITUACOES_ENCERRADAS = [
    "Encerrada",
    "Encerrada (Final)",
    "Encerrada (Termo)",
]

PESO_PROPOSICOES = 0.70
PESO_PRESENCA    = 0.30


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


@app.get("/fornecedores-ranking")
def fornecedores_ranking(busca: str = None, limit: int = 100, offset: int = 0):
    """Retorna o ranking de fornecedores com base no somatório do volume financeiro."""
    conn = get_connection()
    query = """
    SELECT 
        txtCNPJCPF AS cnpj_cpf, 
        txtFornecedor AS nome_fornecedor, 
        SUM(vlrLiquido) AS total_recebido,
        COUNT(*) AS qtd_despesas
    FROM Despesas
    WHERE txtCNPJCPF IS NOT NULL AND txtCNPJCPF != ''
    """
    params = []
    if busca:
        query += " AND (txtFornecedor LIKE ? OR txtCNPJCPF LIKE ?)"
        params.extend([f"%{busca}%", f"%{busca}%"])
    
    query += """
    GROUP BY txtCNPJCPF
    ORDER BY total_recebido DESC
    LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    
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





#respondendo questao 11
@app.get("/panorama-partidos-destaques")
def panorama_partidos_destaques():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    maior_gastador = conn.execute("""
        SELECT
            sgPartido AS partido,
            ROUND(SUM(vlrLiquido), 2) AS valor
        FROM Despesas
        WHERE sgPartido IS NOT NULL
          AND sgPartido <> ''
        GROUP BY sgPartido
        ORDER BY valor DESC
        LIMIT 1
    """).fetchone()

    mais_proposicoes = conn.execute("""
        SELECT
            d.ultimoStatus_siglaPartido AS partido,
            COUNT(*) AS valor
        FROM PropAutores pa
        JOIN Deputados d
            ON pa.id_deputado = d.id_dep
        WHERE d.ultimoStatus_siglaPartido IS NOT NULL
          AND d.ultimoStatus_siglaPartido <> ''
        GROUP BY d.ultimoStatus_siglaPartido
        ORDER BY valor DESC
        LIMIT 1
    """).fetchone()

    maior_bancada = conn.execute("""
        SELECT
            ultimoStatus_siglaPartido AS partido,
            COUNT(*) AS valor
        FROM Deputados
        WHERE ultimoStatus_siglaPartido IS NOT NULL
          AND ultimoStatus_siglaPartido <> ''
        GROUP BY ultimoStatus_siglaPartido
        ORDER BY valor DESC
        LIMIT 1
    """).fetchone()

    conn.close()

    return {
        "maior_gastador": dict(maior_gastador),
        "mais_proposicoes": dict(mais_proposicoes),
        "maior_bancada": dict(maior_bancada)
    }

##############################################
@app.get("/panorama-partidos-frequencia")
def panorama_partidos_frequencia():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        sgPartido AS partido,
        COUNT(*) AS valor
    FROM Despesas
    WHERE sgPartido IS NOT NULL
      AND sgPartido <> ''
    GROUP BY sgPartido
    ORDER BY valor DESC
    """

    resultado = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in resultado]

##############################################
@app.get("/panorama-partidos-proposicoes")
def panorama_partidos_proposicoes():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        d.ultimoStatus_siglaPartido AS partido,
        COUNT(*) AS valor
    FROM PropAutores pa
    JOIN Deputados d
        ON pa.id_deputado = d.id_dep
    WHERE d.ultimoStatus_siglaPartido IS NOT NULL
      AND d.ultimoStatus_siglaPartido <> ''
    GROUP BY d.ultimoStatus_siglaPartido
    ORDER BY valor DESC
    """

    resultado = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in resultado]

  ##############################################
@app.get("/panorama-partidos-gastos")
def panorama_partidos_gastos():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        sgPartido AS partido,
        ROUND(SUM(vlrLiquido), 2) AS valor
    FROM Despesas
    WHERE sgPartido IS NOT NULL
      AND sgPartido <> ''
    GROUP BY sgPartido
    ORDER BY valor DESC
    """

    resultado = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in resultado]

##############################################
@app.get("/panorama-partidos-nuvem-palavras")
def panorama_partidos_nuvem_palavras():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        tema,
        COUNT(*) AS valor
    FROM PropTemas
    WHERE tema IS NOT NULL
      AND tema <> ''
    GROUP BY tema
    ORDER BY valor DESC
    LIMIT 50
    """

    resultado = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in resultado]



#################################################
#################################################
import math


@app.get("/custo-beneficio")
def custo_beneficio():

    conn = get_connection()

    # ==========================================
    # GASTOS
    # ==========================================

    sql_gastos = """
    SELECT

        d.id_dep,

        d.nome_civil_dep,

        d.nome_eleitoral_dep,

        d.ultimoStatus_siglaPartido,

        COALESCE(
            SUM(g.vlrLiquido),
            0
        ) AS gasto_total

    FROM Deputados d

    LEFT JOIN Despesas g

        ON d.nome_eleitoral_dep = g.txNomeParlamentar

    GROUP BY

        d.id_dep,

        d.nome_civil_dep,

        d.nome_eleitoral_dep,

        d.ultimoStatus_siglaPartido
    """

    rows_gastos = conn.execute(
        sql_gastos
    ).fetchall()

    # ==========================================
    # PROPOSIÇÕES
    # ==========================================

    sql_prop = """
    SELECT

        id_deputado,

        COUNT(
            DISTINCT id_proposicao
        ) AS total_proposicoes

    FROM PropAutores

    GROUP BY id_deputado
    """

    prop_map = {

        r["id_deputado"]:

        r["total_proposicoes"]

        for r in conn.execute(
            sql_prop
        ).fetchall()

    }

    # ==========================================
    # PRESENÇAS
    # ==========================================

    tipos_ph = ",".join(

        "?" * len(
            TIPOS_EVENTO_RELEVANTES
        )

    )

    situacoes_ph = ",".join(

        "?" * len(
            SITUACOES_ENCERRADAS
        )

    )

    parametros = (

        TIPOS_EVENTO_RELEVANTES

        +

        SITUACOES_ENCERRADAS

    )

    sql_pres = f"""
    SELECT

        pd.id_deputado,

        COUNT(
            DISTINCT pd.id_evento
        ) AS total_presencas

    FROM PresencaDeputados pd

    INNER JOIN Eventos e

        ON pd.id_evento = e.id_evento

    WHERE

        e.tipo_evento IN ({tipos_ph})

    AND

        e.situacao_evento IN ({situacoes_ph})

    GROUP BY

        pd.id_deputado
    """

    pres_map = {

        r["id_deputado"]:

        r["total_presencas"]

        for r in conn.execute(

            sql_pres,

            parametros

        ).fetchall()

    }

    conn.close()

    # ==========================================
    # CONSOLIDAÇÃO
    # ==========================================

    deputados = []

    for row in rows_gastos:

        deputados.append({

            "id_dep":

            row["id_dep"],

            "nome_civil_dep":

            row["nome_civil_dep"],

            "nome_eleitoral_dep":

            row["nome_eleitoral_dep"],

            "ultimoStatus_siglaPartido":

            row["ultimoStatus_siglaPartido"],

            "gasto_total":

            float(

                row["gasto_total"]

            ),

            "total_proposicoes":

            prop_map.get(

                row["id_dep"],

                0

            ),

            "total_presencas":

            pres_map.get(

                row["id_dep"],

                0

            )

        })

    # ==========================================
    # NORMALIZAÇÃO
    # ==========================================

    max_log_prop = math.log(

        max(

            d["total_proposicoes"]

            for d in deputados

        ) + 1

    )

    max_pres = max(

        d["total_presencas"]

        for d in deputados

    ) or 1

    max_log_gasto = math.log(

        max(

            d["gasto_total"]

            for d in deputados

        ) + 1

    )

    # ==========================================
    # CÁLCULO
    # ==========================================

    for d in deputados:

        log_prop = math.log(

            d["total_proposicoes"]

            + 1

        )

        log_gasto = math.log(

            d["gasto_total"]

            + 1

        )

        nota_prop = (

            log_prop

            /

            max_log_prop

        ) * 10

        nota_pres = (

            math.sqrt(

                d["total_presencas"]

            )

            /

            math.sqrt(

                max_pres

            )

        ) * 10

        nota_gasto = (

            log_gasto

            /

            max_log_gasto

        ) * 10

        beneficio = (

            PESO_PROPOSICOES

            * nota_prop

        ) + (

            PESO_PRESENCA

            * nota_pres

        )

        eficiencia_gasto = (

            10

            - nota_gasto

        )

        indice = (

            0.80

            * beneficio

        ) + (

            0.20

            * eficiencia_gasto

        )

        presenca_relativa = (

            math.sqrt(

                d["total_presencas"]

            )

            /

            math.sqrt(

                max_pres

            )

        ) * 100

        d["presenca_relativa"] = round(

            presenca_relativa,

            1

        )

        d["beneficio"] = round(

            beneficio,

            2

        )

        d["indice"] = round(

            indice,

            2

        )

    # ==========================================
    # ORDENAÇÃO
    # ==========================================

    deputados.sort(

        key=lambda x:

        x["indice"],

        reverse=True

    )

    # ==========================================
    # RETORNO
    # ==========================================

    resultado = []

    for i, d in enumerate(

        deputados,

        start=1

    ):

        resultado.append({

            "ranking":

            i,

            "id_dep":

            d["id_dep"],

            "nome_civil_dep":

            d["nome_civil_dep"],

            "nome_eleitoral_dep":

            d["nome_eleitoral_dep"],

            "ultimoStatus_siglaPartido":

            d["ultimoStatus_siglaPartido"],

            "gasto_total":

            round(

                d["gasto_total"],

                2

            ),

            "total_proposicoes":

            d["total_proposicoes"],

            "presenca_relativa":

            d["presenca_relativa"],

            "beneficio":

            d["beneficio"],

            "indice":

            d["indice"]

        })

    return resultado





    ###################################################################
@app.get("/vies-politico")
def vies_politico():

    conn = get_connection()

    # ==========================================
    # CONSTANTES
    # ==========================================

    PARTIDOS = {

        "PT": -1,
        "PSOL": -1,
        "PCdoB": -1,
        "REDE": -1,

        "PDT": -0.5,
        "PSB": -0.5,

        "MDB": 0,
        "PSD": 0,
        "UNIÃO": 0,
        "CIDADANIA": 0,
        "AVANTE": 0,
        "SOLIDARIEDADE": 0,

        "PODE": 0.5,
        "REPUBLICANOS": 0.5,

        "PP": 1,
        "PL": 1,
        "NOVO": 1

    }

    TEMAS_DIREITA = [

        "Defesa e Segurança",

        "Economia",

        "Finanças Públicas e Orçamento",

        "Agricultura, Pecuária, Pesca e Extrativismo",

        "Indústria, Comércio e Serviços",

        "Estrutura Fundiária"

    ]

    TEMAS_ESQUERDA = [

        "Direitos Humanos e Minorias",

        "Educação",

        "Saúde",

        "Previdência e Assistência Social",

        "Trabalho e Emprego",

        "Meio Ambiente e Desenvolvimento Sustentável"

    ]

    def nota_tema(tema):

        if not tema:

            return 0

        if tema in TEMAS_DIREITA:

            return 1

        if tema in TEMAS_ESQUERDA:

            return -1

        return 0

    # ==========================================
    # DEPUTADOS EM EXERCÍCIO
    # ==========================================

    sql_dep = """

    SELECT

        id_dep,

        nome_eleitoral_dep,

        ultimoStatus_siglaPartido,

        ultimoStatus_siglaUf

    FROM Deputados

    WHERE

        ultimoStatus_situacao='Exercício'

    """

    deputados = {}

    for row in conn.execute(

        sql_dep

    ).fetchall():

        deputados[

            row["id_dep"]

        ] = {

            "id_dep":

            row["id_dep"],

            "nome":

            row["nome_eleitoral_dep"],

            "partido":

            (

                row["ultimoStatus_siglaPartido"]

                or ""

            ).upper(),

            "uf":

            row["ultimoStatus_siglaUf"],

            "temas": [],

            "votos_validos": 0,

            "votos_alinhados": 0

        }

    # ==========================================
    # PROPOSIÇÕES
    # ==========================================

    sql_prop = """

    SELECT

        pa.id_deputado,

        pt.tema

    FROM PropAutores pa

    INNER JOIN Proposicoes p

        ON pa.id_proposicao = p.id_proposicao

    INNER JOIN PropTemas pt

        ON p.sigla_tipo_proposicao = pt.sigla_tipo_proposicao

        AND

        p.numero_proposicao = pt.numero_proposicao

        AND

        p.ano_proposicao = pt.ano_proposicao

    """

    for row in conn.execute(

        sql_prop

    ).fetchall():

        id_dep = row["id_deputado"]

        if id_dep in deputados:

            if row["tema"]:

                deputados[id_dep]["temas"].append(

                    row["tema"]

                )

    # ==========================================
    # ORIENTAÇÕES
    # ==========================================

    sql_orientacoes = """

    SELECT

        id_votacao,

        siglaBancada,

        orientacao

    FROM VotOrientacoes

    WHERE

        orientacao IN (

            'Sim',

            'Não'

        )

    """

    orientacoes = {}

    for row in conn.execute(

        sql_orientacoes

    ).fetchall():

        chave = (

            row["id_votacao"],

            row["siglaBancada"].upper()

        )

        orientacoes[

            chave

        ] = row["orientacao"]

    # ==========================================
    # VOTOS
    # ==========================================

    sql_votos = """

    SELECT

        id_votacao,

        id_deputado,

        voto

    FROM VotVotos

    WHERE

        voto IN (

            'Sim',

            'Não'

        )

    """

    for row in conn.execute(

        sql_votos

    ).fetchall():

        id_dep = row["id_deputado"]

        if id_dep not in deputados:

            continue

        partido = deputados[

            id_dep

        ]["partido"]

        chave = (

            row["id_votacao"],

            partido

        )

        if chave not in orientacoes:

            continue

        deputados[id_dep][

            "votos_validos"

        ] += 1

        if row["voto"] == orientacoes[chave]:

            deputados[id_dep][

                "votos_alinhados"

            ] += 1

    conn.close()

    # ==========================================
    # CONSOLIDAÇÃO
    # ==========================================

    esquerda = 0

    centro = 0

    direita = 0

    resultado_deputados = []

    partidos = {}

    for dep in deputados.values():

        # ====================
        # PARTIDO
        # ====================

        nota_partido = PARTIDOS.get(

            dep["partido"],

            0

        )

        # ====================
        # TEMAS
        # ====================

        temas_direita = 0

        temas_esquerda = 0

        for tema in dep["temas"]:

            nota = nota_tema(

                tema

            )

            if nota == 1:

                temas_direita += 1

            elif nota == -1:

                temas_esquerda += 1

        total_ideologico = (

            temas_direita

            +

            temas_esquerda

        )

        if total_ideologico:

            nota_temas = (

                temas_direita

                -

                temas_esquerda

            ) / total_ideologico

        else:

            nota_temas = 0

        # ====================
        # VOTAÇÕES
        # ====================

        if dep["votos_validos"]:

            perc = (

                dep["votos_alinhados"]

                /

                dep["votos_validos"]

            )

            nota_votos = (

                perc * 2

            ) - 1

        else:

            nota_votos = 0

        # ====================
        # ÍNDICE
        # ====================

        indice = (

            0.10

            * nota_partido

        ) + (

            0.80

            * nota_temas

        ) + (

            0.10

            * nota_votos

        )

        # ====================
        # CLASSIFICAÇÃO
        # ====================

        if indice <= -0.20:

            tendencia = "Esquerda"

            esquerda += 1

        elif indice >= 0.20:

            tendencia = "Direita"

            direita += 1

        else:

            tendencia = "Centro"

            centro += 1

        # ====================
        # TEMA PREDOMINANTE
        # ====================

        tema_predominante = "-"

        if dep["temas"]:

            tema_predominante = max(

                set(

                    dep["temas"]

                ),

                key=dep["temas"].count

            )

        # ====================
        # AGRUPAMENTO PARTIDOS
        # ====================

        partido = dep["partido"]

        if partido not in partidos:

            partidos[partido] = {

                "partido":

                partido,

                "total_deputados": 0,

                "indices": [],

                "temas": []

            }

        partidos[partido][

            "total_deputados"

        ] += 1

        partidos[partido][

            "indices"

        ].append(

            indice

        )

        if tema_predominante != "-":

            partidos[partido][

                "temas"

            ].append(

                tema_predominante

            )

        resultado_deputados.append({

            "id_dep":

            dep["id_dep"],

            "nome":

            dep["nome"],

            "partido":

            partido,

            "uf":

            dep["uf"],

            "tema_predominante":

            tema_predominante,

            "alinhamento_votos":

            round(

                (

                    dep["votos_alinhados"]

                    /

                    dep["votos_validos"]

                    * 100

                )

                if dep["votos_validos"]

                else 0,

                1

            ),

            "indice":

            round(

                indice,

                2

            ),

            "tendencia":

            tendencia

        })

    # ==========================================
    # PARTIDOS
    # ==========================================

    resultado_partidos = []

    for p in partidos.values():

        media = (

            sum(

                p["indices"]

            )

            /

            len(

                p["indices"]

            )

        )

        classificacao = "Centro"

        if media <= -0.20:

            classificacao = "Esquerda"

        elif media >= 0.20:

            classificacao = "Direita"

        tema = "-"

        if p["temas"]:

            tema = max(

                set(

                    p["temas"]

                ),

                key=p["temas"].count

            )

        resultado_partidos.append({

            "partido":

            p["partido"],

            "classificacao":

            classificacao,

            "total_deputados":

            p["total_deputados"],

            "tema_predominante":

            tema

        })

    resultado_deputados.sort(

        key=lambda x:

        x["indice"],

        reverse=True

    )

    return {

        "cards": {

            "esquerda":

            esquerda,

            "centro":

            centro,

            "direita":

            direita

        },

        "grafico": [

            {

                "grupo":

                "Esquerda",

                "quantidade":

                esquerda

            },

            {

                "grupo":

                "Centro",

                "quantidade":

                centro

            },

            {

                "grupo":

                "Direita",

                "quantidade":

                direita

            }

        ],

        "partidos":

        resultado_partidos,

        "deputados":

        resultado_deputados

    }
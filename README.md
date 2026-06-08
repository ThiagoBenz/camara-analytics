# Câmara Analytics

Sistema de análise de dados parlamentares desenvolvido para a disciplina de Banco de Dados Relacional da Universidade Federal do Piauí (UFPI).

O projeto utiliza dados públicos da Câmara dos Deputados para realizar consultas, análises e visualizações relacionadas à atividade parlamentar brasileira, incluindo gastos, votações, proposições legislativas, partidos políticos e presença parlamentar.

---

## Objetivo

O Câmara Analytics tem como objetivo transformar dados públicos da Câmara dos Deputados em informações acessíveis por meio de consultas, rankings e indicadores analíticos.

O sistema permite explorar dados em diferentes escopos:

- Nacional
- Estadual (UF)
- Partidário

---

## Tecnologias Utilizadas

### Frontend

- Angular
- Angular Material
- TypeScript
- HTML5
- CSS3

### Backend

- Python
- FastAPI
- Uvicorn

### Banco de Dados

- SQLite

### Manipulação de Dados

- Pandas

### Fonte dos Dados

- Dados Abertos da Câmara dos Deputados
- Arquivos CSV contendo despesas parlamentares
- Base de dados legislativa convertida do Microsoft Access (.accdb)

---

## Funcionalidades

### Implementadas

- Ranking de deputados por gastos parlamentares
- Integração Angular + FastAPI
- Consulta de despesas parlamentares
- API REST para consumo dos dados
- Banco de dados SQLite

### Em Desenvolvimento

- Agrupamento por partido
- Agrupamento por estado
- Nuvem de palavras por eixo temático
- Análise de votações parlamentares
- Correlação entre escolaridade e desempenho parlamentar
- Indicador de custo-benefício parlamentar
- Indicador de influência legislativa
- Ranking de fornecedores
- Correlação deputado × fornecedor
- Análise das categorias de despesas

---

## Estrutura do Projeto

```text
camara-analytics/
│
├── backend/
│   ├── database/
│   │   ├── csv/
│   │   ├── schema.sql
│   │   └── *.sql
│   │
│   ├── main.py
│   ├── import_csv.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── angular.json
│   ├── package.json
│   └── package-lock.json
│
└── README.md
```

---

## Requisitos

### Backend

- Python 3.11 ou superior
- pip

### Frontend

- Node.js 20 ou superior
- npm
- Angular CLI

---

# Instalação

## 1. Clonar o projeto

```bash
git clone git@github.com:SEU_USUARIO/camara-analytics.git

cd camara-analytics
```

---

## 2. Configurar Backend

Entrar na pasta:

```bash
cd backend
```

Criar ambiente virtual:

### Linux / macOS

```bash
python3 -m venv venv
```

Ativar ambiente:

```bash
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

---

## 3. Gerar Banco de Dados SQLite

Caso o banco ainda não exista:

```bash
python import_csv.py
```

Esse script importa os arquivos CSV e cria/popula o banco SQLite.

### Rotina de eixos

Para carregar a tabela de deputados e classificar os eixos temáticos a partir das despesas:

```bash
python backend/rotina_eixos.py
```

Se quiser recarregar a tabela de deputados do arquivo SQL:

```bash
python backend/rotina_eixos.py --force
```

---

## 4. Iniciar Backend

```bash
uvicorn main:app --reload
```

API disponível em:

```text
http://127.0.0.1:8000
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Configurar Frontend

Abrir outro terminal.

Entrar na pasta:

```bash
cd frontend
```

Instalar dependências:

```bash
npm install
```

---

## 6. Iniciar Frontend

```bash
ng serve
```

Aplicação disponível em:

```text
http://localhost:4200
```

---

## Fluxo de Desenvolvimento

Antes de iniciar o frontend:

1. Inicie o backend:

```bash
uvicorn main:app --reload
```

2. Em outro terminal:

```bash
ng serve
```

3. Acesse:

```text
http://localhost:4200
```

---

## Dados Utilizados

O sistema utiliza dados públicos relacionados a:

- Deputados Federais
- Despesas Parlamentares
- Votações
- Proposições Legislativas
- Presença Parlamentar
- Frentes Parlamentares
- Partidos Políticos

---

## Equipe

Projeto desenvolvido pelos alunos da Universidade Federal do Piauí (UFPI) para a disciplina de Banco de Dados Relacional.

---

## Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.

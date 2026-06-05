-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

-- That file uses encoding UTF-8

CREATE TABLE `Deputados`
 (
	`id_dep`			INTEGER NOT NULL, 
	`uri_dep`			varchar NOT NULL, 
	`nome_civil_dep`			varchar NOT NULL, 
	`cpf_dep`			varchar NOT NULL, 
	`sexo_dep`			varchar NOT NULL, 
	`redeSocial_dep`			TEXT, 
	`data_nascimento_dep`			DateTime, 
	`escolaridade_dep`			varchar, 
	`ultimoStatus_siglaPartido`			varchar, 
	`ultimoStatus_siglaUf`			varchar, 
	`ultimoStatus_situacao`			varchar
	, PRIMARY KEY (`id_dep`)
);

-- CREATE INDEXES ...

CREATE TABLE `Eventos`
 (
	`id_evento`			INTEGER NOT NULL, 
	`data_evento`			DateTime, 
	`situacao_evento`			varchar, 
	`tipo_evento`			varchar, 
	`data_hora_inicio_evento`			DateTime, 
	`data_hora_fim_evento`			DateTime, 
	`descricao_evento`			TEXT, 
	`url_documento_pauta`			varchar
	, PRIMARY KEY (`id_evento`)
);

-- CREATE INDEXES ...

CREATE TABLE `Frentes`
 (
	`id_frente`			INTEGER NOT NULL, 
	`titulo_frente`			TEXT, 
	`data_criacao_frente`			DateTime, 
	`id_legislatura`			INTEGER, 
	`situacao_frente`			varchar, 
	`keywords`			TEXT, 
	`id_deputado_coordenador`			INTEGER
	, PRIMARY KEY (`id_frente`)
);

-- CREATE INDEXES ...

CREATE TABLE `Proposicoes`
 (
	`id_proposicao`			INTEGER NOT NULL, 
	`sigla_tipo_proposicao`			varchar, 
	`numero_proposicao`			INTEGER, 
	`ano_proposicao`			INTEGER, 
	`cod_tipo_proposicao`			INTEGER, 
	`descricao_tipo_proposicao`			TEXT, 
	`ementa`			TEXT, 
	`ementa_detalhada`			TEXT, 
	`keywords`			TEXT, 
	`data_apresentacao`			DateTime, 
	`url_inteiro_teor`			TEXT, 
	`ultimo_status_data_hora`			DateTime, 
	`ultimo_status_descricao_tramitacao`			TEXT, 
	`ultimo_status_descricao_situacao`			TEXT, 
	`ultimo_status_id_situacao`			INTEGER, 
	`ultimo_status_regime`			TEXT, 
	`ultimo_status_apreciacao`			TEXT
	, PRIMARY KEY (`id_proposicao`)
);

-- CREATE INDEXES ...

CREATE TABLE `Votacao`
 (
	`id_votacao`			varchar NOT NULL, 
	`data_votacao`			DateTime NOT NULL, 
	`dataHoraRegistro_votacao`			DateTime, 
	`id_evento`			INTEGER NOT NULL, 
	`aprovacao`			INTEGER NOT NULL, 
	`votosSim`			INTEGER NOT NULL, 
	`votosNao`			INTEGER NOT NULL, 
	`votosOutros`			INTEGER NOT NULL, 
	`descricao_votacao`			TEXT, 
	`ultimaAberturaVotacao_dataHoraRegistro`			DateTime, 
	`ultimaAberturaVotacao_descricao`			TEXT, 
	`ultimaApresentacaoProposicao_dataHoraRegistro`			DateTime, 
	`ultimaApresentacaoProposicao_descricao`			TEXT, 
	`id_proposicao`			INTEGER
	, PRIMARY KEY (`id_votacao`)
);

-- CREATE INDEXES ...

CREATE TABLE `VotOrientacoes`
 (
	`id_votacao`			varchar NOT NULL, 
	`siglaBancada`			varchar NOT NULL, 
	`orientacao`			varchar
);

-- CREATE INDEXES ...

CREATE TABLE `VotProposicoes`
 (
	`id_votacao`			varchar NOT NULL, 
	`data_votacao`			DateTime NOT NULL, 
	`descricao_votacao`			TEXT, 
	`proposicao_id`			INTEGER, 
	`proposicao_siglaTipo`			varchar, 
	`proposicao_numero`			INTEGER, 
	`proposicao_ano`			INTEGER, 
	`proposicao_ementa`			TEXT, 
	`proposicao_titulo`			varchar
);

-- CREATE INDEXES ...

CREATE TABLE `VotVotos`
 (
	`id_votacao`			varchar NOT NULL, 
	`id_deputado`			INTEGER NOT NULL, 
	`voto`			varchar NOT NULL
);

-- CREATE INDEXES ...

CREATE TABLE `Despesas`
 (
	`id_cadastro_deputado`			INTEGER, 
	`id_deputado`			INTEGER, 
	`nome_parlamentar`			varchar, 
	`sigla_partido`			varchar, 
	`sigla_uf`			varchar, 
	`nu_legislatura`			INTEGER, 
	`cod_legislatura`			INTEGER, 
	`cod_subcota`			INTEGER, 
	`desc_subcota`			varchar, 
	`cod_especificacao_subcota`			INTEGER, 
	`desc_especificacao_subcota`			varchar, 
	`fornecedor_nome`			varchar, 
	`fornecedor_cnpj_cpf`			varchar, 
	`data_emissao`			DateTime, 
	`mes`			INTEGER, 
	`ano`			INTEGER, 
	`valor_documento`			REAL, 
	`valor_glosa`			REAL, 
	`valor_liquido`			REAL, 
	`id_documento`			INTEGER, 
	`url_documento`			TEXT
);

-- CREATE INDEXES ...

CREATE TABLE `PresencaDeputados`
 (
	`id_evento`			INTEGER NOT NULL, 
	`id_deputado`			INTEGER NOT NULL, 
	`data_evento`			DateTime, 
	`data_hora_inicio_evento`			DateTime
);

-- CREATE INDEXES ...

CREATE TABLE `FrentesDeputados`
 (
	`id_frente`			INTEGER NOT NULL, 
	`titulo_frente`			TEXT, 
	`id_deputado`			INTEGER NOT NULL, 
	`data_inicio`			DateTime, 
	`data_fim`			DateTime
);

-- CREATE INDEXES ...

CREATE TABLE `PropAutores`
 (
	`id_proposicao`			INTEGER NOT NULL, 
	`id_deputado`			INTEGER, 
	`cod_tipo_autor`			INTEGER, 
	`tipo_autor`			varchar, 
	`ordem_assinatura`			INTEGER, 
	`proponente`			INTEGER NOT NULL
);

-- CREATE INDEXES ...

CREATE TABLE `PropTemas`
 (
	`sigla_tipo_proposicao`			varchar NOT NULL, 
	`numero_proposicao`			INTEGER NOT NULL, 
	`ano_proposicao`			INTEGER NOT NULL, 
	`cod_tema`			INTEGER, 
	`tema`			TEXT, 
	`relevancia`			REAL
);

-- CREATE INDEXES ...



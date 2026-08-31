window.TERRITORIAL_DATA = {
  cadastros: [
    {localidade:'Área urbana agregada',tipo:'Agregado',servico:'Atenção primária e serviços urbanos',regularidade:'Não individualizada',fonte:'Cadastro demonstrativo'},
    {localidade:'Área distrital agregada',tipo:'Agregado',servico:'Rotas de saúde e educação',regularidade:'Não individualizada',fonte:'Cadastro demonstrativo'},
    {localidade:'Área rural agregada',tipo:'Agregado',servico:'Serviços itinerantes e infraestrutura',regularidade:'Não individualizada',fonte:'Cadastro demonstrativo'}
  ],
  comparacao: [
    {nome:'Fossa',evento:38.0,porta:55.6,n:'n=554'},
    {nome:'Rede pública de esgoto',evento:56.1,porta:41.7,n:'n=554'},
    {nome:'Benefício ou aposentadoria',evento:58.4,porta:72.4,n:'n=549'},
    {nome:'Adulto desempregado',evento:29.4,porta:38.2,n:'n=551'},
    {nome:'Problema de saúde no domicílio',evento:60.3,porta:66.4,n:'n=549'}
  ],
  metodologias: [
    {nome:'Cobertura territorial',def:'Presença de registros em estratos territoriais pseudonimizados.',num:'Estratos observados',den:'Estratos analíticos',fonte:'Base analítica pública',freq:'Por onda',lim:'Não representa cobertura domiciliar ou populacional.',proib:'Não localizar pessoas ou microterritórios.'},
    {nome:'Fossa informada',def:'Domicílios da amostra que marcaram fossa como solução de esgotamento.',num:'Respostas positivas',den:'Respostas válidas do item',fonte:'Diagnóstico territorial anonimizado, 2026',freq:'Base histórica',lim:'Não distingue fossa séptica de rudimentar.',proib:'Não apresentar como prevalência municipal.'},
    {nome:'Resíduo de esquema - "outro"',def:'Frequência da resposta residual em pergunta com categorias predefinidas.',num:'Respostas "outro"',den:'Respostas válidas do item',fonte:'Auditoria do instrumento',freq:'Por versão do formulário',lim:'Sinaliza categoria ausente, não erro do participante.',proib:'Não imputar retrospectivamente o conteúdo.'},
    {nome:'Renda familiar declarada',def:'Faixa de renda informada pelo respondente.',num:'Respostas por faixa',den:'Respostas válidas',fonte:'Diagnóstico territorial anonimizado, 2026',freq:'Base histórica',lim:'Autodeclarada e sujeita a viés.',proib:'Não usar como dado oficial municipal.'},
    {nome:'Avaliação de serviços públicos',def:'Percepção do respondente sobre serviços selecionados.',num:'Respostas por categoria',den:'Respostas válidas por serviço',fonte:'Diagnóstico territorial anonimizado, 2026',freq:'Base histórica',lim:'Percepção subjetiva.',proib:'Não apresentar como indicador oficial de qualidade.'}
  ],
  renda: [
    {faixa:'Igual ao valor de referência do instrumento',qtd:263,pct:38.0},
    {faixa:'Acima do valor de referência até R$ 10 mil',qtd:261,pct:37.7},
    {faixa:'Abaixo do valor de referência',qtd:138,pct:19.9},
    {faixa:'Outras faixas ou não informada',qtd:31,pct:4.5}
  ],
  moradia: [
    {tipo:'Condição afirmada no item',qtd:594,pct:86.1},
    {tipo:'Condição não afirmada',qtd:96,pct:13.9}
  ],
  composicaoFamiliar: {
    pessoasPorDomicilio: [
      {faixa:'1 pessoa',qtd:85,pct:12.2},{faixa:'2 pessoas',qtd:197,pct:28.3},
      {faixa:'3 pessoas',qtd:169,pct:24.3},{faixa:'4 pessoas',qtd:143,pct:20.6},
      {faixa:'5 ou mais',qtd:94,pct:13.5}
    ],
    idosos: [
      {faixa:'Nenhum idoso',qtd:436,pct:62.7},{faixa:'1 idoso',qtd:154,pct:22.2},
      {faixa:'2 ou mais idosos',qtd:105,pct:15.1}
    ],
    criancas: [],
    desemprego: [
      {faixa:'Nenhum desempregado',qtd:445,pct:64.0},{faixa:'1 desempregado',qtd:172,pct:24.7},
      {faixa:'2 ou mais ou não informado',qtd:78,pct:11.2}
    ]
  },
  saneamento: {
    esgoto: [
      {tipo:'Fossa',qtd:345,pct:49.6},{tipo:'Rede pública de esgoto',qtd:316,pct:45.5},
      {tipo:'Outro/Não informado',qtd:34,pct:4.9}
    ],
    agua: [{tipo:'Rede pública encanada',qtd:638,pct:91.8},{tipo:'Outro/Poço/Caminhão-pipa',qtd:57,pct:8.2}],
    energia: [{tipo:'Rede pública',qtd:669,pct:96.3},{tipo:'Outro/Ligação improvisada',qtd:26,pct:3.7}],
    lixo: [{tipo:'Recolhido pela prefeitura',qtd:629,pct:90.5},{tipo:'Queimado ou outro destino',qtd:66,pct:9.5}],
    separaLixo: {sim:278,nao:null,pctSim:null}
  },
  servicosAvaliacao: [
    {servico:'Escola pública',bom:62,neutro:20,ruim:0,naoSabe:0,n:82},
    {servico:'Posto de saúde',bom:54,neutro:29,ruim:0,naoSabe:0,n:83},
    {servico:'Assistência social',bom:46,neutro:37,ruim:0,naoSabe:0,n:83},
    {servico:'Coleta de resíduos',bom:46,neutro:36,ruim:0,naoSabe:0,n:82},
    {servico:'Farmácia pública',bom:43,neutro:39,ruim:0,naoSabe:0,n:82},
    {servico:'Serviço de zoonoses',bom:24,neutro:59,ruim:0,naoSabe:0,n:83}
  ],
  gestaoPrefeitura: [
    {avaliacao:'Positiva',qtd:32,pct:38.6},{avaliacao:'Razoável ou neutra',qtd:36,pct:43.4},
    {avaliacao:'Negativa',qtd:15,pct:18.1}
  ],
  vulnerabilidade: {
    trabalhoInfantil:{sim:159,total:695,pct:22.9,label:'Conhece criança/jovem que precisa trabalhar'},
    catacaoLixo:{sim:330,total:695,pct:47.5,label:'Conhece pessoa que faz catação de resíduos'},
    desempregoFamiliar:{sim:250,total:695,pct:36.0,label:'Tem adulto desempregado no domicílio'},
    semParticipacao:{sim:586,total:695,pct:84.3,label:'Sem participação comunitária informada'},
    semProjetoSocial:{sim:591,total:695,pct:85.0,label:'Família não participa de projeto social'},
    semHorta:{sim:503,total:695,pct:72.4,label:'Residência sem horta'}
  },
  lazer: [
    {espaco:'Praça',qtd:65,pct:79.3},{espaco:'Rio ou lago',qtd:64,pct:78.0},
    {espaco:'Bar/restaurante',qtd:53,pct:64.6},{espaco:'Quadra de esporte',qtd:48,pct:58.5},
    {espaco:'Campo de futebol',qtd:33,pct:40.2},{espaco:'Outros espaços',qtd:12,pct:14.6}
  ],
  pedidosMelhorias: [
    {destino:'Vereador',qtd:28,pct:34.1},{destino:'Prefeito',qtd:27,pct:32.9},
    {destino:'Demais respostas agregadas',qtd:27,pct:32.9}
  ],
  localidadesGeo: []
};

# Módulo público de auditoria e análise de dados (`analysis`)

Este diretório concentra a infraestrutura de processamento de dados do pacote territorial anonimizado. Seu propósito é garantir a integridade, a reprodutibilidade e a transparência metodológica na geração dos indicadores estatísticos e das tabelas presentes no protótipo web.

## 1. Requisitos do Ambiente

Para executar os scripts de auditoria de dados, você precisa de um ambiente com Python configurado:
- **Versão recomendada:** Python 3.10 ou superior.
- **Dependências:** Estão descritas no arquivo `requirements.txt` (`pandas`, `numpy`, `openpyxl`).

### Configurando o ambiente

```bash
# Recomendado: criar um ambiente virtual (opcional)
python -m venv venv
# Ativar o ambiente (Windows)
venv\Scripts\activate
# Instalar as dependências
pip install -r requirements.txt
```

## 2. Conteúdo do Diretório

- `public_analytic_data.csv`: base analítica reduzida e pseudonimizada usada para regenerar os resultados públicos.
- `public_data_dictionary.md`: dicionário das colunas publicadas.
- `disclosure_risk_audit.md`: transformações de desidentificação e risco residual.
- `regenerate_analysis.py`: módulo que regenera `results.json` a partir da base analítica pública.
- `schema_e_dicionario.md`: Documentação descrevendo as variáveis coletadas (dicionário de dados) e o formato do output em JSON (schema).
- `cleaning_rules.md`: Regras de limpeza documentadas (como conversões para booleanos, normalização de texto sem acentos, etc.).
- `generate_synthetic.py` & `synthetic_data.xlsx`: Scripts de geração e a respectiva massa de dados fictícios para permitir testes da pipeline de análise de forma pública.

## 3. Versionamento e origem dos dados

> [!IMPORTANT]
> A base bruta não é publicada por conter informações pessoais, respostas livres e granularidade territorial incompatíveis com a finalidade de revisão. O pipeline público começa em `public_analytic_data.csv`.

Para regenerar os resultados públicos:

```bash
python -c "from pathlib import Path; from regenerate_analysis import regenerate; regenerate(Path('public_analytic_data.csv'), Path('results.json'))"
```

## 4. Testes com Dados Sintéticos

Como a base real é omitida, você pode executar todo o fluxo usando a base sintética que foi formatada para simular o layout real dos dados e cobrir casos extremos (missing values, typos de texto).

Para gerar novamente a base sintética a qualquer momento:
```bash
python generate_synthetic.py
```

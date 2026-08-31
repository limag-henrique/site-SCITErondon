# Pacote territorial anonimizado

Este repositório possui um propósito duplo:
1. **Protótipo Web:** Hospedar uma página estática e offline-first para exploração de dados territoriais agregados.
2. **Auditoria de Dados (`analysis`):** Fornecer dados analíticos desidentificados, código e documentação para auditar as estatísticas do estudo.

## 1. Protótipo Web

O protótipo acadêmico é estático e *offline-first*, sem envio de dados a um servidor externo.

### Como executar

1. Abra um terminal na pasta principal do repositório.
2. Execute `python -m http.server 8000`.
3. Acesse `http://localhost:8000` no navegador.
4. Após o primeiro carregamento, os ativos ficam em cache pelo *service worker*.

Também é possível abrir o `index.html` diretamente, mas o cache offline via *service worker* exige carregamento via HTTP/HTTPS.

### Funcionalidades demonstradas

- aviso de geografia protegida, sem coordenadas ou microterritórios;
- cadastro demonstrativo de estratos agregados e serviços, mantido apenas no navegador;
- indicador de cobertura territorial;
- fichas metodológicas automáticas;
- aviso permanente de amostra não representativa;
- comparação eventos versus porta a porta/distritos;
- alerta de categoria “outro” acima do limiar;
- contestação/correção comunitária com trilha local;
- arquitetura *offline-first*.

### Limitações

Os cadastros de serviços e o indicador de cobertura são demonstrativos. Coordenadas, propriedades e microterritórios foram retirados do pacote de revisão. Uma implantação posterior exigiria validação comunitária, autenticação, integração com registros administrativos, política de retenção, controles de acesso e avaliação com usuários reais.

## 2. Auditoria e Análise (`analysis`)

A pasta `analysis` contém os scripts necessários para regenerar as estatísticas públicas a partir de `public_analytic_data.csv`. A base bruta identificável não integra este repositório.

Seu objetivo é garantir a total transparência metodológica, permitindo que a análise de dados, cálculos de vulnerabilidade/capacidade e as comparações (Estudos 1, 2, 3 e 4) possam ser auditados e reproduzidos por terceiros.

### Como auditar

1. Navegue até a pasta `analysis`:
   ```bash
   cd analysis
   ```
2. Instale as dependências necessárias (recomenda-se o uso de um ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```
3. O script principal é o `regenerate_analysis.py`, que lê a fonte de dados e gera os resultados reprodutíveis em `results.json`. Você pode integrar a execução deste script passando o caminho do arquivo base de origem.

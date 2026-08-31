# Dicionário da base analítica pública

`public_analytic_data.csv` contém 640 registros analíticos: 557 da onda realizada em janeiro de 2026 e 83 de uma onda posterior. A transformação foi executada em ambiente privado; nenhuma chave entre códigos e pessoas ou territórios é publicada.

## Campos de desenho

| Campo | Tipo | Definição pública |
|---|---|---|
| `wave` | categoria | códigos de onda sem calendário detalhado. |
| `interface` | categoria | `evento`, `porta_a_porta` ou `segunda_onda`. |
| `territory` | código | Estrato territorial `T01`–`T05`; ausente quando não usado no modelo. |
| `interviewer` | código | Agrupamento `E01`–`E18`; ausente na segunda onda. |
| `submission_hour` | número | Hora inteira, sem data, minuto, segundo ou fuso identificador. |

## Indicadores binários

Os campos abaixo usam `1` para presença/seleção, `0` para ausência/não seleção e vazio para resposta indisponível ou não aplicável:

- infraestrutura e ambiente: `septic`, `sewer_network`, `municipal_trash`, `burning`, `water_network`, `electric_network`, `waste_separation`, `recycling`, `garden`, `difficult_access`, `housing_risk`;
- proteção social e economia: `cadunico`, `commerce`, `low_income`, `unemployed`, `benefit_or_retirement`, `social_transfer`;
- saúde e condições autorreferidas: `health_problem`, `hypertension`, `diabetes`, `controlled_medicine`, `cigarette`, `alcohol`, `physical_disability`, `mental_disability`, `domestic_violence`, `elderly`;
- capacidades e participação: `manual_skill`, `artistic_skill`, `community_engagement`, `social_project`, `improvement_request`;
- esquema informacional: `news_other`.

`household_size` é numérico e foi limitado superiormente a `6`; o valor `6` significa seis ou mais moradores na versão pública.

## Exclusões

A versão pública não contém nome ou contato do respondente, localidade textual, coordenada, UUID, identificador de submissão, texto livre, data completa, minuto, segundo, nome de entrevistador ou vínculo institucional. As posições das colunas brutas não constituem parte do schema público.

## Uso responsável

Os registros decorrem de amostragem de conveniência. Proporções descrevem a base observada e não estimam prevalências municipais. Os códigos `E` e `T` são estratos analíticos opacos e não devem ser vinculados a pessoas ou localidades.

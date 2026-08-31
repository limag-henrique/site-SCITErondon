# Auditoria de risco de divulgação

## Resultado

- Identificadores diretos removidos: nomes, contatos, UUIDs, identificadores de submissão e texto livre.
- Identificadores geográficos removidos: nomes de bairro, distrito, propriedade e coordenadas.
- Identificadores temporais reduzidos: a data foi substituída por onda/interface; minuto e segundo foram eliminados.
- Identificadores operacionais pseudonimizados: entrevistadores e territórios são códigos sem chave pública.
- Tamanho domiciliar limitado superiormente a seis.
- O arquivo foi verificado por padrões de e-mail e UUID, sem ocorrências.

## Risco residual

A pseudonimização preserva relações necessárias aos modelos ajustados, mas não transforma a base em estatística oficial nem elimina todo risco para agentes que já possuam informação auxiliar do trabalho de campo. A base deve ser usada exclusivamente para auditoria científica agregada. Tentativas de reidentificação, ligação com cadastros externos ou interpretação individual são incompatíveis com sua finalidade.

As células pequenas de sobreposição entre agrupamento e interface são apresentadas somente porque constituem diagnóstico metodológico central da estrutura de clusters. Nenhuma chave nominal é disponibilizada, e o protótipo não mostra resultados sensíveis cruzados por agrupamento.

# Schema público

O schema normativo do pacote é o arquivo `public_analytic_data.csv`, descrito em `public_data_dictionary.md`.

## Estrutura

- uma linha por registro analítico;
- campos de desenho: `wave`, `interface`, `territory`, `interviewer`, `submission_hour`;
- indicadores binários com valores `0`, `1` ou ausente;
- `household_size` numérico e limitado superiormente a seis.

O schema bruto de 192 colunas não é publicado porque incluía identificadores diretos, texto livre e variáveis fora da finalidade científica do pacote de revisão.

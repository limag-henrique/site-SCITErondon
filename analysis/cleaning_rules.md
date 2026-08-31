# Regras públicas de limpeza e desidentificação

O pacote público começa após a transformação privada da fonte bruta. As regras observáveis são:

1. registros da onda de janeiro sem qualquer resposta substantiva são excluídos;
2. em janeiro de 2026, as interfaces são classificadas como `evento` ou `porta_a_porta` segundo uma regra privada de processamento; o calendário detalhado não integra o pacote público;
3. nomes de entrevistador são normalizados em ambiente privado e convertidos em `E01`–`E18`, sem chave pública;
4. cinco estratos territoriais usados nos modelos são convertidos em `T01`–`T05`, sem topônimo público;
5. datas, minutos, segundos, UUIDs, contatos, nomes, coordenadas e texto livre não são exportados;
6. tamanho domiciliar é limitado a seis ou mais;
7. respostas “não sabe/não respondeu” permanecem ausentes quando a definição do indicador exige resposta válida;
8. indicadores multisseleção são binarizados conforme documentado em `public_data_dictionary.md` e no Material Suplementar A.

Os scripts públicos não contêm lista nominal nem rotina capaz de reconstruir a chave entre códigos e pessoas.

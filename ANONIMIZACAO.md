# Política de anonimização do pacote de dados

Este repositório é um pacote de dados, código e materiais suplementares preparado para revisão por pares duplo-cega. O local do estudo é apresentado apenas como Município A, no norte de Minas Gerais; autoria e vínculos organizacionais permanecem omitidos.

## Exclusões obrigatórias

Os artefatos públicos não devem conter:

- nomes ou contatos de participantes, entrevistadores, autores ou agentes institucionais;
- UUIDs, identificadores de submissão ou texto livre dos questionários;
- datas e horários completos de registros individuais;
- coordenadas, propriedades rurais ou microterritórios com células pequenas;
- tabelas que relacionem os códigos `E01`–`E18` a pessoas;
- metadados autorais em PDF ou planilhas.

## Transformações

- agrupamentos de entrevistador são representados por códigos `E01`–`E18` ordenados pela quantidade de registros, sem chave pública de reversão;
- territórios usados como estratos analíticos são representados por códigos `T01`–`T05`, sem chave pública de reversão;
- o horário é mantido apenas como hora inteira, sem data, minuto ou segundo;
- tamanho domiciliar é limitado superiormente a seis pessoas na versão pública;
- localidades apresentadas no protótipo são agregadas e células inferiores a dez são suprimidas;
- a documentação de campo é disponibilizada somente como notas metodológicas parafraseadas.

## Limites

A base pública permite auditar os resultados agregados e o papel dos estratos nos modelos, mas não deve ser usada para localizar domicílios ou participantes. A base bruta permanece fora deste repositório e não é necessária para consultar os resultados publicados.

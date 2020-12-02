# Análise dos dados do censo universitário

Este repositório tem como objetivo apresentar uma breve análise realizada sobre os dados do censo universitário brasileiro com efoque em uma perspectiva racial dos alunos na universidade.

Foram coletados e analisados os dados entre os anos de 2009-2019 disponibilizados pelo INEP publicamente [neste site](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior/resultados?_authenticator=73b6b0e03f10cadf5ec8ab8e09e6be4f931e571f).


### Coleta dos dados

Para coletar e extrair os dados disponibilizados no INEP você pode executar o crawler disponibilizado neste repositório:

> É recomendado que crie um [ambiente virtual](https://virtualenv.pypa.io/en/latest/) com python 3.8 e instale os requerimentos necessários para rodar o projeto, desta forma:

```
pip install requirements.txt
```

> Depois execute o crawler disponibilizado
```
python crawler/crawler_censo_universitario.py
```

Você deve obter um resultado semelhante ao descrito abaixo:

![image](https://user-images.githubusercontent.com/3440180/100755727-3fff3680-33cb-11eb-8869-20b906c6c978.png)

Neste ponto todos os arquivos estarão extraídos na pasta `dados` deste projeto, prontos para iniciar a análise.


### Análise dos dados coletados

Para realizar a análise, os dados disponibilizados por meio de planilhas, foram carregados com auxílio da biblioteca `pandas` e salvos em uma base de dados SQLite.

Posteriormente foram realizadas consultas para a ilustração de algumas informações como: a quantidade de alunos negros na universidade por ano, a quantidade de alunos negros que ingressaram por meio de reserva de vagas, dentre outras questões.

[**Confira a análise completa aqui.**](analise.ipynb)
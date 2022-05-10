# Descrição

Uma aplicação que recebe dados de um csv e permite a consulta de uma lista de vulnerabilidades e a atualização de status das mesmas (corrigidas, não corrigidas)

## Instalação

- Primeiro faça o fork e clone o repositório

```
git clone git@github.com
```

- Crie o ambiente um [ambiente virtual em python](https://docs.python.org/pt-br/3/tutorial/venv.html)

```
$ python -m venv venv --upgrade-deps
```

- Entre no ambiente virtual

```
$ source venv/bin/activate
```

- Instale as dependencias do arquivo `requirements.txt`

```
$ pip install -r requirements.txt
```

- crie as tabelas no banco de dados

```
$ ./manage.py migrate
```

- Carregue a pagina de scrips para popular o banco com o cvs

```
$ ./manage.py runscript populate
```

- Por fim, rode a aplicação

```
$ ./manage.py runserver
```

## Testes

- Rode os testes com o comando

```
$ ./manage.py test -v 2
```

## Linguagens/Framework/libs

- Python
- Django
- Django Rest Framework
- django_extensions

# Rotas

## GET - Listar todas

Lista todas as vunerabilidades com paginação de no mácimo 50 por página

### Endpoint: api/reports/

- para selecionar outras páginas utilize o parâmetro: _page_. Ex.: api/reports/?page=3

- Por padrão, o resultado da requisição é ordenado em conjunto por data de publicação crescente **e** cvss decrescente respectivamente.
- Para uma ordenação por data de publicação decrescente utilize **date='desc'**
  - Ex.: api/reports/?page=3&date=desc
- Para uma ordenação por cvss crescente utilize **cvss='asc'**

  - Ex.: api/reports/?page=3&date=desc&cvss=asc

- Pode ser filtrado por **hostname**

  - use o parâmetro _name_

  - Ex.: api/reports/?name=server-4

- Podem ser aplicados mais dois filtros, o **severity** e o **fixed**

  - O _severity_ aceita os seguintes valores:

    - critico
    - alto
    - medio
    - baixo

  - O _fixed_ aceita os valores 'corrigida' e 'nao-corrigida'
  - Exemplos:
    - api/reports/?page=3&fixed=corrigida
    - api/reports/?page=3&severity=baixo

## GET - pegar uma

Pega uma vunerabilidade específica através de seu id

### Endpoint: api/reports/< int:report_id >/

## PATCH - Atualizar status da Vunerabilidade

Permite apenas a mudança de status do fixed que indica que a vunerabilidade foi corrigida ou não.

### Endpoint: api/reports/< int:report_id >/

# Descrição

Uma aplicação que recebe dados de um arquivo.csv e permite a consulta de uma lista de vulnerabilidades e a atualização de status das mesmas (corrigidas, não corrigidas)

## Instalação

- Primeiro faça o fork e clone o repositório

```
git clone < git@github.com:MiqueiasCS/tabela_de_dados_back.git >
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

- Carregue a pagina de scrips para popular o banco com o arquivo .csv

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
** Todas as rotas com excessão do login necessitam de autenticação!! 


## Post - Login
### Endpoint: api/login/

Utilize o _email: testador@mail.com_ e _senha 123asd_ no body;
<div align="center">
  <a href="https://imgur.com/zRVvYda"><img src="https://i.imgur.com/zRVvYda.png" title="source: imgur.com" /></a>
</div>

## GET - Listar todas

Lista todas as vunerabilidades com paginação de no mácimo 50 por página

### Endpoint: api/reports/
<div align="center">
  <a href="https://imgur.com/rJkga6M"><img src="https://i.imgur.com/rJkga6M.png" title="source: imgur.com" /></a>
</div>

#### Paginação

- para selecionar outras páginas utilize o parâmetro: _page_. Ex.: api/reports/?page=3

#### Ordenação
- Por padrão, o resultado da requisição é ordenado em conjunto por cvss decrescente **e** data de publicação crescente respectivamente.
- Para uma ordenação por data de publicação decrescente utilize **date='desc'**
  - Ex.: api/reports/?page=3&date=desc
- Para uma ordenação por cvss crescente utilize **cvss='asc'**

  - Ex.: api/reports/?page=3&date=desc&cvss=asc
  
 <div align="center">
  <a href="https://imgur.com/V0mfgZz"><img src="https://i.imgur.com/V0mfgZz.png" title="source: imgur.com" /></a>
</div>

#### Filtragem

- Pode ser filtrado por **hostname**

  - use o parâmetro _name_
  - Retorna todos os itens que **contém** a palavra passada em **name**
  - Ex.: api/reports/?name=server
 <div align="center">
  <a href="https://imgur.com/SKBHP08"><img src="https://i.imgur.com/SKBHP08.png" title="source: imgur.com" /></a>
</div>

- Podem ser aplicados mais dois filtros, o **severity**, **fixed** e **severity e fixed**

  - O _severity_ aceita os seguintes valores:

    - critico
    - alto
    - medio
    - baixo

  - O _fixed_ aceita os valores 'corrigida' e 'nao-corrigida'
  - Exemplos:
    - api/reports/?page=3&fixed=corrigida
     <div align="center">
      <a href="https://imgur.com/pVztN8g"><img src="https://i.imgur.com/pVztN8g.png" title="source: imgur.com" /></a>
    </div>
    - api/reports/?page=3&severity=baixo
     <div align="center">
      <a href="https://imgur.com/JwE6U0H"><img src="https://i.imgur.com/JwE6U0H.png" title="source: imgur.com" /></a>
     </div>
    - api/reports/?page=3&severity=baixo&fixed=corrigida&severity=baixo
     <div align="center">
      <a href="https://imgur.com/1eyEVOp"><img src="https://i.imgur.com/1eyEVOp.png" title="source: imgur.com" /></a>
     </div>

## GET - mostrar por id

Pega uma vunerabilidade específica através de seu id

### Endpoint: api/reports/< int:report_id >/

 <div align="center">
    <a href="https://imgur.com/JVAcryq"><img src="https://i.imgur.com/JVAcryq.png" title="source: imgur.com" /></a>
 </div>

## GET - listar por hostname

Pega um lista de vunerabilidades registradas com o hostname

### Endpoint: api/reports/< str:hostname >/
- Retorna uma lista com todos os itens do **hostname** informado. Só aceita palavras exatas, o hostname buscado por parâmetro deve ter um registro exatamente igual no banco.
- Não diferencia maiúsculas de minúsculas. Ex.: server-4 = SERVER-4

<div align="center">
    <a href="https://imgur.com/ytpwMKj"><img src="https://i.imgur.com/ytpwMKj.png" title="source: imgur.com" /></a>
</div>

## PATCH - Atualizar status da Vunerabilidade

Permite apenas a mudança de status do fixed que indica que a vunerabilidade foi corrigida ou não.
- fixed é um booleao onde seu valor indica se a vunerabilidade está corrigida ou não

### Endpoint: api/reports/< int:report_id >/
<div align="center">
    <a href="https://imgur.com/dVxjcO0"><img src="https://i.imgur.com/dVxjcO0.png" title="source: imgur.com" /></a>
</div>

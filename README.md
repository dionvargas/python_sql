# Integração com Banco de Dados MySQL em Python

Este projeto implementa uma aplicação Python para gerenciar produtos usando MySQL. Ele utiliza a biblioteca `mysql-connector-python` para se conectar ao banco de dados e realizar operações CRUD (Create, Read, Update, Delete).

## Requisitos

- Python 3.8 ou superior
- MySQL instalado e em execução
- Biblioteca `mysql-connector-python`

## Instalação

### 1. **Clone o repositório**
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_DIRETORIO>
```

### 2. Instale as dependências
Certifique-se de que você possui a biblioteca mysql-connector-python instalada:
```
pip install mysql-connector-python
```
ou
```
python -m pip install mysql-connector-python
```

### 3. Exexuteo o arquivo ``banco.sql``
Execute o arquivo ``banco.sql`` para criar o banco e o popular.

### 4. Altere o arquivo ``main.py``

Altere o arquivo ``main.py`` para as configurações do seu banco de dados na linha:
```python
# Conexão com o banco de dados
dao = ProdutoDAO(host="localhost", user="root", password="123456", database="produtos_ti")
```

## A Classe ProdutoDao

A classe ProdutoDAO é responsável por realizar operações no banco de dados relacionadas aos produtos. Ela encapsula as funcionalidades de conexão, manipulação e fechamento do banco, seguindo o padrão DAO (Data Access Object).

### Métodos
1. ``__init__``
Construtor que estabelece a conexão com o banco de dados e inicializa o cursor.

    - Parâmetros:
        - ``host``: endereço do servidor MySQL (geralmente ``localhost``).
        - ``user``: nome do usuário do MySQL.
        - ``password``: senha do usuário.
        - ``database``: nome do banco a ser utilizado.


``` python
def __init__(self, host, user, password, database):
    self.conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    self.cursor = self.conexao.cursor()
```

2. ``criar_tabela``

Cria a tabela ``produto`` no banco, se ela ainda não existir.

- SQL Executado:
```SQL
CREATE TABLE IF NOT EXISTS produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL
);
```
```python
def criar_tabela(self):
    query = """
    CREATE TABLE IF NOT EXISTS produto (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        descricao TEXT,
        preco DECIMAL(10, 2) NOT NULL
    );
    """
    self.cursor.execute(query)
    self.conexao.commit()
```

3. ``inserir``
Insere um novo produto no banco.

- Parâmetro:
Um objeto da classe Produto contendo nome, descrição e preço.
- SQL Executado:
```SQL
INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s);
```
- Exemplo de Uso:
```python 
produto = Produto(nome="Notebook", descricao="Ultrafino", preco=4500.00)
dao.inserir(produto)
```
```python
def inserir(self, produto):
    query = "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s)"
    valores = (produto.nome, produto.descricao, produto.preco)
    self.cursor.execute(query, valores)
    self.conexao.commit()
```

4. ``listar``

Recupera todos os produtos do banco.

- Retorno:
Uma lista de tuplas contendo os campos ``id``, ``nome``, ``descrição`` e ``preço``.
- SQL Executado:
```SQL
SELECT * FROM produto;
```
```python
def listar(self):
    query = "SELECT * FROM produto"
    self.cursor.execute(query)
    return self.cursor.fetchall()
```

5. ``atualizar``
Atualiza os dados de um produto no banco com base no ``id``.

- Parâmetros:
    - ``produto_id``: identificador do produto a ser atualizado.
    - ``produto``: objeto da classe ``Produto`` com os novos dados.

- SQL Executado:
```SQL
UPDATE produto
SET nome = %s, descricao = %s, preco = %s
WHERE id = %s;
```
```python
def atualizar(self, produto_id, produto):
    query = """
    UPDATE produto
    SET nome = %s, descricao = %s, preco = %s
    WHERE id = %s
    """
    valores = (produto.nome, produto.descricao, produto.preco, produto_id)
    self.cursor.execute(query, valores)
    self.conexao.commit()
```

6. ``deletar``

Remove um produto do banco com base no id.

- Parâmetro:
``produto_id``: identificador do produto a ser deletado.

- SQL Executado:
```SQL
DELETE FROM produto WHERE id = %s;
```

7. ``__del__``

Destrutor que fecha o cursor e a conexão com o banco de dados ao final da execução.
- Inclui verificações para evitar erros caso o cursor ou a conexão não tenham sido criados.

```python
def __del__(self):
    if hasattr(self, 'cursor') and self.cursor:
        self.cursor.close()
    if hasattr(self, 'conexao') and self.conexao:
        self.conexao.close()
```
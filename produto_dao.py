# Importa a biblioteca mysql.connector, usada para conectar e interagir com o banco de dados MySQL
import mysql.connector
# Importa a classe Produto, que representa o modelo de dados de um produto
from produto import Produto

class ProdutoDAO:
    """
    A classe ProdutoDAO gerencia a interação entre a aplicação e o banco de dados.
    Ela fornece métodos para realizar operações CRUD (Create, Read, Update, Delete) na tabela 'produto'.
    """
    
    def __init__(self, host, user, password, database):
        """
        O construtor inicializa a conexão com o banco de dados e cria o cursor para executar as consultas.
        
        :param host: Endereço do servidor MySQL
        :param user: Nome do usuário para autenticação no MySQL
        :param password: Senha do usuário MySQL
        :param database: Nome do banco de dados a ser usado
        """
        # Estabelece a conexão com o banco de dados usando as credenciais fornecidas
        self.conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # Cria um cursor que permite executar comandos SQL no banco de dados
        self.cursor = self.conexao.cursor()

    def criar_tabela(self):
        """
        Cria a tabela 'produto' no banco de dados caso ela não exista.
        A tabela contém colunas para id, nome, descrição e preço do produto.
        """
        query = """
        CREATE TABLE IF NOT EXISTS produto (
            id INT AUTO_INCREMENT PRIMARY KEY,  # ID do produto, será gerado automaticamente
            nome VARCHAR(255) NOT NULL,  # Nome do produto, não pode ser nulo
            descricao TEXT,  # Descrição do produto
            preco DECIMAL(10, 2) NOT NULL  # Preço do produto, precisa ser um número com até 2 casas decimais
        );
        """
        # Executa a query para criar a tabela
        self.cursor.execute(query)
        # Confirma a execução da consulta no banco de dados
        self.conexao.commit()

    def inserir(self, produto):
        """
        Insere um novo produto na tabela 'produto'.
        
        :param produto: Objeto da classe Produto contendo os dados a serem inseridos.
        """
        # Define a consulta SQL para inserir um novo produto
        query = "INSERT INTO produto (nome, descricao, preco) VALUES (%s, %s, %s)"
        # Preenche os valores com os atributos do produto
        valores = (produto.nome, produto.descricao, produto.preco)
        # Executa a query para inserir os dados
        self.cursor.execute(query, valores)
        # Confirma a execução da inserção no banco de dados
        self.conexao.commit()

    def listar(self):
        """
        Lista todos os produtos da tabela 'produto'.
        
        :return: Lista de tuplas contendo os dados de todos os produtos
        """
        # Define a consulta SQL para selecionar todos os produtos
        query = "SELECT * FROM produto"
        # Executa a consulta
        self.cursor.execute(query)
        # Retorna todos os resultados da consulta
        return self.cursor.fetchall()

    def atualizar(self, produto_id, produto):
        """
        Atualiza os dados de um produto existente na tabela 'produto'.
        
        :param produto_id: ID do produto que será atualizado
        :param produto: Objeto da classe Produto contendo os novos dados
        """
        # Define a consulta SQL para atualizar um produto com base no seu ID
        query = """
        UPDATE produto
        SET nome = %s, descricao = %s, preco = %s
        WHERE id = %s
        """
        # Preenche os valores com os atributos do produto e o ID
        valores = (produto.nome, produto.descricao, produto.preco, produto_id)
        # Executa a consulta para atualizar os dados
        self.cursor.execute(query, valores)
        # Confirma a execução da atualização no banco de dados
        self.conexao.commit()

    def deletar(self, produto_id):
        """
        Deleta um produto da tabela 'produto' com base no ID fornecido.
        
        :param produto_id: ID do produto a ser deletado
        """
        # Define a consulta SQL para excluir o produto com o ID fornecido
        query = "DELETE FROM produto WHERE id = %s"
        # Executa a consulta para excluir o produto
        self.cursor.execute(query, (produto_id,))
        # Confirma a execução da exclusão no banco de dados
        self.conexao.commit()

    def __del__(self):
        """
        Destruidor da classe, que fecha a conexão com o banco de dados e o cursor
        quando o objeto ProdutoDAO é destruído.
        """
        # Fecha o cursor, liberando os recursos utilizados
        self.cursor.close()
        # Fecha a conexão com o banco de dados
        self.conexao.close()

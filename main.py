from produto import Produto
from produto_dao import ProdutoDAO

# Conexão com o banco de dados
dao = ProdutoDAO(host="localhost", user="root", password="123456", database="produtos_ti")

# Criando um novo produto
novo_produto = Produto(nome="Monitor Ultrawide", descricao="Monitor de 34 polegadas, resolução QHD.", preco=1800.00)
dao.inserir(novo_produto)
print("Produto inserido com sucesso!")

# Listando todos os produtos
produtos = dao.listar()
for produto in produtos:
    print(produto)

# Atualizando um produto
produto_atualizado = Produto(nome="Teclado RGB", descricao="Teclado mecânico com iluminação personalizável.", preco=300.00)
dao.atualizar(produto_id=1, produto=produto_atualizado)
print("Produto atualizado com sucesso!")

# Deletando um produto
dao.deletar(produto_id=2)
print("Produto deletado com sucesso!")
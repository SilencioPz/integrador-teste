import mysql.connector
from mysql.connector import errorcode

def create_database(cursor, database):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        print("Falha ao criar o banco de dados: {}".format(err))
        exit(1)

# Conexão ao MySQL
print("Conexão a ser estabelecida...")
try:
    conn = mysql.connector.connect(
            host='127.0.0.1',
            user='bruno',
            password='1234'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Usuário ou senha inválida')
    else:
            print(err)
            
#Criação da estrutura do banco de dados
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `projeto_web_mer`;")
cursor.execute("CREATE DATABASE `projeto_web_mer`;")
cursor.execute("USE `projeto_web_mer`;")

# Tabela usuario
print("Criando a tabela 'usuario'...")
cursor.execute("USE projeto_web_mer;")
cursor.execute('''
    CREATE TABLE `usuario` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `nome` varchar(100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `senha` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

# Inserção de usuários com senha em texto plano
cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", ('bruno perez', 'adm@outlook.com', 'crud25@$'))

cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", ('brunim', 'brunim@gmail.com', 'abc12345'))

cursor.execute("INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)", ('rauzim', 'raulzim@gmail.com', 'def56789'))

# Tabela livros
print("Criando a tabela 'livros'...")
cursor.execute('''
    CREATE TABLE `livros` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `usuario_id` int(11) NOT NULL,
    `ISBN` text NOT NULL,
    `titulo` text NOT NULL,
    `autor` text NOT NULL,
    `editora` text NOT NULL,
    `ano_publicacao` int(11) NOT NULL,
    `categoria` text NOT NULL,
    `quantidade` int(11) NOT NULL,
    `preco` DECIMAL(10,2) NOT NULL, 
    `imagem` text NOT NULL,
    `palavrinha` text NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`usuario_id`) REFERENCES `usuario`(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

# Livro inicial com palavrinhas
cursor.execute("INSERT INTO livros (usuario_id, ISBN, titulo, autor, editora, ano_publicacao, categoria, quantidade, preco, imagem, palavrinha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (1, '9788576082675', 'codigo limpo', 'Robert C. Martin', 'Alta Books', 2008, 'Software Development', 10, 45.00, 'codigo-limpo.png', 'codigo limpo habilidades praticas agile software robert martin programador melhor praticar'))

#Tabela Feedback dos usuários
print("Criando a tabela 'feedback'...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS `feedback` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `usuario_id` int(11),
    `opiniao` text NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`usuario_id`) REFERENCES `usuario`(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

#Feedback inicial
cursor.execute("INSERT INTO feedback (usuario_id, opiniao) VALUES (%s, %s)", (1, 'Achei o site mais ou menos. Não falou de jogo nem nada, achei paia...'))

# Print de sucesso e funções de conexão
print("Banco de dados e tabelas criados com sucesso!")
conn.commit()
cursor.close()
conn.close()
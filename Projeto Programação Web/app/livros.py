from bs4 import BeautifulSoup # type: ignore
import os

# Criação da classe livros e os métodos get, set, __str__ e as funções de manipulação HTML
class Livro:
    def __init__(self, nome, autor):
        self.nome = nome
        self.autor = autor

    def get_nome(self):
        return self.nome
    
    def get_autor(self):
        return self.autor
    
    def set_nome(self, new_name):
        self.nome = new_name
    
    def set_autor(self, new_autor):
        self.autor = new_autor


    def __str__(self):
        livro = f'\n'\
                f'--------- Livro --------- \n'\
                f' - Nome: {self.nome} \n - Autor: {self.autor} \n'\
                f'-------------------------\n'
        return livro

    def create_tag(self, tag, conteudo='', **atributos):
        # Monta a string de atributos
        atributos_str = ''.join([f' {key}="{value}"' for key, value in atributos.items() if key != 'class_'])
        # Substitui 'class_' por 'class' para compatibilidade com a palavra reservada
        if 'class_' in atributos:
            atributos_str += f' class="{atributos["class_"]}"'
        
        # Gera a tag completa
        tag_html = f'<{tag}{atributos_str}>{conteudo}</{tag}>'
        
        return tag_html

    def create_book(self):
        img_tag = self.create_tag('img', src='', alt='Livro em destaque', class_='article-img', height='160')
        h3_tag = self.create_tag('h3', self.nome, class_='article-title')
        p_desc_tag = self.create_tag('p', 'ADICIONAR DESCRIÇÃO', class_='article-description')
        p_autor_tag = self.create_tag('p', f'Autor(a): {self.autor}')
        div_content = self.create_tag('div', f'{h3_tag}{p_desc_tag}{p_autor_tag}', class_='article-content')
        
        article_tag = self.create_tag('article', f'{img_tag}{div_content}', class_='article')
        
        return article_tag

# Função para adicionar livros na página /livros
def add_book(article_html, caminho_arquivo='Projeto Programação Web/app/templates/livros.html'):
    # Garante que o caminho é relativo ao diretório atual do script
    caminho_arquivo = os.path.join(os.getcwd(), caminho_arquivo)
    
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
    
    # Lê o conteúdo do arquivo HTML
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo_html = arquivo.read()
    # Utiliza BeautifulSoup para parsear o HTML
    soup = BeautifulSoup(conteudo_html, 'html.parser')
    # Encontra a tag <main>
    main_tag = soup.find('main', class_='main')
    # Adiciona o artigo HTML dentro da tag <main>
    if main_tag:
        # Adiciona o conteúdo
        novo_conteudo = BeautifulSoup(article_html, 'html.parser')
        main_tag.append(novo_conteudo)
    # Salva o HTML modificado de volta no arquivo com pretty print
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(soup.prettify(formatter="html"))
    
    print(f"Livro adicionado ao {caminho_arquivo} com sucesso.")

# Função para remover o último livro adicionado na página /livros
def delete_article(caminho_arquivo='../Projeto Programação Web/app/templates/livros.html'):
    # Garante que o caminho é relativo ao diretório atual do script
    caminho_arquivo = os.path.join(os.getcwd(), caminho_arquivo)

    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
    
    # Lê o conteúdo do arquivo HTML
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        conteudo_html = arquivo.read()
    # Utiliza BeautifulSoup para parsear o HTML
    soup = BeautifulSoup(conteudo_html, 'html.parser')
    # Encontra todas as tags <article>
    articles = soup.find_all('article', class_='article')
    # Remove o último livro se houver algum
    if articles:
        last_article = articles[-1]
        last_article.extract()  # Remove a tag do HTML
    # Salva o HTML modificado de volta no arquivo com pretty print
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(soup.prettify(formatter="html"))
        
    print("Último livro removido com sucesso.")


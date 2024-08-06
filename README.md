Bibliotecas utilziadas:

    FastAPI         - pip install fastapi
    SQLAlchemy      - pip install sqlalchemy
    Uvicorn         - pip install uvicorn
    Starlette       - pip install starlette
    Os              - pip install os
    Flask           - pip install flask
    Bs4             - pip install bs4

Linguagens utilizadas:

    Python
    HTML
    CSS

Extensões:

    SQLite
    SQLite viwer

Funcionamento do Sistema (Backend):

    O nosso projeto se baseia no uso de Python (Bibliotecas: FastAPI e SQLAlchemy) e HTML+CSS para a criação de um site de uma biblioteca qualquer.

    O uso de FastAPI para a criação de métodos GET e POST foi essencial para o andamento do projeto. Aqui está um exemplo de API utilizada no sistema:

        @app.get("/", response_class=HTMLResponse)
            def read_home(request: Request):
                return templates.TemplateResponse("index.html", {"request": request})

    Esta API é o ENDPOINT mais básico do sistema, a qual direciona o usuário para a página Home do site.

    Desenvolvemos também, dois ENDPOINT's para adicionar e remover um livro em /livros. Consiste num sistema orientado a objetos que define a classe Livro e, com base nela, através de um formulário no página /livros, eles são adicionaos e removidos manipulando o arquivo livros.html.

    Abaixo estão os dois ENDPOINT's reponsáveis por isso:

        @app.post("/adicionar-livro", response_class=HTMLResponse)
            def adicionar_livro(nome: str = Form(...), autor: str = Form(...)):
                novo_livro = Livro(nome=nome, autor=autor)
                article_html = novo_livro.create_book()
                add_book(article_html, caminho_arquivo='../Projeto Programação Web/app/templates/livros.html')
                return RedirectResponse(url="/livros", status_code=303)

        @app.post("/delete-article", response_class=HTMLResponse)
            def delete_last_article():
                delete_article()
                return RedirectResponse(url="/livros", status_code=303)

    Os livros estão referenciados como "article" dentro das funções pois <artilce> é a tag HTML que foi utilizada para criar os espaços onde os livros são apresentados.

    O código com os devidos comentários está salvo no arquivo.

    O uso da Biblioteca SQLAlchemy nos possibilitou criar uma base de dados baseada totalmente em código python. Rodando num arquivo base.db, o banco de dados engloba as tabelas "Usuários" e "Livros", onde os usuários são armazenados conforme utilizam o sistema de cadastro do site. Abaixo está um exemplo de tabela criada para nosso projeto:

        __tablename__ = 'usuario'
    
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        nome: Mapped[str] = mapped_column(nullable=False)
        email: Mapped[str] = mapped_column(nullable=False)
        senha: Mapped[str] = mapped_column(nullable=False)
    
    Na utilização do Login, o sistema mapeia o banco de dados, mais especificamente a tabela "usuario", e verifica se existe um usuário com o email correspondente com o inserido na página, validando o email e a senha e encaminhando o usuário à página de sua conta, armazenando o email do usuário para a sessão. Caso a senha esteja incorreta, o sistema enviará uma mensagem de ERROR 400. Abaixo está o ENDPOINT responsável por esta ação:

        @app.post("/login/enviar", response_class=HTMLResponse)
        def login(request: Request, email: str = Form(...), senha: str = Form(...)):
            session = request.session

            user = read(email)
    
            if not user or user.senha != senha:
                raise HTTPException(status_code=400, detail="Credenciais inválidas")

            session['user_email'] = user.email
    
            return RedirectResponse(url="/conta", status_code=303)

    Os métodos responsáveis por criar as tabelas e inserir dados em base.db estão localizados no arquivo crud.py, na pasta CRUD. {CRUD/crud.py}.

Apresentação do Sistema (Frontend):

    Para a utilização do sistema num site iterativo, nós utilizamos HTML+CSS para integrar a estrutura de tags e estilos para o site.

    Criamos 4 páginas principais, as quais: Home, Livros, Autores, Cadastro, além de mais 2 páginas secundárias: Login e Conta. Armazenamos, junto às imagens utilizadas no site, os arquivos CSS na pasta /static/img e /static/css e as páginas HTML na pasta /app/templates.

    Home: página principal do site, onde são mostrados livros que serão adicionados em breve, autores mais populares e 
    recomendações de leitura.

    Livros: página que mostra o seu acervo, contém a sinopse (que não passam de 4 linhas) e os nomes dos autores de todos os livros.

    Autores: página com a missão de mostrar os autores (alguns, pois o arquivo ficaria muito grande se eu aumentasse ainda mais as páginas HTML) de suas obras.

    Cadastro: realizar o cadastro dos usuários com Nome, Email e Senha.

    Login: realizar o login dos usuários já cadastrados.

    Conta: mostra seu nome, foto (imagem de sua escolha) e suas obras favoritas.

Para a execução do sistema basta executar os arquivos: create.bd + models.py + database.py e, por último, main.py (nesta ordem).

Talvez quando o arquivo database.py for aberto ele apresente 2 erros de importação no código referentes à biblioteca Flask mas estes erros podem ser ignorados pois não interferem em nada na execução do código.

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from MODELS.models import Usuario
from CRUD.crud import create, read
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.sessions import SessionMiddleware
from livros import add_book, delete_article, Livro
import os # Import para DEBUG

# Conexão com o banco de dados SQLite
db = create_engine("sqlite:///base.db", echo=True)
Session = sessionmaker(bind=db)

# Conexão com FASTAPI
app = FastAPI()

# Senha do BD
SECRET_KEY = "12345"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Configuração para servir arquivos estáticos (CSS, imagens)
app.mount("/static", StaticFiles(directory="../Projeto Programação Web/static"), name="static")

# Configuração para refernciar o diretório de templates Jinja2
templates = Jinja2Templates(directory="app/templates")

# Rota para página inicial
@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para página de cadastro
@app.get("/cadastro", response_class=HTMLResponse)
def read_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})
 
# Endpoint para cadastro de usuário
@app.post('/cadastro/enviar', response_class=HTMLResponse)
def cadastro(nome:str = Form(...), email: str = Form(...), senha: str = Form(...)):
    usuario = [Usuario(nome=nome,email=email,senha=senha)]
    create(usuario)
    return RedirectResponse(url=f"/login", status_code=303)

# Rota para página de login
@app.get("/login", response_class=HTMLResponse)
def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Endpoint para login de usuário
@app.post("/login/enviar", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    # Obter a sessão
    session = request.session
    # Ler o usuário do banco de dados
    user = read(email)
    # Verificar se o usuário foi encontrado e se a senha está correta
    if not user or user.senha != senha:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    # Armazenar o email do usuário na sessão
    session['user_email'] = user.email
    # Redirecionar para a página conta
    return RedirectResponse(url="/conta", status_code=303)

# Rota para página de livros
@app.get("/livros", response_class=HTMLResponse)
def read_livros(request: Request):
    return templates.TemplateResponse("livros.html", {"request": request})

# Rota para página de autores
@app.get("/autores", response_class=HTMLResponse)
def read_autores(request: Request):
    return templates.TemplateResponse("autores.html", {"request": request})

# Rota para página conta
@app.get("/conta", response_class=HTMLResponse)
def read_conta(request: Request):
    return templates.TemplateResponse("conta.html", {"request": request})

# Rota para adicionar um livro em /livros
@app.post("/adicionar-livro", response_class=HTMLResponse)
def adicionar_livro(nome: str = Form(...), autor: str = Form(...)):
    # Cria um novo livro com os dados recebidos do formulário em /livros
    novo_livro = Livro(nome=nome, autor=autor)
    # Chama a função add_book para adicionar o livro em /livros
    article_html = novo_livro.create_book()
    add_book(article_html, caminho_arquivo='../Projeto Programação Web/app/templates/livros.html')
    # Redireciona para /livros
    return RedirectResponse(url="/livros", status_code=303)

# Rota para deletar o último livro adicionado em /livros
@app.post("/delete-article", response_class=HTMLResponse)
def delete_last_article():
    # Chama a função delete_article para excluir o último livro adicionado
    delete_article()
    # Redireciona para /livros
    return RedirectResponse(url="/livros", status_code=303)

# Execução do servidor usando Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7777)

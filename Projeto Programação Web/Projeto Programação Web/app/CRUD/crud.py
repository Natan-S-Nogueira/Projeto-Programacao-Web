from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MODELS.models import Usuario

# Conexão com Base de dados
db = create_engine("sqlite:///base.db", echo=True)

# Criar sessão para realizar operações de CRUD
 
Session = sessionmaker(bind=db)

# Operação de Escrita
def create(modelos):
    with Session() as s:
        for modelo in modelos:
            s.add(modelo)
        s.commit()

# Operação de Leitura
def read(user_email):
    with Session() as s:
        usuario = s.query(Usuario).filter(Usuario.email == f'{user_email}').first()
    return usuario

# Operação de Atualizar
def update(nome: str, email: str, senha: str):
    with Session() as s:
        usuario = s.query(Usuario).filter(Usuario.email == email).first()
        if usuario:
            usuario.nome = nome
            usuario.email = email
            usuario.senha = senha
            s.commit()
            s.refresh(usuario)
            return usuario
        return None

# Operação de Deletar
def delete(user_email: str):
    with Session() as s:
        usuario = s.query(Usuario).filter(Usuario.email == user_email).first()
        if usuario:
            s.delete(usuario)
            s.commit()
            return None
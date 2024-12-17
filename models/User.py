from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user
import sqlite3

database = 'database.db'

def obter_conexao():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self,nome, email, senha,):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.usu_id = None

    def get_id(self):
        return str(self.usu_id)

    @classmethod
    def get(cls, usu_id):
        conn = obter_conexao()
        SELECT = "SELECT * FROM usuario WHERE usu_id = ?"
        res = conn.execute(SELECT, (usu_id,))
        dados = res.fetchone()
        if dados:
            usuario = User(dados['nome'], dados['email'], dados['senha'])
            usuario.usu_id = dados['usu_id']
            return usuario
        return None

    @classmethod
    def get_by_email(cls,email):
        conn = obter_conexao()
        resultado = conn.execute("SELECT usu_id, nome, email, senha FROM usuario WHERE email = ?", (email,))
        dados = resultado.fetchone()
        if dados:
            usuario =User(dados['nome'], dados['email'], dados['senha'])
            usuario.usu_id =dados['usu_id']
            return usuario
        return None
    
    def save(self):
        conn = obter_conexao()  
        cursor = conn.cursor()    
        cursor.execute("INSERT INTO usuario(nome, email, senha) VALUES (?,?,?)", (self.nome, self.email, self.senha))
        # salva o id no objeto recem salvo no banco
        conn.commit()
        conn.close()
        return True

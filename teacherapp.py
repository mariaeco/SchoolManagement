from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from functions.manager import Escolas

teacherapp = Flask(__name__)

# Função para criar a conexão
def criar_conexao():
    host = 'localhost'
    user = 'maria_c'
    password = 'puffy2020'
    database = 'bdprojeto'  # Nome do banco de dados
    
    conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conexao

@teacherapp.route('/')
def index():
    return render_template('teacherpages/login.html')

@teacherapp.route('/teacherpages/login', methods=['GET','POST'])
def login():
    
    login = request.form.get('login')
    senha = request.form.get('senha')

    if login == 'maria' and senha == '1234':
        return render_template("teacherpages/startpage.html")
    else:
        return render_template('teacherpages/login.html')
    

@teacherapp.route('/teacherpages/startpage', methods=['GET','POST'])
def startpage():   
    return render_template('teacherpages/startpage.html')
    

@teacherapp.route('/teacherpages/view_classes')
def view_classes():
    conexao = criar_conexao()  # Substitua pela sua função para criar conexão
    cursor = conexao.cursor()

    turmas = Escolas(host='localhost', user='maria_c', password='puffy2020', database='bdprojeto')
    cursor.execute("SELECT * FROM turmas_professor")
    turmas = cursor.fetchall()
    resultados = cursor.fetchall()
    cursor.close()
    
    return render_template('teacherpages/view_classes.html', turmas=turmas)

    
    
if __name__ == "__main__":
    teacherapp.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from manager import Escolas

app = Flask(__name__)

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

# Rota para exibir as escolas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manager')
def manager():
    return render_template('manager/manager.html')
    
    
# Rota para adicionar uma nova escola
@app.route('/manager/newschool', methods=['GET','POST'])
def newschool():
    if request.method == "POST":
        codinep = request.form['codinep']
        nome = request.form['nome']
        gre = request.form['gre']
        salas = request.form['nsalas']
    
        conexao = criar_conexao()  # Criar conexão
        cursor = conexao.cursor()
        escolas = Escolas(host='localhost', user='maria_c', password='puffy2020', database='bdprojeto')
        comando = escolas.inserirEscola(codinep,nome, gre, salas)  # Chamando o método inserirEscola com os parâmetros
        cursor.execute(comando)
        conexao.commit()
        conexao.close()
        
        return redirect(url_for('manager'))  # Redirecionar para a página inicial após adicionar a escola
    return render_template('manager/newschool.html')  # Se o método não for POST, retornar o template para criar nova escola

@app.route('/manager/view_school')
def view_school():
    conexao = criar_conexao()  # Criar conexão
    cursor = conexao.cursor()
    escolas = Escolas(host='localhost', user='maria_c', password='puffy2020', database='bdprojeto')

    cursor.execute('SELECT * FROM escola')
    escolas = cursor.fetchall()
    conexao.close()
    return render_template('manager/view_school.html', escolas=escolas)

    
@app.route('/manager/view_student')
def view_student():
    conexao = criar_conexao()  # Substitua pela sua função para criar conexão
    cursor = conexao.cursor()
    alunos_escola = Escolas(host='localhost', user='maria_c', password='puffy2020', database='bdprojeto')
    cursor.execute("SELECT * FROM alunos_por_escola")

    # Recuperar os resultados da consulta
    alunos_escola = cursor.fetchall()

    # Fechar o cursor e a conexão
    cursor.close()
    return render_template('manager/view_student.html', alunos_escola=alunos_escola)


@app.route('/teacherpages/login', methods=['GET','POST'])
def login():
    
    login = request.form.get('login')
    senha = request.form.get('senha')

    if login == 'maria' and senha == '1234':
        return render_template("teacherpages/startpage.html")
    else:
        return render_template('teacherpages/login.html')
    

@app.route('/teacherpages/startpage', methods=['GET','POST'])
def startpage():   
    return render_template('teacherpages/startpage.html')
    

@app.route('/teacherpages/view_classes')
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
    app.run(debug=True)
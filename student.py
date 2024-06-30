#PARTE ACESSADA PELAS ESCOLAS - O GESTOR ESCOLAR E SECRETÁRIOS (MATRICULAR ALUNOS NAS TURMAS)
import sys
import os
import mysql.connector



class Matricula:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        print('\n------ Entrando no Sistema de Administração da Escola ------\n')
        
    
    def matricularAluno(self, cursor):
        self.inep = '25000100' #PARA FACILIDADE VOU ESCOLHER APENAS UMA ESCOLA PARA MONTAR
        max_aluno = 25 #maximo de 20 alunos por turma
        self.ano = '2024'
        print("Turmas Disponíveis:")
        #consulta = (f'SELECT serie, turma FROM serie WHERE codInep = {self.inep} AND ano = {self.ano}')
        consulta = (f"SELECT serie, GROUP_CONCAT(DISTINCT turma) AS turmas FROM serie WHERE codInep = {self.inep} AND ano = {self.ano} GROUP BY serie")
        cursor.execute(consulta)
        turmas = cursor.fetchall()

        for s, t in turmas:
            print("{:<10} {:<10}".format(s,t))
        
        print('\nDigite 1 para 1º ano, 2º para 2º ano ou 3 para 3º ano')   
        self.valor = int(input())
        if(self.valor == 1):
            self.serie = '1º ano'
        elif(self.valor == 2):
            self.serie = '2º ano'
        elif(self.valor == 3):
            self.serie = '3º ano'
        else:
            print("Série não existe")
            self.erro == 1
            input()
    
        for serie_str, turmas_str in turmas:
            if serie_str == self.serie:
               turma = turmas_str.split(',') if turmas_str else []  # Convertendo a string de turmas em uma lista, se houver turmas

        if turma:
            print(f"Escolha Turma do aluno ({', '.join(turma)}):")
        else:
            print("Não há turmas disponíveis para esta série.")      
        
        self.turma = input()
        
        cod_serie = self.buscarTurma(cursor, self.serie, self.turma, self.inep)
        consulta_sql = f'SELECT COUNT(*) FROM alunos WHERE cod_serie = {cod_serie}'
        cursor.execute(consulta_sql)
        n_alunos = cursor.fetchone()[0]      
        print("Numero de alunos matriculados: ", n_alunos)
        
        if n_alunos == max_aluno:
            print("Não há vagas na turma, escolha outra turma")
        else:
            registrado = 0
            self.nome = input("Digite o nome do aluno: ")
            while True:
                if registrado == 1:
                    self.nome = input("Digite um novo aluno: ")
                self.cpf = input("Digite o cpf do aluno: ")
                try:
                    # Verifica se o CPF tem exatamente 11 números
                    if len(self.cpf) != 11 or not self.cpf.isdigit():
                        raise ValueError("O CPF deve conter exatamente 11 números.")    
                    # Verifica se o CPF já existe no banco de dados
                    cursor.execute(f"SELECT COUNT(*) FROM alunos WHERE cpf = '{self.cpf}'")
                    if cursor.fetchone()[0] > 0:
                        registrado = 1
                        raise ValueError("Este CPF já está registrado. O aluno já está matriculado, matricule um novo aluno.")
                except ValueError as e:
                    print(e)
                else:
                    break # Se o CPF for válido, interrompo o loop
            self.comando = f'INSERT INTO alunos (cpf, nome, cod_serie) VALUES ({self.cpf},"{self.nome}",{cod_serie})'       
            return self.comando
                
    def buscarTurma(self, cursor, serie, turma, inep): #busca por codigo INEP
        cursor.execute('SELECT cod_serie FROM serie WHERE serie = %s AND turma = %s AND codInep = %s', (serie, turma, inep))
        self.resultado = cursor.fetchone()[0]   
        if self.resultado == None:
            print("Turma Não Encontrada")
            return 0
        else:         
            return self.resultado
     
 
    def verAluno():
        return 0

    def tranferirdeTurma():
        return 0
    
    def tranferirdeEscola(): #no caso o aluno vem de outra escola e puxo o cadastro dele da outra escola
        return 0
    
    def cancelarMatricula(): #no caso o aluno vem de outra escola e puxo o cadastro dele da outra escola
        return 0

    def menu(self):
        print("------ MENU ------")
        print("1. Matricular Aluno")
        print("2. Transferir Aluno de Turma")
        print("3. Transferir Aluno de Escola")
        print("4. Ver Aluno")
        print("5. Cancelar Matrícula")
        print("0. Sair")
    

if __name__ == "__main__":
    
    # Solicitar ao usuário as credenciais de acesso ao banco de dados
    host = 'localhost'
    user = 'maria_c '
    password = 'puffy2020'
    database = 'bdprojeto'  # Nome do banco de dados
    
    conexao = mysql.connector.connect(
        host = host,
        user =  user,
        password = password,
        database = database
    )
    
    cursor = conexao.cursor() # criando a conexao com o banco de dados
    aluno = Matricula(host,user,password,database)
    

    while True:
        os.system('cls')
        aluno.menu()
        choice = int(input('Digite a opcao desejada: '))
        os.system('cls')
        if choice == 1:
            aluno_matriculado = aluno.matricularAluno(cursor)
            cursor.execute(aluno_matriculado)   
            conexao.commit()
            print("\n Aluno matriculado com sucesso")
            input()
        elif choice == 2:
            boleana = aluno.transferenciaInterna(cursor)
            input()
        elif choice == 3:
            aluno.transferenciaExterna(cursor)
            input()
        elif choice == 4:
            aluno.imprimirAluno(cursor)
            input()
        elif choice == 5:
            aluno.cancelarMatricula(cursor)
            input()
        elif choice == 0:
            print("Encerrando o programa...")
            cursor.close()
            conexao.close()
            sys.exit()
        else:
            print("Opção inválida! Por favor, escolha novamente.")
            

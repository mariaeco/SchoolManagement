#PARTE ACESSADA PELAS ESCOLAS - O GESTOR ESCOLAR E SECRETÁRIOS (INSERÇÃO DE TURMAS, VISUALIZAÇÃO DE TURMAS)
import sys
import os
import mysql.connector



class Turmas:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        print('\n------ Entrando no Sistema de Administração das Escolas ------\n')
        
    
    def inserirTurma(self, cursor):
        self.inep = '25000100' #PARA FACILIDADE VOU ESCOLHER APENAS UMA ESCOLA PARA MONTAR
        self.ano = '2024'
        self.erro = 0
        
        consulta_sql = f'SELECT COUNT(*) FROM serie'
        cursor.execute(consulta_sql)
        ncadastradas = cursor.fetchone()[0] 
        
        consulta_sql = (f'SELECT n_salas FROM escola WHERE codInep = {self.inep}')
        cursor.execute(consulta_sql)
        salas = int(cursor.fetchone()[0])
        
        if ncadastradas >= salas:
            print("Limite de salas atingido!")
            input()
            #return sys.exit()
        else:
            print("\n------- ENTRANDO NA ATUALIZAÇÃO ESCOLAR ----------\n")
            print("Escolha Série para cadastrar:") # aqui preciso buscar em uma tabela de séries autorizadas pra a escola, quais podem ser criadas, mas fica para depois
            print("Digite 1 para  1º ano")
            print("Digite 2 para  2º ano")
            print("Digite 3 para  3º ano")
            valor = int(input())
            
            if valor not in [1, 2, 3]:
                print('Escola não autorizada a cadastrar a série ou série não existente!')
                return
            else:
                self.serie = f'{valor}º ano'
            
            if self.erro == 0:
                # Verificar turmas existentes para a série
                consulta_sql = f'SELECT COUNT(*) FROM serie'
                cursor.execute(consulta_sql)
                contagem = cursor.fetchone()[0]
                proxima_turma = 'A'
                if contagem == 0:
                    self.comando_serie = f'INSERT INTO serie (serie, turma, ano, codInep) VALUES ("{self.serie}","{proxima_turma}", "{self.ano}","{self.inep}")'     
                    print(f'Série {self.serie} - Turma {proxima_turma} inserida com sucesso!')
                    #nao coloco o cod_serie porque este indice está como autoincremento no sql
                else:
                    cursor.execute(f'SELECT turma FROM serie WHERE serie = "{self.serie}"')
                    self.turmas_existentes = set(row[0] for row in cursor.fetchall())

                    while proxima_turma in self.turmas_existentes:
                        proxima_turma = chr(ord(proxima_turma) + 1)
                    self.comando_serie = f'INSERT INTO serie (serie, turma, ano, codInep) VALUES ("{self.serie}","{proxima_turma}", "{self.ano}","{self.inep}")'     
                    print(f'Série {self.serie} - Turma {proxima_turma} inserida com sucesso!')
            
                return self.comando_serie
            
        return 0
            
            
    def buscaEscola(self, cursor, c_inep): #busca por codigo INEP
        self.cursor = cursor
        self.c_inep = c_inep
        query = "SELECT nome FROM escola WHERE codInep = %s"
        cursor.execute(query, (self.c_inep ,))
        self.resultado = cursor.fetchone()
        escola = self.resultado[0]
        return escola
      
    
    def imprimirTurmas(self, cursor):
        self.cursor = cursor
        comando = f'SELECT * FROM serie'
        self.cursor.execute(comando)
        self.turmasEscola = self.cursor.fetchall() #ler o banco de dados
        
        consulta_sql = f'SELECT COUNT(*) FROM serie'
        cursor.execute(consulta_sql)
        contagem = cursor.fetchone()[0]      
        
        print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format("Serie", "Turma", "Ano", "N.Matriculados","Vagas", "Escola"))
        print("=" * 75)
        for turma in self.turmasEscola:
            codserie, serie, turma, ano, codInep = turma #dados da turma
            consulta_sql = f'SELECT COUNT(*) FROM alunos WHERE cod_serie = {codserie}' #buscando a quantidade de alunos matriculados por turma
            cursor.execute(consulta_sql)
            n_alunos = cursor.fetchone()[0]      
            max_aluno = 25 #maximo de 20 alunos por turma
            vagas = max_aluno-n_alunos
            escola = self.buscaEscola(self.cursor, codInep) #buscando o nome da esola
            print("{:<10} {:<10}  {:<10}  {:<10} {:<10} {:<10}".format(serie, turma, ano, n_alunos,vagas, escola))
        print("Quantidade de turmas: ", contagem)
        

    def deletarTurma(self, cursor):
        self.query = "DELETE FROM serie WHERE cod_serie = %i serie  = %s AND turma = %s"
        print("Digite a série que deseja deletar:")
        print("Digite 1 para  1º ano")
        print("Digite 2 para  2º ano")
        print("Digite 3 para  3º ano")
        self.valor = int(input())
        
        if self.valor not in [1, 2, 3]:
            print('Série não existente!')
            return
        else:
            serie = f'{self.valor}º ano'
    
            print("Digite a turma que deseja deletar:")
            turma = input()
            # Verificar se a série e a turma existem na tabela
            cursor.execute('SELECT COUNT(*) FROM serie WHERE serie = %s AND turma = %s', (serie, turma))
            contagem = cursor.fetchone()[0]
            if contagem == 0:
                print('Não foi encontrada nenhuma turma correspondente.')
                return
            else:
                cursor.execute('DELETE FROM serie WHERE serie = %s AND turma = %s', (serie, turma))
                conexao.commit()
                print(f'Turma da série {serie}, turma {turma} deletada com sucesso!')                   

    def imprimirAlunos(self, cursor):
        
        while True:
            os.system('cls')
            print("------ MENU ------")
            print("1. Para ver os alunos de uma turma")
            print("2. Para ver todos os alunos da escola")
            print("0. Sair")
            self.choice = int(input('\nDigite a opcao desejada: '))
            os.system('cls')
            
            inep = "25000100" #para facilitar estou dentro da escola 25000100

            
            if self.choice == 1:
                print("Abaixo digite a série e turma que deseja verificar:")
                print("Digite 1 para  1º ano")
                print("Digite 2 para  2º ano")
                print("Digite 3 para  3º ano")
                valor = int(input())
                
                if valor not in [1, 2, 3]:
                    print('Série não existente!')
                    return
                else:
                    serie = f'{valor}º ano'
                    
                print("Digite a turma que deseja ver (A, B, C,...):")
                turma = input()
                query = f'SELECT cod_serie FROM serie WHERE codInep = "{inep}" AND serie = "{serie}" AND turma = "{turma}"'
                cursor.execute(query)
                codSerie = cursor.fetchone()[0]
            
                
                query2 = f'SELECT * FROM alunos WHERE cod_serie = {codSerie}'
                cursor.execute(query2)   
                turma_escolhida = cursor.fetchall()
                count = 0
                
                os.system('cls')
                print("-" * 45)                    
                print("{:<10} {:<10}".format(serie, turma))
                print("{:<10} {:<10}".format("Matricula", "Nome"))
                print("-" * 45)
                for aluno in turma_escolhida:
                    matr, cpf, nome, cod_serie = aluno
                    print("{:<10} {:<10}".format(matr, nome))
                    count += 1
                print("\n")
                print("Numero total de alunos: ", count)
                input()
                    
                
            elif self.choice == 2:
                query = f'SELECT * FROM serie WHERE codInep = {inep}'
                cursor.execute(query)
                turmas = cursor.fetchall()
                count = 0
                for row in turmas:
                    codSerie, serie, turma, ano, codInep = row
                    query = f'SELECT * FROM alunos WHERE cod_serie = {codSerie}'
                    cursor.execute(query)   
                    alunos = cursor.fetchall()
                    print("=" * 75)
                    print("{:<10} {:<10} {:<10}".format("SERIE", "TURMA","ANO"))
                    print("{:<10} {:<10} {:<10}".format(serie, turma, ano))
                    print("-" * 75)
                    print("{:<10} {:<10}".format("Matricula", "Nome"))
                    print("-" * 75)
                    for aluno in alunos:
                        matr, cpf, nome, cod_serie = aluno
                        print("{:<10} {:<10}".format(matr, nome))
                        count += 1
                    print("\n")
                print("Numero total de alunos: ", count)
                input()
            elif self.choice == 0:
                print("Encerrando o programa...")
                sys.exit()
            else:
                print("Opção inválida! Por favor, escolha novamente.")
        
          


    def buscarAluno(self, cursor):
        print("Digite o nome do aluno:")
        aluno = input()
        # Consulta SQL para selecionar alunos com nomes que começam com as letras fornecidas pelo usuário
        sql = "SELECT * FROM alunos WHERE nome LIKE %s"
        cursor.execute(sql, (aluno + '%',))
        # Exibir resultados
        resultados = cursor.fetchall()
        if not resultados:
            print("Nenhum aluno encontrado com esse nome.")
        else:
            print("{:<10} {:<40} {:<10} {:<10}".format("Matricula", "Nome", "Serie", "Turma"))
            print("=" * 75)
            for aluno in resultados:
                matricula, cpf, nome, cod_serie = aluno #dados da turma
                query = f'SELECT serie, turma FROM serie WHERE cod_serie = {cod_serie}'
                cursor.execute(query)
                self.resultado = cursor.fetchall()[0]
                serie = self.resultado[0]
                turma = self.resultado[1]
                print("{:<10} {:<40}  {:<10} {:<10}".format(matricula, nome, serie, turma))
        
        print(" ------ > apos essa etapa, fazer funcao para ver a matricula do aluno e buscar pela matricula seu boletim ou transferencia < --------")
        
    
            
    def menu(self):
        print("------ MENU ------")
        print("1. Inserir Turma")
        print("2. Listar turmas da escola")
        print("3. Deletar turmas da escola")
        print("4. Ver alunos matriculados")
        print("5. Buscar aluno")
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
    turmas = Turmas(host,user,password,database)
    
    while True:
        os.system('cls')
        turmas.menu()
        choice = int(input('Digite a opcao desejada: '))
        os.system('cls')
        
        if choice == 1:
            serie = turmas.inserirTurma(cursor)
            cursor.execute(serie)   
            conexao.commit()
            input()        
        elif choice == 2:
            boleana = turmas.imprimirTurmas(cursor)
            input()
        elif choice == 3:
            turmas.deletarTurma(cursor)
            input()
        elif choice == 4:
            turmas.imprimirAlunos(cursor)
            input()            
        elif choice == 5:
            turmas.buscarAluno(cursor)
            input()
        elif choice == 0:
            print("Encerrando o programa...")
            cursor.close()
            conexao.close()
            sys.exit()
        else:
            print("Opção inválida! Por favor, escolha novamente.")
            

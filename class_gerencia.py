#PARTE ACESSADA PELA GERENCIA DAS ESCOLAS - AS SECRETARIAS DE EDUCAÇÃO
import sys
import os
from class_serie import Turmas
from class_matricula import Matricula

class Escolas:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
    def inserirEscola(self, inep, nome, gre, nsalas):
        self.inep = inep
        self.nome = nome
        self.gre = int(gre)
        self.nsalas = int(nsalas)
        
        self.comando = f'INSERT INTO escola (codInep, nome, gre, n_salas) VALUES ({self.inep},"{self.nome}",{self.gre},{self.nsalas})'       
        
        return self.comando
        
    
    def imprimirEscolas(self, cursor):
        self.cursor = cursor
        comando = f'SELECT * FROM escola'
        self.cursor.execute(comando)
        escolasEstaduais = self.cursor.fetchall() #ler o banco de dados
        self.escolas = escolasEstaduais
        
        print("{:<10} {:<40} {:<10} {:<10}".format("CodInep", "Nome", "GRE", "Nº de salas"))
        print("=" * 75)
        for escola in self.escolas:
            codInep, nome, gre, numSalas = escola
            print("{:<10} {:<40} {:<10} {:<10}".format(codInep, nome, gre, numSalas))


            
    def buscaEscola(self, cursor, c_inep): #busca por codigo INEP
        self.cursor = cursor
        self.c_inep = c_inep
        
        query = "SELECT nome FROM escola WHERE codInep = %s"
        cursor.execute(query, (self.c_inep ,))
        self.resultado = cursor.fetchone()
        
        if self.resultado:
            print(f"Nome da escola com o código IDEB {self.c_inep}: {self.resultado[0]}")
        else:
            print(f"Nenhuma escola encontrada com o código IDEB {self.c_inep}")
            
        return self.resultado[0]
        
    def menu_atualizacao(self, cursor):
        print("\n------- ENTRANDO NA ATUALIZAÇÃO ESCOLAR ----------\n")
        print("1. Atualizar Nome da Escola")
        print("2. Atualizar GRE da Escola")
        print("3. Atualizar Número de Salas")
        print("0. Sair")
     
        while True:
            
            self.choice = int(input('\nDigite a opcao desejada: '))
            os.system('cls')
            
            self.codigoEscola = int(input('Qual escola deseja atualizar? (Digite o codigo do INEP) '))
            
            #buscar escola para imprimir na tela
            self.cursor = cursor
            self.buscaEscola(self.cursor, self.codigoEscola);
            
            input() 
            if self.choice == 1:
                self.atributo = 'nome'
                self.novo_valor = input('Digite o novo Nome: ')
            elif self.choice == 2:
                self.atributo = 'gre'
                self.novo_valor = input('Digite a nova gre: ')         
            elif self.choice == 3:
                self.atributo = 'n_salas'
                self.novo_valor = int(input('Digite o novo numero de salas: '))  
            elif self.choice == 0:
                print("Encerrando o programa...")
                sys.exit()
            else:
                print("Opção inválida! Por favor, escolha novamente.")
        
            return self.codigoEscola, self.atributo, self.novo_valor
        
    def atualizarEscola(self, cursor):
            self.cursor = cursor
            self.codEscola, self.atributo, self.novo_valor = self.menu_atualizacao(cursor)
            self.comando = f"UPDATE escola SET {self.atributo} = '{self.novo_valor}' WHERE codInep = {self.codEscola}"
             
            return self.comando
                
    def deletarEscola(self, cursor):
            self.query = "DELETE FROM escola WHERE codInep = %s"
            self.c_inep = int(input('Digite o codigo Inep da Escola que deseja deletar: '))
            
            self.cursor = cursor
            self.buscaEscola(self.cursor, self.c_inep);
            deletar = int(input('Tem certeza que deseja deletar? (1 - Sim; 0 - Cancelar deleção) '))
            if deletar == 1:
                return self.query, self.c_inep
            else:
                print("Escola não deletada")
                return 0

    def atributosEscola(self, cursor): 
        c_inep = input("Digite o codigo inep da escola que deseja: ")
        nomeEsc = self.buscaEscola(cursor, c_inep)
        
        cursor.execute('SELECT * FROM serie WHERE codInep = %s', (c_inep,)) #(c_inep,) pq sao apenas alguns elementos da serie
        self.resultado = cursor.fetchall()  
        
        total = 0
        if self.resultado: #BUSCANCO AS TURMAS DA ESCOLA E A QTD DE ALUNOS MATRICULADOS
            print("=" * 75)
            print("ESCOLA:      ", nomeEsc)
            print("=" * 75)
            print("{:<10} {:<10} {:<10} {:<10} {:<10}".format("CodSerie", "Serie", "Turma", "Ano", "NºAlunos"))
            print("=" * 75)
            for turmas in self.resultado:
                codserie, serie, turma, ano, codinep = turmas
                cursor.execute('SELECT COUNT(*) FROM alunos WHERE cod_serie = %s', (codserie,)) #(c_inep,) pq sao apenas alguns elementos da serie
                nalunos = cursor.fetchone()[0]  
                total += nalunos
                print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(codserie, serie, turma, ano,nalunos))
        else:         
            print("Escola não encontrada")             
        print("Total de alunos matriculados na escola", total)


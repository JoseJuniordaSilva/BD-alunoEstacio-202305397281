#  PARA USAR venv/Scripts/Activate
#            cd pytaxqtdesigner
#E RUN PYTHON CODE, na setinha ao lado e DEPOIS repetir o comando no terminal
# o titular é 'junior'
#a senha 'admin123'
# e Notas para croata e NotasMarlene para as de marlene
#se der problema, repita, pois ele sai do diretorio e localizar o arquivo 'C:/xmls/xmlAtual'
# ai importa e pronto
# *********************************************************************************** 

#aulas de 'sistema de gerenciamento com python' do pytax
"""PARA USAR
COM O database.py eu faço um novo database e um arquivo e i MAIN de NOTASdesafioHastag
  OBS : Nas linhas 175 e 221 é onde altero para aparecer na tela de tabelas, geral e base estoque """
from os import access
from typing import Optional
from PySide6.QtWidgets import(QApplication,QFileDialog,QMainWindow,QWidget,
                               QMessageBox,QTreeWidgetItem,QLabel,QLineEdit)  #QTreeWidgetItem
from PySide6 import QtCore
from PySide6.QtCore import Qt,QSize
from ui_login import Ui_login
from ui_main import Ui_MainWindow
import sys
from database import Database
from xml_files import Read_xml
import sqlite3
import pandas as pd
from PySide6.QtSql import QSqlDatabase,QSqlTableModel
import re
from datetime import date
import matplotlib.pyplot as plt

#def cria_empresa():

file_name = 'inicial'

class Login(QWidget,Ui_login):
    def __init__(self) -> None:
        super(Login,self).__init__()
        self.tentativas = 0
        self.setupUi(self)
        self.setWindowTitle("Login do Sistema")

        self.btn_login.clicked.connect(self.check_login)

   

      ##  self.btn_login.clicked.connect(self.open_sistem)

    #não vai mais usar, so no começo  se for o caso vai fazendo aos poucos
    # def open_sistem(self):
    #     if self.txt_password.text() == '123':
    #        self.w = MainWindow()
    #        self.w.show()
    #        self.close()
    #     else:
    #        print("Senha invalida")
    
    

    def check_login(self):
        self.users = Database()
        self.users.conecta()
        autenticado = self.users.check_user(self.txt_user.text(),self.txt_password.text())
       
        file_name = self.txt_empresa.text()
        print('*****************',file_name)

        if autenticado.lower() == 'administrador' or autenticado.lower() == 'user':
            #self.w = MainWindow(autenticado.lower())
            self.w = MainWindow(self.txt_user.text(), autenticado.lower(),file_name)            
            self.w.show()
            self.b = bbb(file_name)             # EXPERIMENTO chama a classe bbb la no final linha 361
            self.j = Database.traz_empre(file_name)   # chma a classe em database e la o nome nao interessa
           
            self.close()
       

        else:
            if self.tentativas < 3:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle('Erro ao acessar')
                msg.setText(f'Usuario ou senha incorreto \n \n Tentativas: {self.tentativas + 1} de 3')
                msg.exec()
                self.tentativas += 1
            if self.tentativas == 3:
                #bloquear o sistema
                self.users.close_conn
                sys.exit(0)


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,user,username,file_name) -> None:
  ##  def __init__(self,user,username) -> None:
    #def __init__(self) -> None:
        super(MainWindow,self).__init__()

        self.setupUi(self)
        #self.setWindowTitle("Sistema de Gerenciamento")
        self.setWindowTitle(f"Sistema de Gerenciamento de {file_name}")
        
        global empresa
        empresa = file_name     # levei pra linha 245 pra ver na tela
        
        self.user = username
        if user.lower() == 'user':
            self.btn_pg_cadastro.setVisible(False)
 

# #==========paginas do sistema----------
        self.btn_home.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pg_home))
        self.btn_importa.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pg_import))
        self.btn_tables.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pg_table))
        self.btn_contato.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pg_contato))
        self.btn_sobre.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pg_sobre))
        self.btn_pg_cadastro.clicked.connect(lambda:self.Pages.setCurrentWidget(self.pg_cadastro))
#         #chamar a funcao
        self.btn_cadastrar.clicked.connect(self.subscribe_user)

#         #arquivos xml
        self.btn_open.clicked.connect(self.open_path)
        self.btn_import.clicked.connect(self.import_xml_files)

        #Filtro
        self.txt_filtro.textChanged.connect(self.update_filter)

        #gerar saida e estorno
        self.btn_gerar.clicked.connect(self.gerar_saida)
        self.btn_estorno.clicked.connect(self.gerar_estorno)

        self.btn_excel.clicked.connect(self.excel_file)

        self.btn_chart.clicked.connect(self.grafic)

        self.reset_table()


    def subscribe_user(self):
        if self.txt_senha.text() != self.txt_senha2.text():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Senhas diferentes")
            msg.setText('A senha nao é igual')
            msg.exec()
            return None
        
        nome = self.txt_nome.text()
        user = self.txt_usuario.text()
        password = self.txt_senha.text()
        access = self.cb_perfil.currentText()

        db = Database()
        db.conecta()

        db.insert_user(nome,user,password,access)
        db.conn.close()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Cadastro de Usuarios")
        msg.setText('Cadastro realizado com SUCESSO')
        msg.exec()

        self.txt_nome.setText("")
        self.txt_senha.setText("")
        self.txt_senha2.setText("")
        self.txt_usuario.setText("")

    def open_path(self):
        self.path = QFileDialog.getExistingDirectory(self, str("Open Directory"),
                                       "/home",
                                       QFileDialog.ShowDirsOnly
                                       | QFileDialog.DontResolveSymlinks)
        
        self.txt_file.setText(self.path)
    
    def import_xml_files(self):
        xml = Read_xml(self.txt_file.text())
        all = xml.all_files()
        self.progressBar.setMaximum(len(all))

        db = Database()
        db.conecta()
        cont =1
        for i in all:
            self.progressBar.setValue(cont)
            fullDataset = xml.nfe_data(i)
            db.insert_data(fullDataset)
            cont += 1
        #atualizar a tabela
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Importação de XML")
        msg.setText("Importação concluida")
        msg.exec()
        self.progressBar.setValue(0)

        db.close_conn()
        
    def table_estoque(self):
       
        #self.tw_estoque.setStyleSheet("color:#fff; font-size:15px;")
        self.tw_estoque.setStyleSheet(u" QHeaderView{color:black};color:black; font-size:15px;")

        cn = sqlite3.connect("system.db")
        result = pd.read_sql_query(f"SELECT * FROM Notas_Marlene WHERE data_saida = ''",cn)     #alterei Notas_Marlene
        result = result.values.tolist()
        #print(result)
        self.x = ""
        self.campo = ""
        for i in result:
            #checa a nota se é mais de uma vez e adiciona outro nivel
            if i[0] == self.x:
                QTreeWidgetItem(self.campo, i)
            else:
                self.campo = QTreeWidgetItem(self.tw_estoque, i)              
                self.campo.setCheckState(0,Qt.CheckState.Unchecked)
            self.x = i[0]
        self.tw_estoque.setSortingEnabled(True)
        for i in range(1,15):
            self.tw_estoque.resizeColumnToContents(i)

    def table_saida(self):
        self.tw_saida.setStyleSheet(u" QHeaderView{color:black};color:black; font-size:15px;")

        cn = sqlite3.connect("system.db")
        result = pd.read_sql_query("""SELECT Nfe,data_importacao,data_saida,usuario FROM Notas WHERE data_saida != ''""",cn)
        result = result.values.tolist()
        for rr in result:
            print(rr)
        self.x = ""
        self.campo = ""
        for i in result:
            ##checa a nota se é mais de uma vez e adiciona outro nivel
            if i[0] == self.x:
                QTreeWidgetItem(self.campo, i)
            else:
                self.campo = QTreeWidgetItem(self.tw_saida, i)              
                self.campo.setCheckState(0,Qt.CheckState.Unchecked)
            self.x = i[0]
        self.tw_saida.setSortingEnabled(True)
        for i in range(1,15):
            self.tw_saida.resizeColumnToContents(i)
    def table_geral(self):
     
        print('em geral            ',empresa)  # trouxe da 96
  
        self.tb_geral.setStyleSheet(u" QHeaderView{color:black};color:black; font-size:15px;")
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName("system.db")
        db.open()

        self.model = QSqlTableModel(db=db)
        self.tb_geral.setModel(self.model)
        self.model.setTable(f'{empresa}')     #alterei Notas_Marlene  TROUXE DA LINHA 96
        self.model.select()

    def reset_table(self):
        self.tw_estoque.clear()
        self.tw_saida.clear()

        self.table_saida()
        self.table_estoque()
        self.table_geral()

    def update_filter(self,s):
        s = re.sub("[W_]+", "",s)
        filter_str = 'Nfe LIKE "%{}%"'.format(s)
        self.model.setFilter(filter_str)

    def gerar_saida(self):
        self.checked_items_out = []
        def recurse(parent_item):
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                grand_child = child.childCount()
                if grand_child > 0:
                    recurse(child)
                if child.checkState(0) == Qt.Checked:
                    self.checked_items_out.append(child.text(0))
        recurse(self.tw_estoque.invisibleRootItem())
        #pergnta se o usuario deseja a dar a saida
        self.question("saida")
    def gerar_estorno(self):
        self.checked_items = []
        def recurse(parent_item):
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                grand_child = child.childCount()
                if grand_child > 0:
                    recurse(child)
                if child.checkState(0) == Qt.Checked:
                    self.checked_items.append(child.text(0))
        recurse(self.tw_saida.invisibleRootItem())
        #pergnta se o usuario deseja a dar a saida
        self.question("estorno")
    def question(self, table):
        msgBox = QMessageBox()
        if table == "estorno":
            msgBox.setText("Deseja estornar as Nfes Selecionadas?")
            msgBox.setInformativeText("As selecionadas voltarão para o estorno \n clique em YES para confirmar")
            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            msgBox.setDetailedText(f'Notas:{self.checked_items}')

        else:
            msgBox.setText("Deseja gerar saida as Nfes Selecionadas?")
            msgBox.setInformativeText("As notas abaixo serão baixadas no estoque \n clique em YES para confirmar")
            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            msgBox.setDetailedText(f'Notas:{self.checked_items_out}')
        msgBox.setIcon(QMessageBox.Question)
        ret = msgBox.exec()
        
        if ret == QMessageBox.Yes:
            if table == "estorno":
                self.db = Database()
                self.db.conecta()
                self.db.update_estorno(self.checked_items)
                self.db.close_conn()
                self.reset_table()
            else:
                data_saida = date.today()
                data_saida = data_saida.strftime("%d/%m/%Y")
                self.db = Database()
                self.db.conecta()
                self.db.update_estoque(data_saida,self.user,self.checked_items_out)
                self.db.close_conn()
                self.reset_table()

    def  excel_file(self):
        cnx = sqlite3.connect("system.db")
        result = pd.read_sql_query("SELECT * FROM Notas",cnx)
        result.to_excel("Resumo de Notas.xlsx", sheet_name="Notas",index=False)
     

        msgBox = QMessageBox()
    
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Relatório de Notas")
        msgBox.setText("Relatorio gerado com sucesso")
        msgBox.exec()

    def grafic(self):
        cnx = sqlite3.connect("system.db")
        estoque = pd.read_sql_query("SELECT * FROM Notas",cnx )
        saida = pd.read_sql_query("SELECT * FROM Notas WHERE data_saida != ''",cnx)
        #eu = pd.read_
        estoque = len(estoque)
        saida = len(saida)

        labels = "Estoque","Saidas"
        sizes = [estoque,saida]
        fig1,axl = plt.subplots()
        axl.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
        axl.axis("equal")

        plt.show()


## chamada em init da MainWindow  autenticao linha 63
class bbb():
    def __init__(self,empresa) -> None:
        print('viva a espiritualidade superior    ',empresa)        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()
    


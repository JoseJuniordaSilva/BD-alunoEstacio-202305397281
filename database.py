"""no INSERT_DATA fiz alterações para colher em uma variavel a empresa"""
import sqlite3


empresa = 'mmm'
outra_varia = 'blabla'
class Database():
    def __init__(self,name = "system.db") -> None:
        self.name = name
   #******************************************* TESTES
    def traz_empre(maria):       #CHAMADA EM MAIN.PY NA LINHA 64 
        print('um ',maria)  
        global empresa    
        empresa =  maria
        print('    olá       ',empresa)
        #return empresa      #VER AULA 'Escopo de Variáveis no python - Transferindo valores entre funções' DE 
                              # rorampy   COMO importo e crio uma variavel=database.traz_empre()
        Database.pra_ver(empresa)
   #******************************************* TESTES ATE AQUI        
    def pra_ver(jose):
        print('pra ver ',jose)
        print('outra pra ver ',empresa)

   

    #************************************************************************
    
    
    def conecta(self):
        self.conn = sqlite3.connect(self.name)
    
    def close_conn(self):
        try:
            self.conn.close()
        except:
            pass
  #criar tabela user
    def create_table_users(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""  
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    user TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    access TEXT NOT NULL);        """)
            #self.conn.commit()
           
            #cursor.execute("""  
            #    CREATE TABLE IF NOT EXISTS users('
            #        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            #        nome TEXT NOT NULL,
            #        user TEXT UNIQUE NOT NULL,
            #        password TEXT NOT NULL,
            #        access TEXT NOT NULL');        """)
           
        except AttributeError:
            print('Faça a conexão')
 #inserir dados
    def insert_user(self,nome,user,password,access):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO users(nome,user,password,access) VALUES (?,?,?,?)
                """,(nome,user,password,access))
            self.conn.commit()
        except AttributeError:
            print("Faça a conexão")
# #checar o usuario
    def check_user(self,user,password):
       try:
            cursor = self.conn.cursor()
            cursor.execute(""" 
                SELECT * FROM users;
              """)
          
            for linha in cursor.fetchall():              
                if linha[2].upper() == user.upper() and linha[3] == password and linha[4] == 'Administrador':              
            #    if linha[2].upper() == user.upper():
                    print('OI')
                    return "Administrador"
                   
                elif linha[2].upper() == user.upper() and linha[3] == password and linha[4] == 'Usuario':
                    return "User"
                else:
                    continue
            return "Sem acesso"
       except:
            pass
    
    #def insert_data(self,full_dataset):
    def insert_data(self,full_dataset):
        print('acertei ',empresa)
        cursor = self.conn.cursor()
        campos_tabela = (
            'NFe','serie','data_emissao','chave','cnpj_destinatario','nome_destinatario','valorNfe','itemNota','cod','qntd','descricao','unidade_medida','valorProd','data_importacao','municipio','usuario','data_saida'
        )
        qntd = ','.join(map(str,'?'*17))  # equivale a dezesseis vezer '?,?,? etc
        query = f""" INSERT INTO {empresa} {campos_tabela} VALUES ({qntd})"""   # alterei Notas
    #    query = f""" INSERT INTO Notas_Marlene {campos_tabela} VALUES ({qntd})"""   # alterei Notas
        try:
            for nota in full_dataset:
                print(nota)
                cursor.execute(query,tuple(nota))
                self.conn.commit()
        except sqlite3.IntegrityError:
            print("Nota ja existe no banco")

    def create_table_nfe(self):
        #MUDEI DE TEXT PARA INTEGER O valorNfe
        # E mudei CREATE TABLE IF NOT EXISTS Notas
        cursor = self.conn.cursor()                                       #alterei Notas pra Notas_Marlene 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notas_Marlene(   
                       NFe TEXT,
                       serie TEXT,
                       data_emissao TEXT,
                       mes TEXT,
                       chave TEXT,
                       cnpj_destinatario TEXT,
                       nome_destinatario TEXT,
                       valorNfe INTEGER,
                       itemNota TEXT,
                       cod TEXT,
                       qntd INTEGER,
                       descricao TEXT,
                       unidade_medida TEXT,
                       valorProd INTEGER, 
                       data_importacao TEXT,
                       municipio TEXT,
                       usuario TEXT,
                       data_saida TEXT,
                       PRIMARY KEY(chave,Nfe,itemNota)                       
            )  """)
        
    def update_estoque(self,data_saida,user,notas):
        try:
            cursor = self.conn.cursor()                    #alterei Notas pra marlene e em main.table_estoque()
            for nota in notas:
                cursor.execute(f"""UPDATE Notas_Marlene set data_saida = '{data_saida}', usuario = '{user}' WHERE Nfe = '{nota}' """)
                self.conn.commit()

        except AttributeError:
            print("Faça a conexão, para alterar campos")
            

    def update_estorno(self,notas):
        try:
            cursor = self.conn.cursor()
            for nota in notas:
                cursor.execute(f"UPDATE Notas set data_saida = '' WHERE Nfe = '{nota}' ")
                self.conn.commit()

        except AttributeError:
            print("Faça a conexão, para alterar campos")
            
   
if __name__ == "__main__":
    db = Database()
    db.conecta()
    ##db.check_user('junior','admin123')
    #db.create_table_users()
    db.create_table_nfe()
    db.close_conn()


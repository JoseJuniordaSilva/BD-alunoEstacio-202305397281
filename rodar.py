#  PARA USAR venv/Scripts/Activate
#E RUN PYTHON CODE, na setinha ao lado e DEPOIS repetir o comando no terminal
# e Notas para croata e NotasMarlene para as de marlene
# *********************************************************************************** 


"""usar este programa com o main para colocar dados no sqlite, retirando os ja existentes ou colocando novos pois ele nao repete o que ja esta la (ver em ) e assim poderei rodar o mesmo ate o fim do ano"""
import os
import pandas as pd
import datetime as dt
import sqlite3
import plotly.express as px   #usado nos graficos, tem que instalar pip install plotly



#criar a conexao
class Database():
    def __init__(self, name = "system.db") -> None:
        self.name = name

    def conecta(self):
        self.conn = sqlite3.connect(self.name)
    
   # def close_conn(self):
    #    try:
        self.conn.close()
     #   except:
      #      pass
        

if __name__ == "__main__":
   # db = Database()
   # db.conecta()
    cn = sqlite3.connect("system.db")
    
    FILE_NAME = str(input("Em qual arquivo? Notas ou Notas_Marlene "))
    cursor = cn.cursor()
    cursor.execute(f"SELECT * FROM {FILE_NAME}")         #alterei Notas pra Notas_Marlene 
    #help()
    dados_lidos = cursor.fetchall()
    #nome_mes = (dados_lidos[2]) 
    #print(nome_mes)
  
  
#******************************
#VER AULA 387 SQlite para deletar e praDeletar.py


    for i in dados_lidos:
        
####        print('aqui ',i[0],i[2],i[5],i[6])  # so as datas e os nomes ou qualquer coisa e/ou so um pedaço da data no caso o mes
####        print('mes ',i[0],i[2][3:5])  # so as datas e os nomes ou qualquer coisa e/ou so um pedaço da data no caso o mes
          
        #atualizar o campo mes com o mes em texto
       cursor.execute(f"UPDATE {FILE_NAME} SET mes = '{i[2][3:5]}' where NFe = '{i[0]}'") #alterei Notas    
       cn.commit()  
                                                                        #pra Notas_Marlene 
    
    result = pd.read_sql_query(f"SELECT * FROM {FILE_NAME}",cn) #alterei Notas pra Notas_Marlene 
#    result = pd.read_sql_query(f"SELECT * FROM {FILE_NAME} where NFe = %1",cn) #alterei Notas pra Notas_Marlene 
    ###result = pd.read_sql_query("SELECT * FROM Notas_Marlene",cn) #alterei Notas pra Notas_Marlene 
 #   print(f'Result {type(result)}')
   # result = pd.read_sql_table("Notas",'sqlite3://systema.db')
    #result = result.values.tolist()
    #print(len(result))
    #print(result[["chave","nome_emitente","municipio"]])
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
 

    df = pd.DataFrame()
    #.groupby('municipio').sum()
    df= df._append(result)
    ########print(df)
    #print(df[['NFe','serie',('valorNfe').replace(',','.'),'municipio']])
   
    #pm = df.groupby('municipio')[["serie","valorProd"]].sum()

# por mumicipio    pm = df.groupby(['municipio','data_emissao'])['valorNfe'].sum()  # NAO NAO soma com valorProd porque NÃO É INTEGER e valorNfe É INTEGER

#por mes
    pm = df.groupby(['mes','municipio','valorNfe','valorProd'])['qntd'].sum()  # NAO NAO soma com valorProd porque NÃO É INTEGER e valorNfe É INTEGER   POR MES(mes)
    #pm = pm[['valorNfe']].sort_values(by='valorNfe')
    print(pm)

#por mes/Quantidade
    pmq = df.groupby(['mes'])['qntd'].sum()     # pro ral  *20
    print("POR MES QUANTIDADE ===================")
    print(pmq)
#por mes/ valor
    pmvr = df.groupby(['mes'])['valorNfe'].sum()
    print('POR MES VALORES=======================')
    print(pmvr)

    #por clientes
    pc = df.groupby(['nome_destinatario','NFe','valorNfe','valorProd'])['qntd'].sum() 
    print("POR CLIENTES==========================")
    print(pc)

    #soma quantidade por cliente 
    
    sqpc = df.groupby(['nome_destinatario'])['qntd'].sum()*20 #litros 
    print("POR CLIENTES QUANTIDADE===================================(litros)")
    print(sqpc)

    #soma valor nfe por cliente 
    svpc = df.groupby(['nome_destinatario'])['valorNfe'].sum() 
    print('POR CLIENTES VALORES===================')
    print(svpc)

    #por cidades/ valor
    pcvr = df.groupby(['municipio'])['valorNfe'].sum()
    print('POR cidades VALORES=======================')
    print(pcvr)
    
    #por cidades/ quantidades de garrafas
    pcvr = df.groupby(['municipio'])['qntd'].sum()
    print('POR cidades QUANTIDADES DE GARRAFPES===============este para ver quantos vendeu========')
    print(pcvr)



    #achar samanda dupla
    nome_samanda = df.groupby(['nome_destinatario','NFe','cnpj_destinatario','data_emissao','qntd'])['valorNfe'].sum()

    # nome_samanda.to_excel("junior.xlsx")  #criando um arquivo excel
    
    pd.set_option('display.max_rows',None) 
    """ para nao truncar e ver apenas tantas linhas ,. visto na busca 'display.max_columns'  posso pasar (None ou o tanto de linha que quero ver) para ilimitado pode ser tambem max_coluns    OU ('displa.max_colwidht') para ver a coluna inteira 
    VER DOCUMENTAÇÃO
    """
    juntar_nome_samanda_pmq = pd.concat([pmq,nome_samanda])
   

    print(nome_samanda)  # é o ultimo e sera gravado no arq python/samandaNfe.txt
    print("Por mes ----------------------------")
    print(pmq)

    caminho_arquivo = 'c:\\python\\'   # cria  nesta pasta
    caminho_arquivo += 'samandaNfe.txt'  # ele cria o arquivo em branco
    with open(caminho_arquivo, 'w') as arquivo:
         arquivo.writelines(
        str(juntar_nome_samanda_pmq)
        #str(nome_samanda)
        #('linha 3\n','linha 4\n')
    )


    print('*'*30)
    print('DATAS')
    datas = dt.date(2024,2,18)
    mes = datas.month
    print(f'O mes {mes} e o ctime {datas.ctime()}')
    agora = dt.datetime.now()
    print(agora)
    agora_string = agora.strftime('%A %d %B %Y')
    print(agora_string)
    volta_data = dt.datetime.strptime(agora_string,'%A %d %B %Y')
    print(volta_data)

    cn.close()
    #db.close_conn()

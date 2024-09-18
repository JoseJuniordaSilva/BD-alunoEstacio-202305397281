import os
import xml.etree.ElementTree as Et    #para  parsear o xml
from datetime import date


class Read_xml():
    def __init__(self,directory) -> None:
        self.directory = directory

    def all_files(self):
        return [os.path.join(self.directory,arq) for arq in os.listdir(self.directory) if arq.lower().endswith(".xml")]
    def nfe_data(self,xml):    # onde ele vai buscar os dados
        root = Et.parse(xml).getroot()
        #print(root.tag)
        nsNFe = {"ns": "http://www.portalfiscal.inf.br/nfe"}
        
        #dados nfe
        NFe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF",nsNFe))
        #print(Nfe.upper())
        serie = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie",nsNFe))
        data_emissao = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi",nsNFe))
        data_emissao = f"{data_emissao[8:10]}/{data_emissao[5:7]}/{data_emissao[:4]}"

        #dados emitente
        chave = self.check_none(root.find("./ns:protNFe/ns:infProt/ns:chNFe",nsNFe))
        cnpj_destinatario = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:CNPJ",nsNFe))
        nome_destinatario = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:xNome",nsNFe))
        municipio = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:dest/ns:enderDest/ns:xMun",nsNFe))

        cnpj_destinatario = self.format_cnpj(cnpj_destinatario)
        valorNfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF",nsNFe))
        data_importacao = date.today()
        data_importacao = data_importacao.strftime("%d/%m/%Y")
        data_saida = ''
        usuario = ''

        itemNota = 1
        notas = []

        for item in root.findall("./ns:NFe/ns:infNFe/ns:det",nsNFe):
            #dados dos itens
            cod = self.check_none(item.find(".ns:prod/ns:cProd",nsNFe))
            qntd = self.check_none(item.find(".ns:prod/ns:qCom",nsNFe))
            descricao = self.check_none(item.find(".ns:prod/ns:xProd",nsNFe))
            unidade_medida = self.check_none(item.find(".ns:prod/ns:uCom",nsNFe))
            valorProd = self.check_none(item.find(".ns:prod/ns:vProd",nsNFe))     
            
            dados = [NFe,serie,data_emissao,chave,cnpj_destinatario,nome_destinatario,
                     valorNfe,itemNota,cod,qntd,descricao,unidade_medida,valorProd,data_importacao,
                     municipio,usuario,data_saida]
            #dados = [data_importacao]
            notas.append(dados)
            itemNota +=1
            #print(notas)
        return notas

    #checa se for  vazio
    def check_none(self,var):
        if var == None:
            return ""
        else:
            try:
                return var.text    # botar depois .replace(".",",")
            except:
                return var.text 

    def format_cnpj(self,cnpj):
        try:
            cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
            return cnpj
        except:
            return ""


if __name__ == "__main__":
    xml = Read_xml("C:\\xmls\\xmlAtual")
    all = xml.all_files()
    print(xml.nfe_data(all[0]))
    for i in all:
        result = xml.nfe_data(i)

        print(f'ola junior {result}')

#C:\xmls\notasEstudos

import pymongo
from datetime import datetime

cliente = pymongo.MongoClient('mongodb://localhost:27017/')
banco = cliente['contatosRealizados']
tabela = banco['estados']
acesso = banco['acesso']

def cadastraEstado(telefone, estado):
    contato = {}
    contato["phone"] = telefone
    contato["estado"] = estado
    
    procurar = { "phone": telefone }
    novoValor = { "estado": estado }

    x = tabela.update_one(procurar, {'$set': novoValor}, upsert=True)
    print('Registro inserido {0}'.format(x.matched_count))

def procurarEstado(numero):
    queryStr = {}
    queryStr['phone'] = numero
    result = tabela.find_one(queryStr)
    print('### DEBUG ### {0}'.format(result))
    if result == None:
        return 0
    else:
        return result['estado']

def contar(numero):
    queryStr = {}
    queryStr['phone'] = numero
    result = tabela.count_documents(queryStr)
    print('Telefones encontrados: {0}'.format(result))
    return result

#def validaPedido(Npedido): 

def cadastraToken(token):
    dadosToken = {}
    dadosToken["token"] = token
    acesso.drop()
    acesso.insert_one(dadosToken)
    
    for i in acesso.find():
        print(i)

def recuperaToken():
    return acesso.find_one()['token']  

def arrumaData(data):
    #Thu, 29 Nov 2018 20:11:05 GMT
    dia = int(data[5:7])
    mes = data[8:11]
    ano = int(data[12:16])
    hora = int(data[17:19])
    minuto = int(data[20:22])

    def retornaMes(mes):
        dicMes = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        for k, v in dicMes.iteritems():
            if mes == k:
                return int(v)

    data = datetime(ano, retornaMes(mes), dia, hora, minuto)

    return data
    

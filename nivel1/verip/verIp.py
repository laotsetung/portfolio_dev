import requests, json, time
import sys
from geopy.geocoders import Nominatim #lib para buscar endereço por latitudexlongitude

#VARIAVEIS
app = Nominatim(user_agent="tutorial")

#regatar o IP que foi passado como argumento
arg=None


nomes_col = ['IP           ','Continente   ','Pais         ',
             'Longitude    ','Latitude     ','Rua          ',
             'Cidade       ','Estado       ','Requisições  ']

nomes_col2 = ['IP           ','Continente   ','Pais         ',
             'Longitude    ','Latitude     ','Requisições  ']

r2 = [] #array com o resultado das informações
p = [0,1,2,3] #verificar ip
contador = 0

#FUNÇÕES
#Baixei essa funcao já pronta, ela simplesmente tenta recuperar os dados da lib geopy
#se não consegue ela invoca ela mesma outra vez, eu inclui um contador para fazer isso no maximo 5x
def get_address_by_location(latitude, longitude, language="en"):
    coordinates = f"{latitude}, {longitude}"
    print('Tentado coletar mais dados...')
    contador += 1
    if (contador>5):
        return None
    time.sleep(1)
    try:
        return app.reverse(coordinates, language=language).raw
    except:
        get_address_by_location(latitude, longitude)

#funcao que vai mostrar os dados no console
def mostraDados(resultado):
    z=0
    for x in resultado:
        if(len(resultado)>6): #nas duas opções com mais ou menos data
            print(nomes_col[z] + ' : ' +str(x))
        else:
            print(nomes_col2[z] + ' : ' +str(x))
        z+=1

#INICIO CODIGO
if(len(sys.argv) > 1): #verifica se um ip foi passado na chamada, se sim armazena,se não finaliza
    arg = sys.argv[1]
else:
    print(' ')
    print(' ---- ERRO ----')
    print('Argumento IP faltando')
    quit()

if(arg==None): #ip valido?
    print(' ')
    print(' ---- ERRO ----')
    print('Argumento IP faltando')
    quit()
else: #Verificando se é um IP válido
    parte = arg.split('.')
    try:
        p[0] = int(parte[0])
        p[1] = int(parte[1])
        p[2] = int(parte[2])
        p[3] = int(parte[3])

        if(p[0] > 255 or p[1] > 255 or p[2] > 255 or p[3] > 255):
            print(' ')
            print(' ---- ERRO ----')
            print('IP INVÁLIDO')
            quit()
    except:
        print(' ')
        print(' ---- ERRO ----')
        print('IP INVÁLIDO')
        quit()

url = 'http://ipwhois.app/json/'+arg

#tentando REQUEST
try:
    result = requests.get(url) #um metodo usando requests
except:
    print(' ')
    print(' ----- ERRO ------')
    print('Problemas para fazer o REQUEST, possível problema de conexão')
    quit()

print('Requerindo JSON com dados do IP')

z=0
print('Aguardando conexão') #Aguardando status_code == 200, aguardar no maximo 10x
while result.status_code != 200:
    time.sleep(0.5)
    if(z>10):
        break
    z+=1
    continue

if (result.status_code == 200):
    try:
        #tenta resgatar os dados do json e depois armazena todos numa variavel r2
        r = result.json()
        ip = r['ip']
        continente = r['continent']
        pais = r['country']
        codigo_tel = r['country_phone']
        long = str(r['longitude'])
        lat = str(r['latitude'])
        fuso = r['timezone_gmt']
        reqts = str(r['completed_requests'])
        print('Feito')

        #usando segunda lib para pegar dados exatos da localizacao
        try:
            address = get_address_by_location(lat, long)
            if (address is not None):
                end = address['address']
                rua = end['road']
                cidade = end['city']
                estado = end['state']
                r2 = [ip,continente,pais,long,lat,rua,cidade,estado,reqts]
        except:
            r2 = [ip,continente,pais,long,lat,reqts]

        #Poderia também fazer uma dict dos dados
        #dic1 = {'Pais:':pais,'Longitude:':long,'Latitude:':lat,'Continente:':continente,'IP':ip,'DDI':codigo_tel,'Fuso Hr:':fuso}

        mostraDados(r2) #Mostra todos os dados, e se chegou até aqui o programa sera finalizado sem erros
    except:
        print(' ')
        print(' ---- ERRO ----')
        print('Provavelmente o IP não foi encontrado, ou ocorreu algum outro problema')
        print('Verificar o IP / Verificar sua internet / Tentar novamente')
else:
    print('Erro ao carregar informações... fechando...')
    quit()

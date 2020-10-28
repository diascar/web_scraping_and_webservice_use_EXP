import requests
import sys

uri = "http://viacep.com.br/ws/"
c = sys.argv[1]

def consulta(cep):
    new_uri = f'{uri}{cep}/json'
    print(new_uri)
    resposta = requests.get(new_uri)
    end = resposta.json()
    print(f"O logradouro é {end['logradouro']}, no bairro {end['bairro']} e na cidade {end['localidade']}.")

consulta(c)

import requests

# Criar uma sessão autenticada
session = requests.Session()

# Credenciais
LOGIN_URL = "https://saude.sulamericaseguros.com.br/prestador/login"
BUSCA_URL = "https://saude.sulamericaseguros.com.br/prestador/api/paciente/buscar"  

credentials = {
    "codigoReferenciado": "100000009361",
    "usuario": "master",
    "senha": "837543"
}

# Fazer login
response = session.post(LOGIN_URL, data=credentials)
if response.status_code == 200:
    print("✅ Login realizado com sucesso!")
else:
    print("❌ Falha no login:", response.text)
    exit()

# Parâmetros da busca do paciente
params = {
    "carteira": "55788888485177660015"
}

# Fazer a busca
response = session.get(BUSCA_URL, params=params)

if response.status_code == 200:
    print("✅ Paciente encontrado:", response.json())
else:
    print("❌ Erro ao buscar paciente:", response.text)

import requests
from bs4 import BeautifulSoup

def login(usuario, senha, codigo):
    url = "https://saude.sulamericaseguros.com.br/prestador/login/"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Pragma": "no-cache",
        "Referer": "https://saude.sulamericaseguros.com.br/prestador/login/",
        "Origin": "https://saude.sulamericaseguros.com.br",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/134.0.0.0 Safari/537.36"
    }

    payload = {
        "lumNewParams": f"""<parameters destId="8A61890A697C8A4C01697C9D3DE0250E" destType="lumII">
        <p n="lumFromForm">Form_8A61890A697C8A4C01697C9D3DE0250E</p>
        <p n="lumFormAction">https://saude.sulamericaseguros.com.br/main.jsp?lumPageId=8A61898253CE1C780153D20B7FF82329&amp;lumA=1&amp;lumII=8A61890A697C8A4C01697C9D3DE0250E</p>
        <p n="doui_processActionId">loginPrestador</p>
        <p n="doui_fromForm">Form_8A61890A697C8A4C01697C9D3DE0250E</p>
        <p n="lumII">8A61890A697C8A4C01697C9D3DE0250E</p>
        <p n="code">{codigo}</p>
        <p n="user">{usuario}</p>
        <p n="senha">{senha}</p>
        </parameters>""",
        "lumPageOriginalUrl": "main.jsp?lumPageId=8A61898253CE1C780153D20B7FF82329",
        "lumII": "8A61890A697C8A4C01697C9D3DE0250E",
        "lumA": "1",
    }

    session = requests.Session()
    response = session.post(url, headers=headers, data=payload)

    if "Usuário ou Senha Inválidos" in response.text or "login" in response.url:
        print("❌ Login falhou!")
        return None
    else:
        print("✅ Login efetuado com sucesso!")
        return session


def acessar_guia(session):
    guia_url = "https://saude.sulamericaseguros.com.br/prestador/servicos-medicos/contas-medicas/faturamento-tiss-3/faturamento/guia-de-consulta/"
    
    headers_guia = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://saude.sulamericaseguros.com.br/prestador/servicos-medicos/contas-medicas/faturamento-tiss-3/faturamento/",
    }

    response = session.get(guia_url, headers=headers_guia)

    if response.status_code == 200:
        print("✅ Página 'Guia de Consulta' acessada com sucesso!")
        with open("guia_de_consulta.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        return True
    else:
        print(f"❌ Erro ao acessar 'Guia de Consulta': {response.status_code}")
        return False


def buscar_paciente(session, numero_carteira):
    url_busca = "https://saude.sulamericaseguros.com.br/main.jsp?lumPageId=8A61898253CE1C780153D20B7FF82329&lumA=1&lumII=8A61890A697C8A4C01697C9D3DE0250E"

    payload = {
        "campo": "numeroCarteira",
        "valorCampo": numero_carteira,
        "doui_processActionId": "buscarPaciente",
        "lumII": "8A61890A697C8A4C01697C9D3DE0250E",
        "lumPageOriginalUrl": "main.jsp?lumPageId=8A61898253CE1C780153D20B7FF82329",
        "lumA": "1",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/134.0.0.0 Safari/537.36",
        "Referer": "https://saude.sulamericaseguros.com.br/prestador/servicos-medicos/contas-medicas/faturamento-tiss-3/faturamento/guia-de-consulta/",
        "Origin": "https://saude.sulamericaseguros.com.br"
    }

    response = session.post(url_busca, data=payload, headers=headers)

    if response.ok:
        print("✅ Busca do paciente realizada com sucesso!")
        with open("resultado_paciente.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        # EXTRAÇÃO
        with open("resultado_paciente.html", "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        paciente_info = {}

        for label in soup.find_all("label"):
            nome_campo = label.get_text(strip=True)
            valor_input = label.find_next("input")
            if valor_input and valor_input.has_attr("value"):
                paciente_info[nome_campo] = valor_input["value"]

        print("📋 Dados do Paciente:")
        for campo, valor in paciente_info.items():
            print(f"{campo}: {valor}")

        return paciente_info
    else:
        print(f"❌ Erro ao buscar paciente: {response.status_code}")
        return None

# ====================== EXECUÇÃO ======================
if __name__ == "__main__":
    usuario = "master"
    senha = "837543"
    codigo = "100000009361"
    numero_carteira = "55788888485177660015"

    session = login(usuario, senha, codigo)

    if session:
        if acessar_guia(session):
            buscar_paciente(session, numero_carteira)


# Lê e interpreta o HTML da resposta da busca
with open("resultado_paciente.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

# Verifica se existe a mensagem de erro no resultado
sem_resultado = soup.find("div", class_="text-danger", string="Nenhum resultado encontrado para o filtro atual.")

if sem_resultado:
    print("❌ Nenhum paciente encontrado com esse número de carteira.")
else:
    print("✅ Paciente encontrado!")
    # Aqui você pode buscar e extrair dados específicos do paciente se necessário
    # Exemplo:
    info = soup.find_all("td")
    for td in info:
        print("📌", td.text.strip())

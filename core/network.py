import socket
import requests

# Definindo constantes
API_HOST = "ipinfo.io"
TIMEOUT = 10.0

def validar_alvo(alvo):
    """
    Camada de Rede: Traduz o domínio para IP (DNS).
    Retorna: (Sucesso: bool, IP ou Mensagem de Erro: str).
    """
    try:
        ip_alvo = socket.gethostbyname(alvo)
        return True, ip_alvo
    except socket.gaierror:
        return False, "Erro: Não foi possível processar o domínio."

def fazer_requisicao_api(ip_alvo):
    """
    Camada de Aplicação (HTTP): O requests gerencia a conexão TCP e os cabeçalhos HTTP.
    Retorna: (Sucesso: bool, Objeto Resposta ou Mensagem de Erro: str)
    """
    url = f"http://{API_HOST}/{ip_alvo}/json"
    cabecalhos = {"User-Agent": "ClienteRedes-UFS/4.0"}
    
    try:
        resposta = requests.get(url, headers=cabecalhos, timeout=TIMEOUT)
        
        # O raise_for_status() aciona um erro automaticamente se o servidor 
        # responder com algo como 404 (Não Encontrado) ou 500 (Erro Interno)
        resposta.raise_for_status()
        
        return True, resposta
    except requests.exceptions.RequestException as e:
        return False, f"Erro na comunicação HTTP com o servidor: {e}"

def extrair_dados_json(resposta):
    """
    Processamento: Usa o decodificador nativo do requests para extrair o JSON.
    Retorna: (Sucesso: bool, Dicionário JSON ou Mensagem de Erro: str)
    """
    try:
        dados_json = resposta.json()
        return True, dados_json
    except ValueError:
        return False, "Erro: A resposta do servidor não é um JSON válido."

def def buscar_dados_ip(alvo):
    #TODO

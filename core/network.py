import socket
import json

# Definindo constantes
API_HOST = "ipinfo.io"
API_PORT = 80
TIMEOUT = 10.0

def validar_alvo(alvo):
    """
    Camada de Rede: Traduz o domínio para IP (DNS).
    Retorna: (Sucesso: bool, IP ou Mensagem de Erro: str).
    """
    try:
        ip_alvo = socket.gethostbyname(alvo)
        return True, ip_alvo
    except socker.gaierror:
        return False, "Erro: Não foi possível processar o domínio."

def montar_requisicao_http:
    """
    Camada de Aplicacao: Constrói o texto da requisicao HTTP GET.
    Retorna: String da requisição.
    """
    return (
        f"GET /{ip_alvo}/json HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: ClienteRedes-UFS/3.0\r\n"
        "Connection: close\r\n\r\n"
    )
def executar_transacao_tcp(host, porta, requisicao_str):
    #TODO
def extrair_corpo_json(resposta_texto):
    #TODO
def def buscar_dados_ip(alvo):
    #TODO

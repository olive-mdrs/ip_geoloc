import socket
import json

API_HOST = "ipinfo.io"
API_PORT = 80
TIMEOUT = 10.0

def validar_alvo(alvo):
    """Tradução DNS."""
    try:
        ip_alvo = socket.gethostbyname(alvo)
        return True, ip_alvo
    except socket.gaierror:
        return False, "Erro: Não foi possível processar o domínio."

def fazer_requisicao_api(ip_alvo):
    """
    Camada de Transporte e Aplicação: Sockets TCP.
    """
    # Construção manual do cabeçalho HTTP
    requisicao = (
        f"GET /{ip_alvo}/json HTTP/1.1\r\n"
        f"Host: {API_HOST}\r\n"
        "User-Agent: ClienteRedes-UFRN/5.0\r\n"
        "Connection: close\r\n\r\n"
    )
    
    cliente = None
    try:
        # AF_INET = IPv4, SOCK_STREAM = TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(TIMEOUT)
        cliente.connect((API_HOST, API_PORT))
        
        # Enviando os bytes pela rede
        cliente.sendall(requisicao.encode('utf-8'))
        
        # Recebendo a resposta fragmentada
        resposta = b""
        while True:
            dados = cliente.recv(4096)
            if not dados:
                break
            resposta += dados
            
        # Decodificando os bytes recebidos para texto
        return True, resposta.decode('utf-8', errors='ignore')
        
    except Exception as e:
        return False, f"Erro na comunicação HTTP via socket: {e}"
        
    finally:
        if cliente:
            cliente.close()

def extrair_dados_json(resposta_texto):
    """
    Separa o cabeçalho HTTP do corpo JSON usando a quebra dupla \r\n\r\n.
    """
    if "\r\n\r\n" not in resposta_texto:
        return False, "Erro: Resposta HTTP malformada."
        
    cabecalhos, corpo = resposta_texto.split("\r\n\r\n", 1)
    
    try:
        return True, json.loads(corpo)
    except json.JSONDecodeError:
        return False, "Erro ao decodificar JSON retornado."
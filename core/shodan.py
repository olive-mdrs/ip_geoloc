import socket
import ssl
import json

def buscar_dados_shodan(ip_alvo):
    """
    Consulta o Shodan InternetDB usando um Socket TCP envolto em SSL (HTTPS).
    """
    host = "internetdb.shodan.io"
    porta = 443 # Porta padrão para HTTPS
    
    # Requisição HTTP padrão, mas trafegará criptografada
    requisicao = (
        f"GET /{ip_alvo} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "User-Agent: ClienteRedes-UFS/5.0\r\n"
        "Connection: close\r\n\r\n"
    )
    
    # Cria o contexto de segurança padrão do sistema operacional
    contexto = ssl.create_default_context()
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.settimeout(5.0)
    
    try:
        # Envolve o socket cru com a camada TLS antes de conectar
        conexao_segura = contexto.wrap_socket(cliente, server_hostname=host)
        conexao_segura.connect((host, porta))
        conexao_segura.sendall(requisicao.encode('utf-8'))
        
        resposta_crua = b""
        while True:
            dados = conexao_segura.recv(4096)
            if not dados:
                break
            resposta_crua += dados
            
        resposta_texto = resposta_crua.decode('utf-8', errors='ignore')
        
        if "\r\n\r\n" not in resposta_texto:
             return False, "Resposta inválida do servidor Shodan."
             
        cabecalhos, corpo = resposta_texto.split("\r\n\r\n", 1)
        
        # Tratamento de status 404 direto no texto HTTP
        if "404 Not Found" in cabecalhos:
            return True, {"info": "Nenhum dado historico encontrado no Shodan para este IP."}
            
        return True, json.loads(corpo)
        
    except Exception as e:
        return False, f"Erro ao consultar Shodan via socket seguro: {e}"
        
    finally:
        try:
            # Importante fechar a conexão criptografada
            conexao_segura.close()
        except:
            pass

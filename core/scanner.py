import socket
import concurrent.futures

def testar_porta_tcp(ip, porta):
    """
    Testa uma única porta via TCP Connect e tenta capturar o banner.
    Retorna: (porta, is_aberta, banner_texto)
    """
    resultado = -1
    banner = None
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Timeout (0.5s) para varrer portas fechadas/filtradas rapidamente
        sock.settimeout(0.5) 
        resultado = sock.connect_ex((ip, porta))
        
        if resultado == 0:
            try:
                # Envia um payload HTTP simples para provocar uma resposta do servidor
                sock.sendall(b"GET / HTTP/1.0\r\n\r\n")
                dados = sock.recv(1024)
                if dados:
                    # Pega apenas a primeira linha do retorno para manter o visual limpo
                    banner = dados.decode('utf-8', errors='ignore').split('\n')[0].strip()
            except Exception:
                banner = "Sem banner (Timeout ou recusa)"
                
    except Exception:
        pass
    finally:
        sock.close()
        
    is_aberta = (resultado == 0)
    return porta, is_aberta, banner

def escanear_portas_alvo(ip, lista_portas):
    """
    Gerencia a varredura de múltiplas portas utilizando threads.
    Retorna: Lista de dicionários com as portas abertas.
    """
    portas_abertas = []
    
    # Executa até 20 conexões simultâneas para otimizar o tempo total
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futuros = {executor.submit(testar_porta_tcp, ip, porta): porta for porta in lista_portas}
        
        for futuro in concurrent.futures.as_completed(futuros):
            porta, is_aberta, banner = futuro.result()
            if is_aberta:
                portas_abertas.append({
                    "porta": porta,
                    "banner": banner
                })
                
    # Ordena as portas do menor para o maior antes de retornar
    return sorted(portas_abertas, key=lambda x: x["porta"])

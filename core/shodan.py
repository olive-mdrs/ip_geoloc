import requests

def buscar_dados_shodan(ip_alvo):
    """
    Consulta a API pública do Shodan InternetDB para obter CVEs e portas conhecidas.
    Retorna: (Sucesso: bool, Dicionário de Dados ou Mensagem: str)
    """
    url = f"https://internetdb.shodan.io/{ip_alvo}"
    
    try:
        # Timeout curto. Se o Shodan não responder rápido, evitamos travar a aplicação.
        resposta = requests.get(url, timeout=5.0)
        
        # O Shodan retorna 404 se não tiver informações sobre o IP. 
        # Isso não é um erro da nossa rede, apenas ausência de dados.
        if resposta.status_code == 404:
            return True, {"info": "Nenhum dado historico encontrado no Shodan para este IP."}
            
        resposta.raise_for_status()
        return True, resposta.json()
        
    except requests.exceptions.RequestException as e:
        return False, f"Erro ao consultar Shodan: {e}"

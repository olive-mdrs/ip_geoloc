from core.ipinfo import validar_alvo, fazer_requisicao_api, extrair_dados_json
from core.shodan import buscar_dados_shodan
from core.scanner import escanear_portas_alvo

def executar_analise_completa(alvo, portas_str):
    """
    Coordena todas as fases do projeto, unindo dados de várias fontes.
    """
    resultado_final = {}
    
    # FASE 1: Resolução DNS
    sucesso_dns, ip_alvo = validar_alvo(alvo)
    if not sucesso_dns:
        return False, ip_alvo
    
    resultado_final["ip"] = ip_alvo
    
    # FASE 2: Geolocalização (IPInfo)
    sucesso_http, resposta_ipinfo = fazer_requisicao_api(ip_alvo)
    if sucesso_http:
        sucesso_json, dados_ipinfo = extrair_dados_json(resposta_ipinfo)
        if sucesso_json:
            resultado_final["geo"] = dados_ipinfo
    
    # FASE 3: Enriquecimento (Shodan)
    sucesso_shodan, dados_shodan = buscar_dados_shodan(ip_alvo)
    if sucesso_shodan:
        resultado_final["shodan"] = dados_shodan
        
    # FASE 4: Scanner Local de Portas
    # Converte a string do usuário "80, 443" em uma lista de inteiros [80, 443]
    try:
        lista_portas = [int(p.strip()) for p in portas_str.split(",") if p.strip()]
    except ValueError:
        return False, "Formato de portas inválido. Use números separados por vírgula."
        
    if not lista_portas:
        lista_portas = [21, 22, 23, 80, 443, 3306, 8080] # Portas padrão se vazio
        
    resultado_final["portas_abertas_local"] = escanear_portas_alvo(ip_alvo, lista_portas)
    
    return True, resultado_final

import unittest
import json
from core.network import fazer_requisicao_api, extrair_dados_json

class TestParsingHTTP(unittest.TestCase):
    """Testes Unitários: Validação da lógica interna sem uso de rede."""

    def test_extracao_json_sucesso(self):
        resposta_simulada = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Connection: close\r\n"
            "\r\n\r\n"
            '{"ip": "8.8.8.8", "city": "Natal"}'
        )
        sucesso, dados = extrair_dados_json(resposta_simulada)
        self.assertTrue(sucesso)
        self.assertEqual(dados["ip"], "8.8.8.8")

    def test_extracao_falha_cabecalho(self):
        resposta_quebrada = "Resposta sem padrão de cabecalho."
        sucesso, mensagem = extrair_dados_json(resposta_quebrada)
        self.assertFalse(sucesso)
        self.assertIn("malformada", mensagem)

    def test_extracao_falha_json(self):
        resposta_html = (
            "HTTP/1.1 500 Internal Error\r\n\r\n"
            "<html><body>Erro Fatal</body></html>"
        )
        sucesso, mensagem = extrair_dados_json(resposta_html)
        self.assertFalse(sucesso)
        self.assertIn("decodificar JSON", mensagem)


class TestNetworkIntegration(unittest.TestCase):
    """Testes de Integração: Conexão real com a internet via Sockets TCP."""

    def test_requisicao_real_ipinfo(self):
        print("\n\n--- INICIANDO TESTE DE CONEXÃO REAL VIA SOCKET (IPINFO) ---")
        
        # 1. Dispara a requisição real para o IP do Google
        sucesso_http, resposta_crua = fazer_requisicao_api("8.8.8.8")
        
        # Verifica se o socket conectou e trouxe resposta
        self.assertTrue(sucesso_http, "Falha ao conectar via socket TCP.")
        self.assertIn("HTTP/1.1 200 OK", resposta_crua)

        # 2. Extrai os dados reais
        sucesso_json, dados = extrair_dados_json(resposta_crua)
        self.assertTrue(sucesso_json, "Falha ao extrair o JSON da resposta real.")

        # 3. Imprime no terminal para verificação visual
        print("Dados reais recebidos do servidor:")
        print(json.dumps(dados, indent=4))

        # 4. Verifica dados mínimos esperados
        self.assertEqual(dados.get("ip"), "8.8.8.8")
        self.assertEqual(dados.get("country"), "US")
        
        print("--- TESTE DE CONEXÃO REAL CONCLUÍDO COM SUCESSO ---\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)

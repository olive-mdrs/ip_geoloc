import unittest
from core.network import extrair_dados_json

class TestParsingHTTP(unittest.TestCase):

    def test_extracao_json_sucesso(self):
        """Simula uma resposta TCP perfeita."""
        resposta_simulada = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            "Connection: close\r\n"
            "\r\n\r\n" # A quebra fundamental do protocolo
            '{"ip": "8.8.8.8", "city": "Natal"}'
        )
        
        sucesso, dados = extrair_dados_json(resposta_simulada)
        self.assertTrue(sucesso)
        self.assertEqual(dados["ip"], "8.8.8.8")
        self.assertEqual(dados["city"], "Natal")

    def test_extracao_falha_cabecalho(self):
        """Testa a reação a uma string sem as quebras HTTP corretas."""
        resposta_quebrada = "Resposta sem padrão de cabecalho."
        sucesso, mensagem = extrair_dados_json(resposta_quebrada)
        
        self.assertFalse(sucesso)
        self.assertIn("malformada", mensagem)

    def test_extracao_falha_json(self):
        """Testa o comportamento se o servidor retornar um HTML de erro em vez de JSON."""
        resposta_html = (
            "HTTP/1.1 500 Internal Error\r\n\r\n"
            "<html><body>Erro Fatal</body></html>"
        )
        sucesso, mensagem = extrair_dados_json(resposta_html)
        
        self.assertFalse(sucesso)
        self.assertIn("decodificar JSON", mensagem)

if __name__ == "__main__":
    unittest.main()

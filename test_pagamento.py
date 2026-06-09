import unittest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout

from pagamento import enviar_para_gateway, processar_compra


class TestPagamento(unittest.TestCase):
    @patch("pagamento.requests.post")
    def test_enviar_para_gateway_retorna_json(self, mock_post):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            "status": "aprovado",
            "transacao_id": "123",
        }
        mock_post.return_value = mock_response

        resultado = enviar_para_gateway({"numero": "4111111111111111"}, 100)

        self.assertEqual(
            resultado,
            {"status": "aprovado", "transacao_id": "123"},
        )

    @patch("pagamento.requests.post")
    def test_enviar_para_gateway_500_gera_connection_error(self, mock_post):
        mock_response = Mock(status_code=500)
        mock_post.return_value = mock_response

        with self.assertRaises(ConnectionError):
            enviar_para_gateway({"numero": "4111111111111111"}, 100)

    @patch("pagamento.enviar_para_gateway")
    def test_processar_compra_aprovado(self, mock_enviar):
        mock_enviar.return_value = {
            "status": "aprovado",
            "transacao_id": "abc123",
        }

        mensagem = processar_compra(1, {"numero": "4111111111111111"}, 100)

        self.assertEqual(mensagem, "Sucesso! Transação abc123 confirmada.")

    @patch("pagamento.enviar_para_gateway")
    def test_processar_compra_recusado(self, mock_enviar):
        mock_enviar.return_value = {
            "status": "recusado",
            "motivo": "Saldo insuficiente",
        }

        mensagem = processar_compra(1, {"numero": "4111111111111111"}, 100)

        self.assertEqual(
            mensagem,
            "Pagamento recusado. Motivo: Saldo insuficiente.",
        )

    @patch("pagamento.enviar_para_gateway")
    def test_processar_compra_status_desconhecido(self, mock_enviar):
        mock_enviar.return_value = {"status": "pendente"}

        mensagem = processar_compra(1, {"numero": "4111111111111111"}, 100)

        self.assertEqual(mensagem, "Status de pagamento desconhecido.")

    @patch("pagamento.requests.post")
    def test_processar_compra_timeout(self, mock_post):
        mock_post.side_effect = Timeout()

        mensagem = processar_compra(1, {"numero": "4111111111111111"}, 100)

        self.assertEqual(
            mensagem,
            "Tempo de resposta esgotado. Verifique sua fatura antes de tentar de novo.",
        )


if __name__ == "__main__":
    unittest.main()

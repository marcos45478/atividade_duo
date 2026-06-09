# Documentação do Projeto de Pagamento

## Visão Geral
Este projeto implementa um fluxo simples de processamento de pagamento via gateway externo.

Arquivos principais:
- `pagamento.py`: contém a lógica de envio de dados ao gateway e o processamento da compra.
- `test_pagamento.py`: contém os testes unitários que garantem o comportamento esperado em diferentes cenários.

## Como funciona

### pagamento.py

Funções principais:
- `enviar_para_gateway(dados_cartao, valor)`: faz a requisição HTTP para o gateway de pagamentos.
  - envia um POST para `https://api.pagarapido.com.br/v1/transacoes` com o cartão e valor.
  - trata `500` como indisponibilidade do gateway.
  - lança exceções apropriadas para erros de rede e de requisição.

- `processar_compra(usuario_id, dados_cartao, valor)`: processa o retorno do gateway e devolve uma mensagem ao usuário.
  - `aprovado` → retorna mensagem de sucesso com `transacao_id`.
  - `recusado` → retorna mensagem com o motivo da recusa.
  - outros status → retorna "Status de pagamento desconhecido."
  - trata `ConnectionError`, `Timeout` e `RequestException` de forma específica.

## Cenários testados

No arquivo `test_pagamento.py` são validados vários caminhos:

1. `test_enviar_para_gateway_retorna_json`
   - verifica se `enviar_para_gateway` retorna o JSON correto quando o gateway responde com sucesso.

2. `test_enviar_para_gateway_500_gera_connection_error`
   - valida que um status `500` do gateway gera um `ConnectionError`.

3. `test_processar_compra_aprovado`
   - simula `enviar_para_gateway` aprovando a compra e verifica a mensagem de sucesso.

4. `test_processar_compra_recusado`
   - simula recusa por falta de limite e verifica a mensagem de recusa com motivo.

5. `test_processar_compra_status_desconhecido`
   - simula status desconhecido e verifica a mensagem de status desconhecido.

6. `test_processar_compra_timeout`
   - simula `requests.post` lançando `Timeout` e verifica mensagem de tempo esgotado.

## Execução dos testes

Dentro do ambiente virtual (`venv`) ativado, execute:

```powershell
python -m pytest -v
```

> Observação: o comando `pytest` pode não estar disponível diretamente no PowerShell se o `venv` não estiver corretamente ativado ou se o executável não estiver no `PATH`. Nesse caso, use `python -m pytest -v`.

## Observações adicionais

- A implementação atual usa mock para simular o gateway de pagamento em `processar_compra`, evitando chamadas de rede reais durante os testes.
- O teste de timeout cobre o cenário de queda do servidor em alta demanda, como em uma Black Friday.

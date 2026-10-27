# SPEC — superfície de consulta do PDV para agentes

## Problema
O PDV (`retail-pos-python`) guarda estoque, fiado, validade e vendas num SQLite local. Para um agente responder "quanto está fiado?", hoje é preciso abrir o app, navegar por telas e ler números na interface. Isso não é automatizável e não tem contrato estável.

## Objetivo
Expor consultas **somente-leitura** por dois canais: CLI em JSON e servidor MCP. Nenhuma escrita. Nenhuma credencial.

## Público
1. Você, no terminal, para tirar dúvida rápida.
2. Agentes (Claude Code, Codex, Cursor) que precisam de contexto da loja.
3. Recrutador/cliente olhando o portfólio.

## Contrato de saída
Sempre `{"comando": "<nome>", "dados": ...}` em JSON, UTF-8, uma execução por comando.

| Comando | Dados | Regra |
|---|---|---|
| `resumo-hoje` | vendas, total, fiado, data | vendas do dia, `cancelada = 0` |
| `fiado` | id, nome, comprado, pago, saldo, telefone, limite | saldo = compras `forma_pagamento='fiado'` − pagamentos não estornados; só saldo > 0,004 |
| `estoque-baixo` | id, nome, quantidade, minimo, falta | `ativo = 1` e `quantidade_estoque <= estoque_minimo` |
| `validade` | id, nome, quantidade, data_validade, dias_restantes | `quantidade > 0` e vence em até N dias (inclui vencidos) |

## Restrições (não negociáveis)
- Conexão `file:...?mode=ro`. Nunca abrir em modo escrita.
- Sem `INSERT/UPDATE/DELETE`, sem migração, sem `init_db()`.
- Saída sem dados pessoais além do necessário: telefone só no comando `fiado`, que é ferramenta de cobrança.
- Timeout de 30 s por consulta.
- Nenhuma dependência além da stdlib para o CLI.

## Não-objetivos
- Não substituir a interface do PDV.
- Não expor escrita (baixa de fiado, ajuste de estoque) nesta versão.
- Não rodar em rede: uso local, via stdio.

## Critérios de aceite
1. `python3 pos_query.py --db <banco> resumo-hoje` devolve JSON válido.
2. Os quatro comandos rodam sem erro contra um banco real.
3. Nenhum arquivo do banco é modificado: `git status` limpo e `md5sum` do `.db` idêntico antes/depois.
4. `mcp_server.py` sobe no inspector e lista 4 ferramentas.
5. Teste automatizado cobrindo o cálculo de saldo de fiado (inclui pagamento estornado).

## Verificação
- Comparar `resumo-hoje` com o total mostrado na tela do PDV no mesmo minuto.
- Conferir o saldo de 2 clientes manualmente (maior e menor saldo).
- Rodar `python3 -m pytest` no repo após integrar o teste.

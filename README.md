# Case de agentic engineering — PDV do mercadinho como superfície de agente

![CI](https://github.com/FelipeFeerreira/pos-agent-surface/actions/workflows/ci.yml/badge.svg)

## O que é
Um case público, em um repositório pequeno, que mostra a habilidade que Karpathy chama de *agentic engineering*: usar agentes para entregar software de verdade, com spec, testes, permissões e revisão — e não só "vibe coding".

O produto do case é uma **superfície agent-native** para o PDV que já roda na loja: consultas somente-leitura (estoque baixo, fiado em aberto, validade, resumo do dia) expostas por CLI em JSON e por **servidor MCP**, prontas para qualquer agente consumir.

## Por que isso vale dinheiro
- É demonstrável em 5 minutos: agente pergunta "quanto está fiado hoje?" e recebe JSON estruturado.
- Prova três coisas que cliente paga: integração com sistema legado, contrato estável (JSON/schema), e segurança (read-only, sem credencial no código).
- Diferencia proposta no Upwork de "mais um dev que usa ChatGPT": tem artefato auditável.

## Estrutura
```
agentic-engineering-case/
├── README.md          # este arquivo (o que é, por que importa, como demonstrar)
├── SPEC.md            # a spec usada para dirigir o agente
├── CHECKLIST.md       # o padrão de qualidade aplicado (agentic, não vibe)
└── pos-query/
    ├── pos_query.py   # CLI read-only (testada contra mercadinho.db)
    ├── mcp_server.py  # wrapper MCP (não testado: pacote `mcp` ausente)
    └── README.md      # uso, contrato de saída, como plugar no PDV
```

## Testes
`pytest -q tests/` cobre o contrato do CLI (somas, cancelamento, estorno, validade e read-only);
o workflow em `.github/workflows/ci.yml` roda os testes em Python 3.11 e 3.13 e sobe o servidor MCP via stdio.

## Estado (27/10/2026)
- Publicado em [github.com/FelipeFeerreira/pos-agent-surface](https://github.com/FelipeFeerreira/pos-agent-surface).
- Integrado ao PDV como `agent_surface/` na branch `feat/agent-surface`.
- `pos_query.py`: **testado** contra o banco real, em modo somente-leitura (`mode=ro`).
  - `resumo-hoje`: 20 vendas, R$ 274,71, R$ 22,97 a prazo.
  - `fiado`: 24 clientes com saldo, soma R$ 1.291,41.
  - `estoque-baixo`: encontrou estoque negativo (ex.: PAO FRANCES MARQUESPAN, -1.601 un.).
  - `validade`: 1 lote vencido com saldo (COCA 600 ML, vencido em 12/10).
- `mcp_server.py`: **testado** com o SDK MCP 2.x — 4 ferramentas expostas e `resumo_do_dia` chamado via stdio.
- Nenhum banco, dado de cliente ou credencial foi publicado. O repositório contém apenas código e documentação.

## Achados que já valem correção no PDV
1. **Estoque negativo** em produtos de produção (pão): indica baixa de venda/consumo sem entrada correspondente. É o mesmo tipo de divergência que a oportunidade de conciliação de estoque ataca.
2. **Lote vencido com saldo**: o controle de validade existe, mas não bloqueia venda nem alerta sozinho.

## Próximos passos
1. Rodar `python3 test_mcp_smoke.py` dentro de `pos-query/` em CI (GitHub Actions).
2. Teste automatizado do saldo de fiado com pagamento estornado.
3. Captura de tela de um agente consultando o PDV, no README.
4. Corrigir no PDV: estoque negativo e bloqueio de venda de lote vencido.

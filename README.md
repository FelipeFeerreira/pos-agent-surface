# POS agent surface — read-only queries for an agent, over a real point-of-sale database

[![CI](https://github.com/FelipeFeerreira/pos-agent-surface/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeFeerreira/pos-agent-surface/actions/workflows/ci.yml)

A small, public case in **agentic engineering**: a real product built with a written spec, contract tests, permissions and review — not vibe coding. The product is an agent-native, **read-only** surface over the point-of-sale database that already runs in a store: low stock, open customer credit, expiry, and a summary of the day, exposed as a JSON CLI and as an **MCP server**.

Nothing here connects to a live store: the repository carries code, a spec and tests. The demo runs against a generated fixture database.

## What it does

| Query | Output |
| --- | --- |
| `resumo-hoje` | sales, revenue and credit granted for the current day |
| `fiado` | customers with an open balance and the total owed |
| `estoque-baixo` | products at or below minimum stock |
| `validade` | lots past or near their expiry date |

Every command opens SQLite in read-only mode (`mode=ro`) and prints one JSON object with a stable schema, so an agent can consume it without a parser.

## Stack

- **Python 3.11+** for the CLI (`pos-query/pos_query.py`) and the MCP wrapper (`pos-query/mcp_server.py`)
- **SQLite** as the source, opened read-only
- **pytest** for the contract tests; `tests/fixtures.py` builds a deterministic database
- **MCP (Model Context Protocol) SDK 2.x** exposing the four queries as tools
- **GitHub Actions** for CI, on Python 3.11 and 3.13

## Run it

```bash
git clone https://github.com/FelipeFeerreira/pos-agent-surface.git
cd pos-agent-surface
python3 -m pip install pytest "mcp>=2,<3"

# build a fixture database, then query it
python tests/fixtures.py /tmp/fixture.db
python pos-query/pos_query.py --db /tmp/fixture.db resumo-hoje
python pos-query/pos_query.py --db /tmp/fixture.db estoque-baixo
```

The CLI never writes: if a database is passed without read-only access the process fails instead of mutating it.

### MCP server

```bash
POS_DB=/tmp/fixture.db python pos-query/mcp_server.py
```

The four queries are registered as tools, so any MCP-capable agent can ask "how much credit is open today?" and get structured JSON.

## Tests

```bash
pytest -q tests/                                   # contract tests over the CLI
python tests/fixtures.py /tmp/fixture.db
POS_DB=/tmp/fixture.db python pos-query/test_mcp_smoke.py   # MCP smoke over stdio
```

The CI workflow runs both commands on every push and pull request, on Python 3.11 and 3.13: [workflow](.github/workflows/ci.yml).

The tests cover totals, cancellation and refund handling, expiry filtering and the read-only guarantee; the MCP smoke test starts the server over stdio and calls a tool end to end.

## Repository layout

```
.
├── SPEC.md               # the spec the agent worked from
├── CHECKLIST.md          # the quality bar applied (agentic, not vibe coding)
├── pos-query/
│   ├── pos_query.py      # read-only CLI
│   ├── mcp_server.py     # MCP wrapper
│   └── README.md         # usage and output contract (Portuguese)
└── tests/
    ├── fixtures.py       # deterministic database
    └── test_pos_query.py # contract tests
```

## Status and limits

- The CLI and the MCP server are tested in CI against a fixture database.
- Not tested here: the physical scale, the receipt printer and any Windows-specific path — those belong to the store deployment and are not part of this case.
- The store database is private: no customer record, price table or credential is published in this repository.

## Português

Este repositório nasceu como um case em português sobre engenharia agêntica — a spec (`SPEC.md`), o checklist de qualidade (`CHECKLIST.md`) e o README do CLI continuam em português. O README principal ficou em inglês porque o público-alvo é recrutador e cliente remoto.

## License

MIT — see [LICENSE](LICENSE).

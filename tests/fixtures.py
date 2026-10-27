"""Cria um banco de fixture com o subconjunto de schema usado por pos_query.

Determinístico: mesmos IDs e valores em toda execução, sem dados reais.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import date, timedelta

SCHEMA = """
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY, nome TEXT, categoria TEXT, unidade TEXT,
    preco_custo REAL, preco_venda REAL, quantidade_estoque REAL,
    estoque_minimo REAL, ativo INTEGER DEFAULT 1
);
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY, nome TEXT, telefone TEXT, limite_credito REAL
);
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY, data_hora TEXT, valor_total REAL, desconto REAL DEFAULT 0,
    forma_pagamento TEXT, cliente_id INTEGER, cancelada INTEGER DEFAULT 0
);
CREATE TABLE pagamentos_fiado (
    id INTEGER PRIMARY KEY, cliente_id INTEGER, valor REAL, estornado INTEGER DEFAULT 0
);
CREATE TABLE lotes_validade (
    id INTEGER PRIMARY KEY, produto_id INTEGER, quantidade REAL, data_validade TEXT
);
"""


def criar(caminho: str) -> str:
    if os.path.exists(caminho):
        os.remove(caminho)
    conn = sqlite3.connect(caminho)
    conn.executescript(SCHEMA)

    conn.executemany(
        "INSERT INTO produtos (id, nome, categoria, unidade, preco_custo, preco_venda,"
        " quantidade_estoque, estoque_minimo, ativo) VALUES (?,?,?,?,?,?,?,?,?)",
        [
            (1, "ARROZ 5KG", "Mercearia", "UN", 18.0, 25.0, 2.0, 5.0, 1),   # abaixo do mínimo
            (2, "FEIJAO 1KG", "Mercearia", "UN", 5.0, 8.0, 30.0, 10.0, 1),  # ok
            (3, "PRODUTO INATIVO", "Mercearia", "UN", 1.0, 2.0, 0.0, 1.0, 0),
        ],
    )

    conn.executemany(
        "INSERT INTO clientes (id, nome, telefone, limite_credito) VALUES (?,?,?,?)",
        [(10, "CLIENTE A", "0000", 100.0), (11, "CLIENTE B", "1111", 0.0)],
    )

    hoje = date.today().isoformat()
    conn.executemany(
        "INSERT INTO vendas (id, data_hora, valor_total, forma_pagamento, cliente_id, cancelada)"
        " VALUES (?,?,?,?,?,?)",
        [
            (100, f"{hoje} 10:00:00", 50.0, "fiado", 10, 0),
            (101, f"{hoje} 11:00:00", 30.0, "fiado", 11, 0),
            (102, f"{hoje} 12:00:00", 20.0, "dinheiro", None, 0),
            (103, f"{hoje} 13:00:00", 99.0, "fiado", 10, 1),  # cancelada, não conta
        ],
    )

    conn.executemany(
        "INSERT INTO pagamentos_fiado (id, cliente_id, valor, estornado) VALUES (?,?,?,?)",
        [
            (200, 10, 20.0, 0),   # saldo A = 50 - 20 = 30
            (201, 11, 5.0, 1),    # estornado: saldo B = 30
        ],
    )

    conn.execute(
        "INSERT INTO lotes_validade (id, produto_id, quantidade, data_validade) VALUES (?,?,?,?)",
        (300, 2, 4.0, (date.today() + timedelta(days=3)).isoformat()),
    )
    conn.commit()
    conn.close()
    return caminho


if __name__ == "__main__":
    import sys

    print(criar(sys.argv[1] if len(sys.argv) > 1 else ":memory:"))

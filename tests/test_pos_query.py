"""Testes do contrato de pos_query.py contra um banco de fixture."""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixtures import criar  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RAIZ, "pos-query", "pos_query.py")


@pytest.fixture(scope="module")
def banco(tmp_path_factory):
    caminho = str(tmp_path_factory.mktemp("db") / "fixture.db")
    return criar(caminho)


def rodar(banco: str, *args: str) -> dict:
    saida = subprocess.run(
        [sys.executable, SCRIPT, "--db", banco, *args],
        capture_output=True, text=True, timeout=60,
    )
    assert saida.returncode == 0, saida.stderr
    return json.loads(saida.stdout)


def test_resumo_hoje_soma_apenas_vendas_nao_canceladas(banco):
    dados = rodar(banco, "resumo-hoje")["dados"]
    assert dados["vendas"] == 3
    assert dados["total"] == pytest.approx(100.0)
    assert dados["fiado"] == pytest.approx(80.0)


def test_estoque_baixo_ignora_inativos(banco):
    itens = rodar(banco, "estoque-baixo")["dados"]
    assert [i["nome"] for i in itens] == ["ARROZ 5KG"]
    assert itens[0]["falta"] == pytest.approx(3.0)


def test_fiado_desconta_pagamento_e_ignora_estornado(banco):
    clientes = {c["nome"]: c for c in rodar(banco, "fiado")["dados"]}
    assert clientes["CLIENTE A"]["saldo"] == pytest.approx(30.0)
    assert clientes["CLIENTE B"]["saldo"] == pytest.approx(30.0)


def test_validade_traz_lote_proximo(banco):
    lotes = rodar(banco, "validade", "--dias", "7")["dados"]
    assert len(lotes) == 1
    assert lotes[0]["nome"] == "FEIJAO 1KG"


def test_banco_ausente_falha_com_mensagem(banco, tmp_path):
    inexistente = str(tmp_path / "nao_existe.db")
    saida = subprocess.run(
        [sys.executable, SCRIPT, "--db", inexistente, "schema"],
        capture_output=True, text=True, timeout=60,
    )
    assert saida.returncode != 0
    assert "não encontrado" in saida.stderr


def test_banco_nao_e_escrito(banco):
    import hashlib

    def hash_arquivo() -> str:
        with open(banco, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    antes = hash_arquivo()
    for comando in ("resumo-hoje", "estoque-baixo", "fiado", "validade", "schema"):
        rodar(banco, comando)
    assert hash_arquivo() == antes

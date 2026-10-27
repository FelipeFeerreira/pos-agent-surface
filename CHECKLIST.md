# CHECKLIST — agentic engineering (o padrão do case)

Aplicado a este case e reutilizável em qualquer entrega com agente.

## Antes de gerar código
- [ ] Spec escrita com objetivo, contrato de saída, restrições e não-objetivos (`SPEC.md`).
- [ ] Critério de aceite verificável por comando, não por opinião.
- [ ] Domínio dos dados lido (schema real), não inventado.

## Durante
- [ ] Agente trabalha em branch/worktree isolada; nada direto na main.
- [ ] Permissões mínimas: leitura do banco, sem credencial no prompt.
- [ ] Cada passo tem teste executável (aqui: os 4 comandos contra banco real).
- [ ] Diff revisado por humano antes de integrar.
- [ ] Regra de negócio em um só lugar (o cálculo de fiado existe uma vez, no CLI).

## Antes de dizer "pronto"
- [ ] Rodou o comando e colou a saída (`resumo-hoje` × tela do PDV).
- [ ] Verificou que nada foi escrito (`md5sum` do `.db` igual).
- [ ] Tratou erro: banco ausente, tabela faltando, JSON inválido.
- [ ] README explica como rodar em 3 linhas.

## O que não fazer (vibe coding disfarçado)
- [ ] Sem "deve funcionar" sem execução.
- [ ] Sem dependência nova sem justificativa (aqui: stdlib no CLI; `mcp[cli]` só no wrapper).
- [ ] Sem dado pessoal de cliente em exemplo, print ou README.
- [ ] Sem publicar no GitHub sem aprovação do Felipe.

## Transferência para proposta de freela
Frase de uma linha para usar em proposta:
> "Entrego a integração com contrato verificável: spec, JSON estável, testes e superfície MCP pronta para agentes — não só código que passa."

Prova: link do repo do case + saída real do comando + diff revisado.

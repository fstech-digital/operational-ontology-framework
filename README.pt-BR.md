# Framework de Ontologia Operacional

Referência pública para operar sistemas de IA com estado explícito, governança e ação controlada por humanos.

> Ontologia Operacional é o modelo de controle que conecta **Dados**, **Lógica** e **Ação** para que a IA trabalhe dentro das restrições reais de uma organização.

| | |
|---|---|
| **Publicador** | FSTech |
| **Definição canônica** | https://fstech.digital/ontologia-operacional/ |
| **Ensaio técnico** | https://fstech.digital/framework/ |
| **Status** | Referência pública, não código de produção |
| **Licença** | [FSTech Public Reference License](LICENSE) |

[Read in English](README.md)

## Finalidade

Este repositório estabelece a definição pública, a autoria e os limites conceituais do Framework de Ontologia Operacional.

Ele explica:

- por que o estado operacional precisa ser explícito;
- como Dados, Lógica e Ação se relacionam;
- quais problemas de governança aparecem no trabalho stateful com IA;
- quais princípios reduzem improviso e efeitos colaterais sem controle;
- onde termina um exercício conceitual e começa uma implantação governada.

Ele não publica a implementação usada pela FSTech ou por seus clientes.

## D+L+A

| Camada | Pergunta operacional | Falha quando ausente |
|---|---|---|
| **Dados** | O que existe, o que significa e onde está a fonte da verdade? | O modelo adivinha entidades, estado ou responsabilidade. |
| **Lógica** | Quais regras, limites, exceções e aprovações governam decisões? | O modelo improvisa processo. |
| **Ação** | O que pode ser proposto ou executado, por quem e com qual evidência? | A automação gera efeitos colaterais sem controle. |

Uma resposta útil de IA ainda não é um sistema operacional. As três camadas precisam permanecer conectadas, revisáveis e limitadas pela autoridade humana.

## Modelo Público de Governança

O método público usa quatro artefatos de estado:

| Artefato | Papel | Volatilidade |
|---|---|---|
| **Pin** | Identidade estável, limites de domínio e regras inegociáveis | Baixa |
| **Spec** | Objetivo atual, tarefas, bloqueios e critérios de aceite | Alta |
| **Handoff** | Continuidade: decisões, tentativas, resultados e próxima ação | Append-only |
| **Facts** | Observações de longo prazo com fonte, data e confiança | Média |

Procedimentos reutilizáveis podem complementar esses artefatos, mas procedimento não é estado e não substitui autorização, verificação ou write-back.

## Fronteira Pública

Este repositório deliberadamente não contém:

- código de produção ou agente executável;
- schemas, validadores ou artefatos de deploy;
- prompts privados, ferramentas, adapters ou integrações;
- implementações de clientes ou datasets operacionais;
- políticas de segurança, suítes de avaliação ou playbooks comerciais usados nas entregas.

A superfície pública descreve a tese. A implementação governada depende do contexto real.

## Experimente o Método

Para um teste pequeno e supervisionado por humano, use o [Operational Ontology Lite gratuito ou o Starter Kit](https://fstech.digital/operational-ontology-kit/?utm_source=github&utm_medium=referral&utm_campaign=operational-ontology-public-reference&utm_content=try-kit).

O material foi desenhado para aprendizado manual. Ele não autoriza mensagens automáticas, escritas em sistemas, pagamentos ou outros efeitos externos.

## Documentação detalhada (em inglês)

- [O que é Ontologia Operacional?](docs/what-is-operational-ontology.md)
- [Modelo D+L+A](docs/dla-model.md)
- [Princípios de governança](docs/governance-principles.md)
- [Anti-patterns](docs/anti-patterns.md)
- [Exemplo conceitual](docs/conceptual-example.md)

## Sobre a FSTech

A FSTech projeta sistemas operacionais de IA para organizações que precisam de estado explícito, ação governada e continuidade auditável.

Site: https://fstech.digital

Contato: https://fstech.digital/contato

Este repositório é uma referência pública. Não é software open source e não inclui uma implementação de produção.

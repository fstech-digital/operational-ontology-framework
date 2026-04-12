# Framework de Ontologia Operacional FSTech

**Pin/Spec Protocol v2.** Como operar agentes de IA em produção com estado auditável, sem memória persistente no modelo.

> Agentes baseados em LLM se tornam production-ready quando operam dentro de um envelope de controle explícito, não quando o modelo fica mais inteligente.

| | |
|---|---|
| **Autor** | Felipe Silva |
| **Versão** | 1.0 |
| **Data** | Abril 2026 |
| **Licença** | [CC BY 4.0](LICENSE) |
| **Canônico** | [fstech.digital/framework](https://fstech.digital/framework/) |

---

## 1. Contexto e Problema

Agentes baseados em LLM enfrentam três problemas estruturais quando saem do protótipo e entram em produção real.

**Falta de auditabilidade.** Não há registro estruturado do que o agente decidiu e por quê. Logs de execução mostram o quê, raramente o porquê. Quando o agente age errado, reconstruir a cadeia causal é forense, não engenharia.

**Perda de estado entre execuções.** Cada chamada começa do zero sem contexto das anteriores. A tentativa comum é persistir via bancos vetoriais ou embeddings, o que transfere o problema: o agente agora lembra de forma difusa, sem garantia de quais fatos sobreviveram.

**Validação circular.** O modelo valida a si mesmo. Pergunta ao LLM se a resposta está correta, e ele confirma. Sem camada externa de controle, a validação é ruído treinado para soar confiante.

O Framework de Ontologia Operacional FSTech resolve os três com uma estrutura documental mínima executada em ciclo. Sem infraestrutura adicional, sem memória persistente no modelo, sem dependência de stack específica.

## 2. Tese Central

> Um agente de IA é production-ready quando opera dentro de um envelope de controle explícito, com estado auditável entre execuções, e quando a memória vive no documento, não no modelo.

O framework é agnóstico de modelo (roda com Claude, GPT, Gemini, modelos locais) e de infraestrutura (não requer banco vetorial, orquestrador específico ou pipeline customizado). A única dependência é um filesystem e disciplina documental.

Um corolário direto segue dessa premissa: porque a memória vive no filesystem e não no modelo, o agente é portável entre provedores sem perda de estado. Trocar de modelo amanhã não apaga o que ele aprendeu ontem.

## 3. Fundação: A Tríade D+L+A

A Ontologia Operacional se sustenta numa decomposição de primeiros princípios: todo sistema de gestão real tem três componentes atômicos, não mais.

**DADOS (D).** As entidades do negócio. Leads, clientes, projetos, contratos, faturas. Tudo que existe no mundo real e precisa ser representado no sistema. Extração e estruturação do conhecimento disperso em sistemas legados, documentos e memórias dos operadores.

**LÓGICA (L).** As regras de relação. Scoring, classificação, priorização, condições de ativação. A inteligência do negócio mapeada de forma que o sistema possa inferir. São as leis que governam o comportamento.

**AÇÃO (A).** O write-back acionável. Automações, notificações, atualizações de estado, mensagens enviadas. O estágio onde o insight se transforma em execução real no ambiente operacional.

A estrutura clássica é linear: D para L para A. A observação da prática mostra que o loop é contínuo: ações geram dados novos, que alimentam lógica refinada, que produz ações melhores. Projetar um sistema linear é projetar um sistema que morre no primeiro ciclo.

**Implicação operacional.** Ao projetar qualquer automação, a pergunta canônica não é "o que acontece quando executarmos" mas "o que acontece depois da ação". Se a resposta é nada, o sistema é linear, e linear significa frágil.

**Metáfora para clientes.** O negócio tem substantivos (clientes, pedidos, contratos), verbos (cobrar, notificar, consultar) e gramática (regras de priorização, scoring, escalação). Um sistema operacional existe quando todas as frases do negócio estão escritas e o sistema sabe executá-las. Dados são substantivos. Lógica é gramática. Ação são verbos.

## 4. Componentes Executáveis

O framework implementa D+L+A como três artefatos documentais mínimos. Cada artefato é um arquivo de texto, versionado, legível por humano e por modelo.

### 4.1 Pin (Invariante) — D + L

Arquivo imutável que descreve o que o projeto é. Propriedades verdadeiras independente do estado atual: regras, identidade, limites, restrições.

O Pin funciona como invariante de sistema. Projetos crescem em complexidade, mas invariantes mudam raramente. Quando há dúvida sobre o projeto, o agente consulta o Pin primeiro, porque é o documento mais estável e de menor custo cognitivo para processar.

**O que vai no Pin:**
- Identidade e escopo do projeto
- Regras imutáveis (restrições, políticas, limites)
- Entidades do domínio com definições não ambíguas
- Rotas de decisão com condições de entrada e saída
- Automações (crons, triggers, webhooks) formalizadas

**O que não vai no Pin:**
- Estado de execução, isso é Spec
- Histórico de decisões, isso é Handoff
- Preferências do operador humano, isso é outro documento

### 4.2 Spec (Comportamento) — L + A

Arquivo vivo que descreve o que fazer. Checklist sequencial de tarefas. Quanto mais tarefas e dependências, mais rápido o documento muda, por isso a Spec é mais volátil que o Pin.

A Spec é o espaço comportamental. Cada tarefa concluída é marcada e gera aprendizado. Tarefa marcada como concluída é imutável, nunca desmarca. Se o resultado tem defeito, cria nova tarefa corretiva referenciando a original. Mesmo princípio do Git: commits são imutáveis, correções são novos commits.

**Princípio da auto-contenção.** Toda tarefa numa Spec precisa sobreviver ao handoff. Quem escreve a tarefa raramente é quem a executa, pode ser outro agente, outra sessão, outro dia. Uma tarefa que depende de contexto implícito para ser entendida morre no momento em que o contexto morre. Por isso, cada entrada da Spec carrega uma camada de metadados suficiente para que qualquer executor posterior saiba o que fazer, por que aquilo existe, de onde veio a demanda e qual o caminho mínimo de implementação.

### 4.3 Handoff (Memória) — A para D

Registro estruturado que alimenta o próximo ciclo. Não é log de execução (o quê), é registro de estado (onde estamos, por que paramos, o que precisa continuar).

**Handoff contém:**
- Foco da sessão encerrada
- Decisões tomadas com justificativa
- Tarefas executadas com resultado
- Tarefas não executadas com razão
- Continuação: briefing de reengajamento para o próximo ciclo

**O handoff é a memória.** O modelo não precisa de persistência de estado próprio, porque o handoff da sessão N alimenta o boot da sessão N+1. Cada novo ciclo começa com contexto completo em minutos, sem banco vetorial, sem embeddings, sem memória stateful.

Uma distinção fina importa: isto não é "zero persistência". O filesystem persiste, a ontologia persiste, o handoff persiste. O que é zero é estado mantido dentro do modelo. A memória vive no documento, não no peso da rede neural.

## 5. Ciclo de Execução

O framework opera em quatro fases. Cada fase é explícita, cada fase gera artefato.

**Boot → Executar → Write-back → Handoff.** Um ciclo que fecha sobre si mesmo a cada sessão.

### Boot

Carregar Pin e Spec do projeto no início da sessão. Em sistemas com múltiplos agentes, o boot também carrega memória compartilhada (índice global) e a última entrada do handoff.

### Executar

Resolver tarefas na mesma sessão. Quantas a sessão comportar com qualidade. O limite não é número de tarefas, é degradação de contexto. Sinais práticos: o agente repete informação que já foi dita, perde referência a decisões anteriores da sessão, ou gera respostas genéricas onde antes era específico. Em termos de janela, operar acima de 50% da capacidade de contexto do modelo é zona de alerta. A FSTech usa 500K tokens como threshold de handoff em modelos com janela de 1M.

**Execução paralela (Wave).** Quando a Spec tem três ou mais tarefas independentes, o agente principal dispara sub-agentes em paralelo com contexto isolado. O principal preserva contexto para orquestração e raciocínio. Dependências são respeitadas: tarefa B que depende de A espera A concluir.

**Contexto isolado por tarefa pesada.** Para tarefas que envolvem leitura extensiva (análise de codebase, pesquisa, auditoria), delegar a sub-agente mesmo que sejam sequenciais. O sub-agente opera em contexto fresco, sem acumular resíduo. Isso evita degradação de qualidade por acúmulo de contexto irrelevante.

### Write-back (Commit Atômico)

A cada tarefa concluída:

- **Verificar** antes de marcar concluída, confirmar que a tarefa está realmente feita, com rigor proporcional ao risco
- **Commitar** uma tarefa, um commit. Mensagem referencia a tarefa. Rastreabilidade total via git bisect
- **Marcar concluída** na Spec
- **Anotar aprendizado** para a próxima tarefa, se houver

**Verificação pré-done (Gate programático).** Antes de marcar qualquer tarefa como concluída, o agente executa uma verificação proporcional ao risco da ação. Tarefas de baixo impacto passam por releitura de coerência. Tarefas de impacto médio exigem teste funcional. Tarefas de alto impacto exigem teste adversarial, revisão manual, e disciplina explícita contra vulnerabilidades conhecidas. O rigor não é uniforme porque o custo do erro não é uniforme.

**Anti-pattern canônico.** Verificação não é "rodei e não deu erro". É "tentei quebrar e não consegui".

### Handoff

Encerrar a sessão quando:

- Sinais de degradação aparecem: repetição de informação já coberta, perda de referência a decisões anteriores, respostas genéricas onde antes havia especificidade, ou consumo acima de 50% da janela de contexto do modelo
- Há mudança de projeto ou domínio
- O agente entra em território onde o contexto acumulado virou ruído, não sinal

**Procedimento: sempre nova sessão, nunca compactação.** Compactação é compressão lossy. Ela perde nuance, perde causalidade e paga um custo de contexto logo na abertura da sessão seguinte. Uma sessão nova com boot via Pin e Spec começa leve, recupera o estado completo a partir do que está documentado no filesystem e preserva a fidelidade dos fatos.

**Por que Handoff não é apenas outra compactação.** Handoff e compactação são dois atos distintos. Compactação é heurística automática aplicada ao histórico inteiro, sem objetivo além de reduzir tokens. Handoff é escrito com intenção explícita de continuidade. A assimetria não está no ato de escrever, está no propósito. Um é reação, o outro é protocolo.

## 6. Mapeamento D+L+A nos Componentes

| Camada | Onde vive | O que contém |
|--------|----------|-------------|
| Dados (D) | Pin + contexto herdado do Handoff anterior | Entidades, regras, estado inicial |
| Lógica (L) | Pin (rotas) + Spec (tarefas) + Gate pré-done | Regras de decisão e validação externa |
| Ação (A) | Execução + Handoff | Write-back no sistema real, memória para o próximo ciclo |

A validação externa (Gate pré-done) é o que elimina a circularidade. O agente não valida a si mesmo nas questões verificáveis externamente. Schema, permissões, estado de dependências, tudo é checado por código, não por opinião do modelo.

## 7. Write-Back Obrigatório

> If you think you know something but don't write it down, you only think you know it.
> — Leslie Lamport

Write-back não é apenas registro. É o próprio ato de pensar. Formular em texto revela lacunas, forçando precisão que o pensamento interno não exige.

Toda percepção, insight ou decisão gera write-back:
- Atualização de documento
- Criação de registro
- Alteração de estado
- Notificação acionável

**Métrica:** ciclo insight para write-back menor que um dia.

**Teste:** se é difícil de escrever, a ideia ainda não está madura.

Insight sem alteração do sistema real é lixo computacional.

## 8. Case Real: FSTech em Produção

O framework não é especulação. A FSTech opera sua frota interna de agentes neste framework há seis meses em produção, cinco canais ativos, múltiplos clientes.

**Frota operando sob o framework:**
- **Ares** agente orquestrador no terminal do operador, executa auditoria, refatoração, desenvolvimento, análise estratégica
- **Ontos** hub central da frota, roda em servidor dedicado, intermedia comunicação e orquestra agentes de campo
- **Finn** agente financeiro pessoal em produção para três clientes distintos, rodando em containers isolados, cada cliente com seu Pin
- **Chava** assistente pessoal rodando no notebook de uma cliente, integração com WhatsApp, calendário e contatos
- **Ares WhatsApp** mesmo agente orquestrador em canal de WhatsApp, comunicação direta com leads e clientes

**Prova técnica de portabilidade.** Ao longo dos seis meses de operação, a frota migrou entre modelos sem perder estado acumulado. Ares rodou com Claude em diferentes versões, Ontos opera parcialmente sobre modelos locais (Gemma), Finn mescla provedores comerciais conforme o custo por cliente. Em nenhuma dessas transições o conhecimento acumulado foi perdido, porque o conhecimento nunca esteve no modelo.

**Case externo validado.** Uma empresa cliente (VJ Turrini, consultoria empresarial) enfrentava o problema clássico: lógica operacional concentrada em duas pessoas, sem registro estruturado. Decisões sobre clientes, agenda e prioridades viviam na memória dos sócios. O agente (Chava) foi configurado com Pin próprio (regras do negócio, perfil de clientes, políticas de atendimento) e Spec operacional. A adoção aconteceu sem imposição: a operadora começou a consultar o agente via WhatsApp para tarefas reais, verificou que as respostas refletiam as regras do negócio, e passou a delegar progressivamente. Em quatro semanas, o agente respondia consultas de clientes, organizava agenda e mantinha histórico auditável de decisões. O caminho foi consulta, confiança, automação. Não o inverso.

## 9. Posicionamento

O framework não compete com frameworks de orquestração de chamadas (LangChain, CrewAI, AutoGen). Complementa. Esses frameworks resolvem como o agente chama ferramentas. O Framework de Ontologia Operacional FSTech resolve como o agente mantém estado auditável entre chamadas e execuções.

| Aspecto | Orquestração de chamadas | Framework FSTech |
|---------|------------------------|-----------------|
| Categoria | Orquestração de chamadas | Controle de estado e execução |
| Dependência | Stack específica | Agnóstico de modelo e de infra |
| Auditabilidade | Logs de execução | Handoff estruturado em documento |
| Memória | Persistente (banco vetorial, embeddings) | Documental (filesystem) |
| Relação | Pode rodar sobre qualquer um | Pode rodar sob qualquer um |

**Comparativo com referências internacionais:**
- **Palantir Foundry** opera sob Closed World Assumption com ontologia centralizada. O Framework FSTech segue o mesmo princípio (se não está documentado, não existe para o sistema) mas substitui o stack proprietário por filesystem versionado. Mesmo paradigma, infraestrutura radicalmente mais simples.
- **Microsoft Fabric IQ Ontology** oferece contexto operacional para agentes via produto gerenciado. O Framework FSTech oferece o mesmo sem fornecedor único, sem lock-in, sem SaaS obrigatório.
- **Skan Agentic Ontology of Work** formaliza ontologia como linguagem comum entre agentes. O Framework FSTech vai além ao formalizar o ciclo de execução, não apenas o vocabulário.

### 9.1 Soberania de Memória

Quando a memória vive dentro do modelo, dentro do provider, dentro de um harness proprietário, quem usa o agente não controla seu próprio estado. Trocar de provider significa começar do zero.

O Framework de Ontologia Operacional FSTech resolve esse problema por construção. Como a memória vive em artefatos de filesystem versionados (Pin, Spec, Handoff), a frota é portável por desenho. Um agente que rodou com Claude ontem pode rodar com Gemini amanhã, com GPT na semana seguinte, com um modelo local depois, e o estado acumulado continua válido.

Isso não é uma feature adicionada para atrair quem teme lock-in. É consequência direta do princípio inicial de que a memória vive no documento.

## 10. Validação N5

Todo componente do framework passa pelo **N5**, metodologia proprietária de validação analítica desenvolvida pela FSTech. O N5 aplica cinco critérios hierárquicos sobre qualquer solução ou sistema antes de considerá-lo production-ready. A hierarquia interna prioriza evidência empírica sobre elegância teórica.

O Framework de Ontologia Operacional FSTech foi validado pelos cinco critérios do N5 antes de ser publicado. Detalhes completos da metodologia N5 estão disponíveis sob acordo de parceria com a FSTech.

## 11. Limites e Quando Não Usar

Um framework honesto declara onde não se aplica.

- **Agentes conversacionais puros** sem efeito colateral em sistemas reais. Um chatbot de FAQ não precisa de Pin, Spec ou Handoff.
- **Protótipos exploratórios** onde o objetivo é descobrir se o problema existe. Formalizar cedo demais cristaliza hipóteses erradas.
- **Sistemas stateless verdadeiros** onde cada execução é independente. Function as a service, transformações puras, pipelines determinísticos.
- **Equipes sem disciplina de write-back.** O framework falha silenciosamente quando operadores ignoram o registro. Mas a solução não é cultura organizacional, é design de agente.

**Sobre a disciplina de write-back.** A objeção mais comum é que write-back depende de disciplina humana, e humanos esquecem. A resposta é que o agente é o operador principal, não o humano. No design correto, o próprio agente executa o write-back como parte do ciclo: atualiza a Spec ao concluir tarefa, gera o Handoff ao encerrar sessão, commita as mudanças. O humano não precisa lembrar de registrar porque não é ele quem registra. A disciplina está codificada no prompt do agente, não na rotina da equipe. O ponto de falha real não é esquecimento humano, é um agente mal configurado que não recebeu a instrução de registrar. Isso é resolvido no Pin, não em treinamento de pessoas.

### 11.1 Lacuna Empírica Declarada

A prova apresentada (seis meses de operação, cinco agentes, caso VJ Turrini) é evidência operacional, não métrica quantitativa. Não há neste documento: taxa de falha de boot, tempo médio de recuperação por handoff, comparação controlada contra baseline sem write-back.

A disciplina de write-back que o próprio framework prescreve torna essas métricas produzíveis. O material bruto existe, apenas não foi compilado em relatório público até esta versão.

**Roadmap empírico (compromisso público):**
- Métricas de ciclo publicadas em versão futura (ciclos/semana, tempo médio de boot, tempo médio de handoff)
- Comparação controlada contra baseline sem write-back
- Estudo de preservação de estado em transição entre três provedores diferentes

Leia este framework como descrição de mecanismo e convite à verificação, não como artigo científico com métricas arbitradas.

## 12. Este Documento é um Snapshot

O framework aqui descrito não é um estado final. É o recorte de abril de 2026 de um sistema que continua em movimento, exatamente através do ciclo que descreve. Cada componente é refinado pelo próprio write-back que ele governa.

Em termos da tríade, o framework é Dados (estrutura documental), Lógica (ciclo de execução) e Ação (write-back obrigatório), aplicado recursivamente a si mesmo.

## 13. Próximos Passos

Este documento é a versão pública do framework que a FSTech opera internamente. A versão interna inclui:

- Templates executáveis de Pin e Spec por tipo de projeto
- Toolchain de boot e handoff history-based
- Protocolos adjacentes (isolamento de canal, notificação escalonada, firewall de qualificação)
- Metodologia N5 completa aplicada a cada artefato
- Integrações específicas com ferramentas de operação

A versão pública é suficiente para adoção em projetos reais. Organizações que quiserem acelerar adoção podem [contatar a FSTech diretamente](https://fstech.digital/contato).

---

## Sobre a FSTech

A FSTech é uma consultoria brasileira focada em operacionalizar negócios através de ontologias executáveis e agentes de IA em produção. O produto é a operação, não o documento.

- **Fundador:** Felipe Silva
- **Site:** [fstech.digital](https://fstech.digital)
- **Framework (canônico):** [fstech.digital/framework](https://fstech.digital/framework/)
- **Newsletter:** [fstech.digital/newsletter](https://fstech.digital/newsletter/)
- **X:** [@fs_tech_](https://x.com/fs_tech_)

---

Framework de Ontologia Operacional FSTech v1.0 · Abril 2026 · [CC BY 4.0](LICENSE)

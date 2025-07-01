# equipe_mestre/tarefas.py

from crewai import Task
from crewai.agent import Agent
import json

class TarefasEquipeMestre:
    def __init__(self):
        pass

    # ... (as tarefas analisar_requisitos e identificar_ferramentas permanecem inalteradas) ...
    def analisar_requisitos(self, agent: Agent, comando_usuario: str, contexto_arquivo: str):
        return Task(
            description=f"""
                Sua tarefa é **extrair os requisitos detalhados** para uma equipe de IA com base na solicitação do usuário e no conteúdo do arquivo de contexto.

                ⚠️ **REGRA CRÍTICA: SUA RESPOSTA FINAL DEVE CONTER APENAS UM BLOCO DE TEXTO EM MARKDOWN.**
                - NÃO inclua frases como "Final Answer:", "Here is the output", ou pensamentos do agente.
                - Sua resposta deve começar diretamente com: `# Requisitos da Equipe de IA`
                - Nada deve vir antes ou depois do bloco Markdown.

                **Solicitação do Usuário:**
                {comando_usuario}

                **Contexto do Arquivo:**
                {contexto_arquivo if contexto_arquivo else "Nenhum contexto de arquivo fornecido."}

                **EXEMPLO DE SAÍDA PERFEITA (APENAS O MARKDOWN):**
                ```markdown
                # Requisitos da Equipe de IA
                ## 1. Objetivo Principal:
                [Descreva o objetivo principal]
                ## 2. Funcionalidades Chave Necessárias:
                - [Funcionalidade 1]
                - [Funcionalidade 2]
                ## 3. Resultado Final Esperado:
                [Descreva o resultado esperado]
                ```
            """,
            expected_output='Documento em Markdown iniciando com "# Requisitos da Equipe de IA", sem nenhum texto adicional.',
            agent=agent,
        )

    def identificar_ferramentas(self, agent: Agent):
        return Task(
            description="""
                Com base na análise de requisitos fornecida no contexto, sua tarefa é identificar e listar
                as ferramentas da biblioteca `crewai[tools]` que serão essenciais para a equipe.
                Utilize a ferramenta `Catálogo de Ferramentas da CrewAI` para consultar as ferramentas disponíveis.
                **REGRA MAIS IMPORTANTE:** A SUA RESPOSTA FINAL DEVE CONTER APENAS E SOMENTE A LISTA EM MARKDOWN.
                NÃO INCLUA "I now can give a great answer", "Final Answer:", pensamentos, ou qualquer outra frase.
                A SUA RESPOSTA DEVE COMEÇAR DIRETAMENTE COM O PRIMEIRO ITEM DA LISTA, como no exemplo.
                **Análise de Requisitos (Contexto da Tarefa Anterior):**
                {context}
                **EXEMPLO DE SAÍDA PERFEITA (APENAS O MARKDOWN):**
                ```markdown
                - DuckDuckGoSearchTool (crewai_tools)
                ```
            """,
            expected_output='Uma lista Markdown das ferramentas recomendadas (NomeDaFerramenta (biblioteca)), sem nenhum texto adicional.',
            agent=agent,
        )

    def projetar_equipe(self, agent: Agent):
        return Task(
            description="""
                Você é um Arquiteto de Equipes de IA. Sua missão é transformar os requisitos e ferramentas recebidas em uma estrutura funcional de agentes e tarefas.
                
                ⚠️ **REGRA CRÍTICA: A RESPOSTA FINAL DEVE SER EXCLUSIVAMENTE UM OBJETO JSON.**
                - Nenhum texto antes ou depois do JSON.
                - O JSON deve seguir rigorosamente a estrutura abaixo.
                - Qualquer desvio nos nomes das chaves ou formatos causará falhas na próxima etapa.

                **ESTRUTURA OBRIGATÓRIA:**

                - `agentes`: Lista com objetos contendo:
                    - `name` (string)
                    - `role` (string)
                    - `goal` (string)
                    - `backstory` (string)
                    - `llm` (sempre "llm")
                    - `verbose` (sempre true)
                    - `allow_delegation` (sempre false)
                    - `tools` (lista de strings com nomes das classes de ferramentas)

                - `tarefas`: Lista com objetos contendo:
                    - `name` (string)
                    - `description` (string)
                    - `expected_output` (string)
                    - `agent` (string correspondente ao `name` do agente)
                    - `context` (lista de strings com nomes de tarefas anteriores)

                **Contexto (Análise + Ferramentas):**
                {context}

                **EXEMPLO DE RESPOSTA VÁLIDA (APENAS O JSON):**
                ```json
                {{
                    "agentes": [
                        {{
                            "name": "Especialista de Documentação",
                            "role": "Gerador de relatórios técnicos",
                            "goal": "Criar relatórios Markdown baseados em resultados de tarefas.",
                            "backstory": "Profissional experiente em documentação de sistemas de IA.",
                            "llm": "llm",
                            "verbose": true,
                            "allow_delegation": false,
                            "tools": ["MarkdownFormatterTool"]
                        }}
                    ],
                    "tarefas": [
                        {{
                            "name": "Gerar Documentação",
                            "description": "Converter os resultados técnicos em um relatório em Markdown.",
                            "expected_output": "Relatório completo em formato Markdown.",
                            "agent": "Especialista de Documentação",
                            "context": ["Resultados Técnicos"]
                        }}
                    ]
                }}
                ```
            """,
            expected_output='Objeto JSON com chaves "agentes" e "tarefas", formatado corretamente, sem qualquer conteúdo adicional.',
            agent=agent,
        )

    def implementar_equipe_python(self, agent: Agent):
        return Task(
            description="""
                Você é um Engenheiro de Software especializado em CrewAI. Sua tarefa é transformar o plano JSON recebido no contexto em um script Python totalmente funcional.

                ⚠️ **REGRA CRÍTICA:** Sua resposta final deve ser **APENAS** um bloco de código Python Markdown.
                - Comece com ```python
                - Termine com ```
                - Nada fora desse bloco será aceito.

                **ETAPAS OBRIGATÓRIAS DO SCRIPT:**

                1. **Imports essenciais:** Use o exemplo abaixo como guia.
                2. **Configuração inicial:** `load_dotenv()` e `llm = ChatOpenAI(...)`.
                3. **Instanciação de ferramentas:** `nome_tool = ClasseTool()`.
                4. **Instanciação dos agentes:** Crie cada agente com `Agent(...)`.
                5. **Instanciação das tarefas:** Crie cada tarefa com `Task(...)`.
                6. **Montagem da crew:** Crie o objeto `Crew(...)`.

                ---
                **EXEMPLO DE IMPORTS CORRETOS:**
                ```python
                import os
                from dotenv import load_dotenv
                from crewai import Agent, Task, Crew, Process
                from langchain_openai import ChatOpenAI
                # Substitua abaixo pelas ferramentas REAIS necessárias, extraídas do JSON
                from crewai_tools import DuckDuckGoSearchTool, FileReadTool 
                ```
                ---

                **Plano JSON da Equipe:**
                {context}
            """,
            expected_output='Bloco de código Python válido, completo e funcional, formatado corretamente com ```python.',
            agent=agent,
        )

    def validar_codigo(self, agent: Agent):
        return Task(
            description="""
                Você é um Revisor de Qualidade de Código. Sua tarefa é garantir que o script Python
                fornecido no contexto seja sintaticamente válido e livre de erros óbvios.
                Utilize a ferramenta `Verificador de Sintaxe Python` (`verificador_de_sintaxe_python`)
                para analisar o código.
                **Script Python a ser Validado (do Agente 4, do contexto):**
                {context}
                Sua **RESPOSTA FINAL** deve ser apenas uma das seguintes frases:
                - "Validação bem-sucedida: O script Python está sintaticamente válido."
                - "Erro de validação: [Mensagem de erro da ferramenta]."
                NÃO inclua nenhum texto adicional, pensamentos ou explicações.
            """,
            expected_output='Uma mensagem indicando o sucesso da validação sintática ou o erro encontrado.',
            agent=agent,
        )
# equipe_mestre/tarefas.py

from crewai import Task
from crewai.agent import Agent # Importe Agent para tipagem se necessário
import json # Importar a biblioteca json para parsing

class TarefasEquipeMestre:
    def __init__(self):
        pass

    def analisar_requisitos(self, agent: Agent, comando_usuario: str, contexto_arquivo: str):
        return Task(
            description=f"""
                Analise a solicitação do usuário e o conteúdo do arquivo de contexto para extrair os
                requisitos para uma nova equipe de IA.

                Seu objetivo é gerar um documento claro e conciso que servirá de base
                para os outros agentes.

                **A RESPOSTA FINAL DEVE CONTER APENAS O TEXTO FORMATADO EM MARKDOWN**, conforme o exemplo.
                **NÃO INCLUA NENHUMA FRASE INTRODUTÓRIA, DESPEDIDA, PENSAMENTOS OU QUALQUER TEXTO ADICIONAL FORA DO BLOCO MARKDOWN.**

                **Solicitação do Usuário:**
                {comando_usuario}

                **Contexto do Arquivo:**
                {contexto_arquivo if contexto_arquivo else "Nenhum contexto de arquivo fornecido."}

                **EXEMPLO DE SAÍDA ESPERADA (APENAS O MARKDOWN, SEM TEXTO EXTRA):**
                ```markdown
                # Requisitos da Equipe de IA

                ## 1. Objetivo Principal:
                [Descreva o objetivo principal da equipe, por exemplo, 'Gerar conteúdo otimizado para SEO para loja de sapatos veganos']

                ## 2. Funcionalidades Chave Necessárias:
                - [Funcionalidade 1]
                - [Funcionalidade 2]
                - [Funcionalidade N]

                ## 3. Resultado Final Esperado:
                [Descreva o resultado concreto, por exemplo, 'Aumento de X% no tráfego orgânico e Y% nas vendas.']
                ```
            """,
            expected_output='Um documento de análise detalhado formatado em Markdown, sem texto adicional.',
            agent=agent,
        )

    def identificar_ferramentas(self, agent: Agent, contexto_analise_requisitos: str):
        return Task(
            description=f"""
                Com base na análise de requisitos fornecida, sua tarefa é identificar e listar
                as ferramentas da biblioteca `crewai[tools]` que serão essenciais para a equipe
                a ser criada.

                Utilize a ferramenta `Catálogo de Ferramentas da CrewAI` para consultar as ferramentas disponíveis.

                **A RESPOSTA FINAL DEVE CONTER APENAS A LISTA EM MARKDOWN**, conforme o exemplo.
                **NÃO INCLUA NENHUMA FRASE INTRODUTÓRIA, DESPEDIDA, PENSAMENTOS OU QUALQUER TEXTO ADICIONAL FORA DO BLOCO MARKDOWN.**

                **Análise de Requisitos:**
                {contexto_analise_requisitos}

                **EXEMPLO DE SAÍDA ESPERADA (APENAS O MARKDOWN):**
                ```markdown
                - DuckDuckGoSearchTool (crewai_tools)
                - WebsiteSearchTool (crewai_tools)
                - SeleniumScrapingTool (crewai_tools)
                ```
            """,
            expected_output='Uma lista Markdown das ferramentas recomendadas (NomeDaFerramenta (biblioteca)), sem texto adicional.',
            agent=agent,
        )

    def projetar_equipe(self, agent: Agent, analise_requisitos: str, ferramentas_recomendadas: str):
        return Task(
            description=f"""
                Você é um Arquiteto de Equipes de IA. Sua tarefa é projetar a estrutura completa da nova equipe,
                incluindo os Agentes e suas Tarefas, utilizando a análise de requisitos e as ferramentas recomendadas.

                **A RESPOSTA FINAL DEVE CONTER APENAS O OBJETO JSON BEM FORMATADO**, conforme o exemplo.
                **NÃO INCLUA NENHUM TEXTO EXPLICATIVO, PENSAMENTOS OU COMENTÁRIOS FORA DO BLOCO JSON.**
                **A saída DEVE ser APENAS o objeto JSON.**

                **IMPORTANTE:**
                - Inclua as ferramentas RECOMENDADAS PELO AGENTE 2 (com seus nomes EXATOS de classe) nos agentes que as utilizarão.
                - Use 'Crew' e 'Process.sequential' para a Crew.
                - Para cada Agente, inclua: 'name', 'role', 'goal', 'backstory', 'llm' (sempre use 'llm' como valor string literal, não 'self.llm'), 'verbose' (sempre 'true'), 'allow_delegation' (sempre 'false'), e 'tools' (lista de strings com nomes das ferramentas).
                - Para cada Tarefa, inclua: 'name', 'description', 'expected_output', 'agent' (referência ao 'name' do agente responsável), e 'context' (lista de strings referenciando saídas de tarefas anteriores, se houver).
                - Os valores booleanos para 'verbose' e 'allow_delegation' DEVERÃO ser `true` ou `false` (minúsculas) no JSON.

                **Análise de Requisitos (do Agente 1):**
                {analise_requisitos}

                **Ferramentas Recomendadas (do Agente 2):**
                {ferramentas_recomendadas}

                **EXEMPLO DE SAÍDA JSON ESPERADA (APENAS O JSON, SEM TEXTO EXTRA):**
                ```json
                {{
                    "equipe_nome": "Nome da Equipe Gerada (Ex: Equipe de Marketing de Conteúdo)",
                    "agentes": [
                        {{
                            "name": "Nome do Agente (Ex: 'Estrategista de Conteúdo')",
                            "role": "Papel do Agente",
                            "goal": "Objetivo do Agente",
                            "backstory": "História/Contexto do Agente",
                            "llm": "llm",
                            "verbose": true,
                            "allow_delegation": false,
                            "tools": ["DuckDuckGoSearchTool", "WebsiteSearchTool"]
                        }},
                        {{
                            "name": "Redator Criativo",
                            "role": "Criador de Conteúdo",
                            "goal": "Escrever posts de blog e textos persuasivos.",
                            "backstory": "Um mestre das palavras com foco em engajamento.",
                            "llm": "llm",
                            "verbose": true,
                            "allow_delegation": false,
                            "tools": []
                        }}
                    ],
                    "tarefas": [
                        {{
                            "name": "Pesquisa de Mercado",
                            "description": "Pesquisar tendências de mercado para sapatos veganos.",
                            "expected_output": "Relatório de tendências de mercado.",
                            "agent": "Estrategista de Conteúdo",
                            "context": []
                        }},
                        {{
                            "name": "Escrever Rascunho de Blog Post",
                            "description": "Escrever um rascunho de post de blog baseado na pesquisa de mercado.",
                            "expected_output": "Rascunho do post de blog.",
                            "agent": "Redator Criativo",
                            "context": ["Pesquisa de Mercado.output"]
                        }}
                    ],
                    "crew_settings": {{
                        "process": "Process.sequential",
                        "verbose": true
                    }}
                }}
                ```
            """,
            expected_output='Um objeto JSON estritamente formatado com o design completo da nova equipe.',
            agent=agent,
        )
    
    def implementar_equipe_python(self, agent: Agent, plano_design_equipe: str):
        return Task(
            description=f"""
                Você é um Engenheiro de Software de IA. Sua tarefa é converter o "Plano de Design da Equipe"
                (fornecido em formato JSON) em um **script Python completo e executável** utilizando a biblioteca CrewAI.

                **Seu processo deve ser:**
                1.  **Analise e PARSEIE o JSON** fornecido em `plano_design_equipe` para extrair todos os detalhes da equipe.
                2.  Com base nesses detalhes, **gere o código Python COMPLETO para o script da nova equipe como UMA ÚNICA STRING**. Este código DEVE incluir:
                    -   Todos os imports necessários (CrewAI, langchain_openai, dotenv, os, e ferramentas específicas de `crewai_tools`).
                    -   Configuração do LLM: `load_dotenv(); llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"))`.
                    -   Instanciação de CADA ferramenta listada no plano (e.g., `duckduckgo_tool = DuckDuckGoSearchTool()`).
                    -   Definição de CADA Agente com todas as propriedades (role, goal, backstory, llm, verbose, allow_delegation, tools - usando as instâncias de ferramentas criadas).
                    -   Definição de CADA Tarefa com todas as propriedades (description, expected_output, agent, context).
                    -   Montagem da Crew (Crew(agents=[...], tasks=[...], ...)). Não use `add_agent` ou `add_task`.
                
                3.  **A SUA RESPOSTA FINAL DEVE ser a string do CÓDIGO PYTHON GERADO (do passo 2), envolvida em um bloco de código Markdown (`python\\n...código aqui...\\n`).**
                    **NÃO ENVOLVA A STRING DO CÓDIGO EM UM DICIONÁRIO PARA PASSAR À FERRAMENTA `Escritor de Código Python`.** A ferramenta será chamada automaticamente com o que você retornar como Final Answer, desde que seja uma string no formato de bloco de código Python.
                    **NÃO inclua nenhum outro texto, pensamentos ou explicações ANTES ou DEPOIS do bloco de código Markdown.**

                **Plano de Design da Equipe (do Agente 3 - em JSON):**
                {plano_design_equipe}
            """,
            expected_output='APENAS o código Python completo do script da nova equipe, formatado estritamente dentro de um bloco de código Markdown (`python\\n...código aqui...\\n`).',
            agent=agent,
            # Adicionando uma instrução de back-end para tentar forçar o formato correto da saída.
            # Esta parte não faz parte do código, mas é uma explicação do ajuste de mentalidade do agente.
            # O agente precisa entender que o 'expected_output' é o formato final.
            # O ajuste real é nas instruções acima, enfatizando "APENAS a string... envolvida em um bloco de código Markdown".
            # E garantindo que a implementação do LLM siga essa instrução.
        )

    def validar_codigo(self, agent: Agent, script_python: str):
        return Task(
            description=f"""
                Você é um Revisor de Qualidade de Código. Sua tarefa é garantir que o script Python
                fornecido seja sintaticamente válido e livre de erros óbvios.

                Utilize a ferramenta `Verificador de Sintaxe Python` (`verificador_de_sintaxe_python`)
                para analisar o código.

                **Script Python a ser Validado (do Agente 4):**
                {script_python}

                Sua **RESPOSTA FINAL** deve ser apenas uma das seguintes frases:
                - "Validação bem-sucedida: O script Python está sintaticamente válido."
                - "Erro de validação: [Mensagem de erro da ferramenta]."
                NÃO inclua nenhum texto adicional, pensamentos ou explicações.
            """,
            expected_output='Uma mensagem indicando o sucesso da validação sintática ou o erro encontrado.',
            agent=agent,
        )
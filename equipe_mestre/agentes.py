# equipe_mestre/agentes.py

from crewai import Agent
from langchain_openai import ChatOpenAI
import os
# Importe as ferramentas necessárias para os agentes
from .ferramentas import code_writer_tool, verificador_de_sintaxe_python # Importe também o verificador

OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
llm = ChatOpenAI(model=OPENAI_MODEL_NAME)

class AgentesEquipeMestre:
    def __init__(self):
        self.llm = llm

    def analista_de_requisitos(self):
        return Agent(
            role='Analista de Requisitos de IA',
            goal='Interpretar a solicitação do usuário e o conteúdo do arquivo de contexto para criar uma especificação clara e detalhada dos requisitos da equipe a ser criada.',
            backstory='Com vasta experiência em engenharia de requisitos para sistemas de IA, este agente é meticuloso na extração e documentação de necessidades, garantindo que nenhum detalhe importante seja perdido.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def especialista_em_ferramentas(self, ferramentas_disponiveis):
        return Agent(
            role='Especialista em Ferramentas de Agentes de IA',
            goal='Com base na análise de requisitos, determinar precisamente quais ferramentas da biblioteca crewai[tools] a equipe gerada necessitará.',
            backstory='Este agente possui um conhecimento enciclopédico sobre as ferramentas disponíveis no ecossistema CrewAI, sabendo exatamente qual ferramenta se encaixa em cada necessidade.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=ferramentas_disponiveis
        )

    def designer_de_equipes(self):
        return Agent(
            role='Arquiteto de Equipes de IA',
            goal='Projetar a estrutura completa da nova equipe, incluindo papéis, objetivos, histórias de fundo e tarefas, utilizando a análise de requisitos e as ferramentas recomendadas.',
            backstory='Um arquiteto de sistemas de IA experiente, com um talento especial para construir equipes eficientes e coesas. Ele traduz requisitos em estruturas de agentes e tarefas, garantindo clareza e funcionalidade.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def implementador_de_equipes_python(self):
        return Agent(
            role='Engenheiro de Software de IA',
            goal='Converter o plano de design detalhado da equipe em um script Python funcional, bem comentado e que siga as melhores práticas da biblioteca CrewAI.',
            backstory='Com um olhar afiado para código limpo e eficiente, este engenheiro de software é um mestre em transformar especificações em soluções de software robustas.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=[code_writer_tool]
        )

    def validador_de_codigo(self):
        return Agent(
            role='Revisor de Qualidade de Código',
            goal='Garantir que o script Python gerado pelo Implementador seja sintaticamente válido e livre de erros óbvios.',
            backstory='Um analista de QA com expertise em código Python, implacável na busca por erros e inconsistências sintáticas.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=[verificador_de_sintaxe_python] # Atribuindo a ferramenta de validação
        )

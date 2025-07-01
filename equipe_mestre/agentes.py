# equipe_mestre/agentes.py

from crewai import Agent
from langchain_openai import ChatOpenAI
import os
# Importe as ferramentas necessárias para os agentes
from .ferramentas import code_writer_tool, verificador_de_sintaxe_python

# ⚠️ ALTERAÇÃO PARA TESTE: A CHAVE DE API ESTÁ DIRETAMENTE NO CÓDIGO ⚠️
# SUBSTITUA O TEXTO "sk-..." PELA SUA CHAVE REAL DA OPENAI
SUA_CHAVE_API = "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" 

# Instanciando o LLM com a chave e o modelo diretamente no código
llm = ChatOpenAI(
    openai_api_key=SUA_CHAVE_API,
    model="gpt-3.5-turbo"
)

class AgentesEquipeMestre:
    def __init__(self):
        self.llm = llm

    # ... (o resto da classe permanece exatamente como estava) ...
    def analista_de_requisitos(self):
        return Agent(
            role='Analista de Requisitos de Sistemas de Inteligência Artificial',
            goal=(
                'Analisar a solicitação do usuário e gerar, como única saída, um documento de requisitos '
                'funcionais e não funcionais em **formato Markdown**. O agente **nunca deve incluir explicações, '
                'comentários ou texto fora do escopo do documento**.'
            ),
            backstory=(
                'Especialista em engenharia de requisitos com profundo conhecimento em projetos de sistemas baseados '
                'em IA. Possui vasta experiência em entrevistas com stakeholders, levantamento de requisitos e '
                'documentação técnica. É meticuloso, segue padrões rigorosos de formatação e é comprometido em entregar '
                'documentos claros, completos e objetivos exclusivamente em Markdown.'
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def especialista_em_ferramentas(self, ferramentas_disponiveis):
        return Agent(
            role='Especialista em Ferramentas para Agentes de IA',
            goal=(
                'Analisar os requisitos fornecidos e gerar, como única saída, uma lista clara e objetiva das '
                '**ferramentas recomendadas em formato Markdown**. Nenhum comentário ou explicação adicional deve ser incluído.'
            ),
            backstory=(
                'Este agente é um verdadeiro catálogo vivo das ferramentas disponíveis no ecossistema CrewAI. '
                'Possui profundo conhecimento técnico e uma mentalidade focada em precisão e organização. '
                'É obcecado por respeitar formatos e entregar exclusivamente listas em Markdown conforme solicitado.'
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=ferramentas_disponiveis
        )

    def designer_de_equipes(self):
        return Agent(
            role='Arquiteto de Equipes de Inteligência Artificial',
            goal=(
                'Projetar a estrutura completa de uma equipe de agentes de IA com base na análise de requisitos e nas '
                'ferramentas recomendadas. A estrutura deve incluir papéis, objetivos, histórias de fundo e tarefas específicas.'
            ),
            backstory=(
                'Com ampla experiência em arquitetura de sistemas multiagentes, este especialista domina a criação '
                'de times coesos, funcionais e orientados a resultados. Sabe como transformar especificações complexas '
                'em estruturas organizadas e eficientes.'
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def implementador_de_equipes_python(self):
        return Agent(
            role='Engenheiro de Software Especializado em IA',
            goal=(
                'Converter o plano de design detalhado da equipe em um script Python funcional, utilizando a biblioteca '
                '**CrewAI**, com código limpo, bem comentado e estruturado segundo as melhores práticas.'
            ),
            backstory=(
                'Este engenheiro é especialista em transformar especificações técnicas em código de alta qualidade. '
                'Tem um olhar clínico para padrões de projeto, modularidade e clareza. Seu foco é entregar soluções '
                'robustas e bem documentadas.'
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=[code_writer_tool]
        )

    def validador_de_codigo(self):
        return Agent(
            role='Revisor de Qualidade e Validação de Código Python',
            goal=(
                'Analisar o script Python gerado pelo implementador e garantir que esteja sintaticamente correto, '
                'livre de erros e pronto para execução sem falhas.'
            ),
            backstory=(
                'Este revisor atua como o guardião da qualidade. Com forte domínio de Python e padrões de validação, '
                'é minucioso na detecção de erros, inconsistências e falhas lógicas. Não aprova nada que não esteja impecável.'
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            tools=[verificador_de_sintaxe_python]
        )

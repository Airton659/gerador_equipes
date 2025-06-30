python
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from crewai.tools import DuckDuckGoSearchTool, FileReadTool, DirectoryReadTool, SerperDevTool, SeleniumScrapingTool

load_dotenv()
llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"))

arquiteto_de_aplicativos = Agent(
    name="Arquiteto de Aplicativos",
    role="Arquiteto de Sistemas",
    goal="Planejar a estrutura e arquitetura do aplicativo Flutter",
    backstory="Um especialista em design de software altamente experiente.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    tools=[DuckDuckGoSearchTool(), FileReadTool()]
)

designer_de_ui_ux = Agent(
    name="Designer de UI/UX",
    role="Designer de Interface de Usuário",
    goal="Criar protótipos de UI/UX para o aplicativo Flutter",
    backstory="Um artista digital especializado em experiência do usuário.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    tools=[DirectoryReadTool()]
)

engenheiro_de_flutter = Agent(
    name="Engenheiro de Flutter",
    role="Desenvolvedor Flutter",
    goal="Gerar automaticamente o código-fonte do aplicativo Flutter",
    backstory="Um programador habilidoso com experiência em Flutter.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    tools=[SerperDevTool(), SeleniumScrapingTool()]
)

qa_tecnico = Agent(
    name="QA Técnico",
    role="Analista de Qualidade Técnica",
    goal="Realizar validações técnicas e revisões de qualidade",
    backstory="Um detetive técnico obcecado pela perfeição.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    tools=[]
)

input_do_usuario = Task(
    name="Input do Usuário",
    description="Receber a descrição do aplicativo a ser desenvolvido",
    expected_output="Descrição detalhada do aplicativo",
    agent=arquiteto_de_aplicativos,
    context=[]
)

planejamento_de_arquitetura = Task(
    name="Planejamento de Arquitetura",
    description="Colaborar para planejar a arquitetura do aplicativo",
    expected_output="Plano de arquitetura do aplicativo",
    agent=arquiteto_de_aplicativos,
    context=["Input do Usuário.output"]
)

criacao_de_prototipos = Task(
    name="Criação de Protótipos",
    description="Desenvolver protótipos de UI/UX para o aplicativo",
    expected_output="Protótipos de interface do usuário",
    agent=designer_de_ui_ux,
    context=["Planejamento de Arquitetura.output"]
)

geracao_de_codigo_fonte = Task(
    name="Geração de Código-Fonte",
    description="Gerar automaticamente o código-fonte do aplicativo Flutter",
    expected_output="Código-fonte do aplicativo Flutter",
    agent=engenheiro_de_flutter,
    context=["Criação de Protótipos.output"]
)

validacoes_tecnicas_e_revisoes = Task(
    name="Validações Técnicas e Revisões",
    description="Realizar validações técnicas e revisões de qualidade no código",
    expected_output="Relatório de validações e revisões",
    agent=qa_tecnico,
    context=["Geração de Código-Fonte.output"]
)

crew = Crew(
    agents=[arquiteto_de_aplicativos, designer_de_ui_ux, engenheiro_de_flutter, qa_tecnico],
    tasks=[input_do_usuario, planejamento_de_arquitetura, criacao_de_prototipos, geracao_de_codigo_fonte, validacoes_tecnicas_e_revisoes],
    process="Process.sequential",
    verbose=True
)
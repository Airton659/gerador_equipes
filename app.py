# app.py

# --- INÍCIO DA CORREÇÃO DEFINITIVA DO SQLITE ---
# Força o uso da versão correta do SQLite que foi instalada via pip.
# Este bloco DEVE ser o primeiro código a ser executado no script.
try:
  __import__('pysqlite3')
  import sys
  sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
  pass
# --- FIM DA CORREÇÃO ---


import streamlit as st
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
import re # Importar a biblioteca de expressões regulares

from crewai import Crew, Process
from crewai.agent import Agent 
from crewai.task import Task 

# Importando as classes que criamos
from equipe_mestre.agentes import AgentesEquipeMestre
from equipe_mestre.tarefas import TarefasEquipeMestre
from equipe_mestre.ferramentas import catalogo_de_ferramentas

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- FUNÇÃO HELPER PARA EXTRAIR TEXTO ---
def extrair_texto_de_arquivo(arquivo_carregado):
    if arquivo_carregado is None:
        return ""
    nome_arquivo = arquivo_carregado.name
    with open(nome_arquivo, "wb") as f:
        f.write(arquivo_carregado.getbuffer())
    texto = ""
    try:
        if nome_arquivo.endswith('.pdf'):
            with fitz.open(nome_arquivo) as doc:
                for page in doc:
                    texto += page.get_text()
        elif nome_arquivo.endswith(('.txt', '.md')):
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                texto = f.read()
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
    finally:
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
    return texto

# --- FUNÇÃO HELPER PARA EXTRAIR SAÍDA ---
def get_task_output_as_string(task_output) -> str:
    """Extrai a saída da tarefa de forma mais robusta."""
    if task_output is None:
        return ""
    if hasattr(task_output, 'raw_output') and task_output.raw_output:
        return task_output.raw_output
    return str(task_output)


# --- INTERFACE DO STREAMLIT ---
st.set_page_config(page_title="Gerador de Equipes de IA", layout="wide")
st.title("🤖 Gerador de Equipes de IA com CrewAI")
st.info(
    "Descreva o objetivo da equipe que você precisa e, se necessário, "
    "anexe um arquivo de contexto (como um cardápio, catálogo ou relatório) "
    "para gerar uma equipe de agentes de IA personalizada."
)

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Descreva sua necessidade")
    prompt_usuario = st.text_area(
        "Ex: Crie uma equipe para atendimento ao cliente de um restaurante.", height=150
    )
with col2:
    st.subheader("2. Forneça o contexto (Opcional)")
    arquivo_contexto_carregado = st.file_uploader(
        "Anexe um arquivo (.pdf, .md, .txt)", type=["pdf", "md", "txt"]
    )

st.divider()

if st.button("Gerar Equipe de Agentes"):
    if not prompt_usuario:
        st.error("Por favor, descreva a necessidade da equipe antes de continuar.")
    else:
        # Configurando a chave de API a partir dos Secrets do Streamlit
        try:
            os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        except FileNotFoundError:
            st.error("Arquivo de secrets não encontrado. Crie um arquivo .streamlit/secrets.toml localmente ou adicione o Secret no app do Streamlit Cloud.")
        except KeyError:
            st.error("A chave OPENAI_API_KEY não foi encontrada nos seus Secrets. Por favor, adicione-a.")

        with st.spinner("Aguarde... A equipe-mestre está se reunindo para analisar sua solicitação..."):
            
            contexto_arquivo_texto = extrair_texto_de_arquivo(arquivo_contexto_carregado)
            
            # --- MONTAGEM E EXECUÇÃO DA EQUIPE-MESTRE ---
            
            agentes_creator = AgentesEquipeMestre()
            tarefas_creator = TarefasEquipeMestre()

            # Agentes
            analista = agentes_creator.analista_de_requisitos()
            especialista = agentes_creator.especialista_em_ferramentas(
                ferramentas_disponiveis=[catalogo_de_ferramentas]
            )
            designer = agentes_creator.designer_de_equipes()
            implementador = agentes_creator.implementador_de_equipes_python()
            validador = agentes_creator.validador_de_codigo()

            # Tarefas
            tarefa_analise = tarefas_creator.analisar_requisitos(
                agent=analista, 
                comando_usuario=prompt_usuario,
                contexto_arquivo=contexto_arquivo_texto
            )
            tarefa_ferramentas = tarefas_creator.identificar_ferramentas(agent=especialista)
            tarefa_projeto = tarefas_creator.projetar_equipe(agent=designer)
            tarefa_implementacao = tarefas_creator.implementar_equipe_python(agent=implementador)
            tarefa_validacao = tarefas_creator.validar_codigo(agent=agent)
            
            # Definindo o contexto (dependências) para cada tarefa.
            tarefa_ferramentas.context = [tarefa_analise]
            tarefa_projeto.context = [tarefa_analise, tarefa_ferramentas]
            tarefa_implementacao.context = [tarefa_projeto]
            tarefa_validacao.context = [tarefa_implementacao]

            # A Crew é criada com as tarefas definidas.
            equipe_mestre_completa = Crew(
                agents=[analista, especialista, designer, implementador, validador],
                tasks=[tarefa_analise, tarefa_ferramentas, tarefa_projeto, tarefa_implementacao, tarefa_validacao],
                process=Process.sequential,
                verbose=True
            )

            try:
                # O kickoff retornará a saída da ÚLTIMA tarefa (validação)
                resultado_final_crew = equipe_mestre_completa.kickoff()
                
                st.divider()
                st.subheader("Resultado Final do Processo de Geração de Equipes")
                st.markdown(f"**Status da Validação do Código:** `{resultado_final_crew}`")
                st.markdown("---")
                st.subheader("Código Python Gerado:")

                # Acessando o output da tarefa de implementação.
                codigo_gerado_com_markdown = get_task_output_as_string(tarefa_implementacao.output)
                
                match = re.search(r"```\s*python\n(.*?)\n```", codigo_gerado_com_markdown, re.DOTALL)
                
                if match:
                    clean_code = match.group(1).strip()
                    st.code(clean_code, language='python')
                else:
                    st.info("O formato do código gerado não contém um bloco de código Python Markdown válido. Exibindo saída bruta para depuração:")
                    st.code(codigo_gerado_com_markdown, language='text')

            except Exception as e:
                st.error(f"Ocorreu um erro durante a execução da equipe: {e}")
                st.info("Verifique se sua chave de API do LLM está configurada corretamente nos Secrets do Streamlit e se todas as dependências estão instaladas.")
                st.subheader("Saídas das tarefas para depuração:")
                # Exibindo os outputs brutos para ajudar a depurar
                st.markdown("**Saída da Análise (Agente 1):**")
                st.code(get_task_output_as_string(tarefa_analise.output), language='markdown')
                st.markdown("**Saída das Ferramentas (Agente 2):**")
                st.code(get_task_output_as_string(tarefa_ferramentas.output), language='markdown')
                st.markdown("**Saída do Design (Agente 3):**")
                st.code(get_task_output_as_string(tarefa_projeto.output), language='json')
                st.markdown("**Saída da Implementação (Agente 4):**")
                st.code(get_task_output_as_string(tarefa_implementacao.output), language='text')

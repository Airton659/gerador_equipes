# app.py
import streamlit as st
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
import re # Importar a biblioteca de expressões regulares

from crewai import Crew, Process
from crewai.agent import Agent # Necessário para TaskOutput
from crewai.task import Task # Necessário para TaskOutput

# Importando as classes que criamos
from equipe_mestre.agentes import AgentesEquipeMestre
from equipe_mestre.tarefas import TarefasEquipeMestre
from equipe_mestre.ferramentas import catalogo_de_ferramentas # Importe a ferramenta personalizada

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- FUNÇÃO HELPER PARA EXTRAIR TEXTO ---
def extrair_texto_de_arquivo(arquivo_carregado):
    if arquivo_carregado is None:
        return ""
    
    # Usa o nome original para evitar problemas com caminhos
    nome_arquivo = arquivo_carregado.name
    
    # Salva o arquivo temporariamente
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
        # Remove o arquivo temporário
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)
        
    return texto

# --- FUNÇÃO HELPER PARA EXTRAIR SAÍDA DE TAREFA DE FORMA SEGURA ---
# Esta função foi aprimorada para tentar capturar a string real da saída
# especialmente quando a CrewAI retorna um objeto TaskOutput ou se o agente
# não formatou sua Final Answer corretamente.
def get_task_output_as_string(task_obj_or_str) -> str:
    """Tenta extrair a saída da tarefa como string, lidando com diferentes formatos de output da CrewAI."""
    if isinstance(task_obj_or_str, str):
        return task_obj_or_str
    # Se for um objeto TaskOutput (CrewAI v0.20+), acessa raw_output ou description
    if hasattr(task_obj_or_str, 'raw_output') and isinstance(task_obj_or_str.raw_output, str):
        return task_obj_or_or_str.raw_output
    if hasattr(task_obj_or_str, 'description') and isinstance(task_obj_or_str.description, str):
        return task_obj_or_str.description
    # Para versões mais antigas ou outros objetos, tenta str()
    if hasattr(task_obj_or_str, '__str__'):
        return str(task_obj_or_str)
    return ""

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
        with st.spinner("Aguarde... A equipe-mestre está se reunindo para analisar sua solicitação..."):
            
            contexto_arquivo_texto = extrair_texto_de_arquivo(arquivo_contexto_carregado)
            
            # --- MONTAGEM E EXECUÇÃO DA EQUIPE DE TESTE ---
            
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
            
            # As tarefas dependem do .output da tarefa anterior, que será populado pelo kickoff da Crew
            tarefa_ferramentas = tarefas_creator.identificar_ferramentas(
                agent=especialista,
                contexto_analise_requisitos=get_task_output_as_string(tarefa_analise.output) # Garante que seja string
            )
            
            tarefa_projeto = tarefas_creator.projetar_equipe(
                agent=designer,
                analise_requisitos=get_task_output_as_string(tarefa_analise.output), # Garante que seja string
                ferramentas_recomendadas=get_task_output_as_string(tarefa_ferramentas.output) # Garante que seja string
            )

            tarefa_implementacao = tarefas_creator.implementar_equipe_python(
                agent=implementador,
                plano_design_equipe=get_task_output_as_string(tarefa_projeto.output) # Garante que seja string
            )

            tarefa_validacao = tarefas_creator.validar_codigo(
                agent=validador,
                script_python=get_task_output_as_string(tarefa_implementacao.output) # Garante que seja string
            )

            # A Crew é criada com as tarefas definidas. O kickoff gerenciará a execução e a passagem de outputs.
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
                st.markdown(f"**Status da Validação do Código:** {resultado_final_crew}")
                st.markdown("---")
                st.subheader("Código Python Gerado (para referência):")

                # Acessando o output da tarefa de implementação. CrewAI popula o .output das tasks após a execução.
                codigo_gerado_com_markdown = get_task_output_as_string(tarefa_implementacao.output)
                
                # Modificação principal aqui: Ajuste do regex para capturar 'python' em uma nova linha
                match = re.search(r"```\s*python\n(.*)```", codigo_gerado_com_markdown, re.DOTALL)
                
                if match:
                    clean_code = match.group(1).strip()
                    st.code(clean_code, language='python')
                else:
                    st.info("O formato do código gerado não contém um bloco de código Python Markdown válido.")
                    st.code(codigo_gerado_com_markdown, language='text') # Exibe o conteúdo bruto para depuração

            except Exception as e:
                st.error(f"Ocorreu um erro durante a execução da equipe: {e}")
                st.info("Verifique se sua chave de API do LLM está configurada corretamente no arquivo .env e se todas as dependências estão instaladas.")
                st.subheader("Última Saída Conhecida (bruta para depuração):")
                # Tenta mostrar o output bruto das tarefas para depuração
                st.code(get_task_output_as_string(tarefa_implementacao.output) if hasattr(tarefa_implementacao, 'output') else "Nenhuma saída do implementador disponível.", language='text')
                st.markdown(f"**Saída da Tarefa de Análise (bruta):**\n`{get_task_output_as_string(tarefa_analise.output)}`")
                st.markdown(f"**Saída da Tarefa de Ferramentas (bruta):**\n`{get_task_output_as_string(tarefa_ferramentas.output)}`")
                st.markdown(f"**Saída da Tarefa de Projeto (bruta):**\n`{get_task_output_as_string(tarefa_projeto.output)}`")
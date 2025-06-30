# equipe_mestre/ferramentas.py

from crewai.tools import tool
# Importe a biblioteca ast para o verificador_de_sintaxe_python
import ast 

@tool("Catálogo de Ferramentas da CrewAI")
def catalogo_de_ferramentas() -> str:
    """
    Retorna uma lista e descrição de todas as ferramentas disponíveis na biblioteca `crewai_tools`
    que podem ser usadas por outros agentes.
    """
    return """
    Aqui está uma lista de ferramentas disponíveis na biblioteca `crewai_tools`:
    - DuckDuckGoSearchTool: Usada para realizar pesquisas na internet com o DuckDuckGo.
    - FileReadTool: Usada para ler o conteúdo de um arquivo local.
    - DirectoryReadTool: Usada para listar o conteúdo de um diretório.
    - WebsiteSearchTool: Usada para pesquisar e extrair conteúdo de websites específicos.
    - SerperDevTool: Uma ferramenta alternativa para pesquisa na web que usa a API do serper.dev.
    - SeleniumScrapingTool: Usada para tarefas de web scraping complexas que exigem a renderização de JavaScript.
    """

@tool("Escritor de Código Python")
def code_writer_tool(code_string: str) -> str:
    """
    Recebe uma string contendo código Python e a retorna.
    Esta ferramenta serve para o Agente Implementador 'finalizar' a escrita do código.
    """
    return code_string

@tool("Verificador de Sintaxe Python")
def verificador_de_sintaxe_python(codigo: str) -> str:
    """
    Verifica a sintaxe de um código Python.
    Retorna 'Sucesso: O código é sintaticamente válido.' se não houver erros,
    ou a mensagem de erro de sintaxe caso contrário.
    """
    try:
        ast.parse(codigo)
        return "Sucesso: O código é sintaticamente válido."
    except SyntaxError as e:
        return f"Erro de Sintaxe: {e}"


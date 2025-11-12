"""
Aplicação Streamlit - Redator Automático com IA
Automatiza a criação de conteúdo otimizado para SEO com imagens e publicação no Google Docs
"""

import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis de ambiente PRIMEIRO
load_dotenv()

# IMPORTANTE: No Streamlit Cloud, usar st.secrets ao invés de os.getenv
# Tentar carregar de st.secrets primeiro, depois de os.getenv como fallback
def get_api_key(key_name):
    """Pega API key de st.secrets (Streamlit Cloud) ou os.getenv (local)"""
    try:
        # Tentar st.secrets primeiro (Streamlit Cloud)
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except:
        pass
    # Fallback para variável de ambiente (local)
    return os.getenv(key_name)

# Configurar environment variables para os agentes
# ISSO DEVE SER FEITO ANTES DE IMPORTAR OS AGENTES!
os.environ["OPENAI_API_KEY"] = get_api_key("OPENAI_API_KEY") or ""
os.environ["TAVILY_API_KEY"] = get_api_key("TAVILY_API_KEY") or ""
os.environ["SUPABASE_URL"] = get_api_key("SUPABASE_URL") or ""
os.environ["SUPABASE_KEY"] = get_api_key("SUPABASE_KEY") or ""

# AGORA SIM podemos importar os módulos customizados
from memoria.gerenciador_memoria import GerenciadorMemoria
from agents.agente_pesquisador import AgentePesquisador
from agents.agente_redator import AgenteRedator
from agents.gerador_imagem import GeradorImagem
from utils.google_docs_handler import GoogleDocsHandler

# Configuração da página
st.set_page_config(
    page_title="Redator Automático IA",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    /* Esconder ícones do GitHub e outros elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Esconder link do GitHub no canto superior direito */
    a[href*="github.com"] {
        display: none !important;
    }
    
    /* Esconder botões de compartilhamento */
    button[title="Fork this app"],
    button[title="View on GitHub"],
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 20px;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'projeto_selecionado' not in st.session_state:
    st.session_state.projeto_selecionado = None
if 'categoria_selecionada' not in st.session_state:
    st.session_state.categoria_selecionada = None
if 'conteudo_gerado' not in st.session_state:
    st.session_state.conteudo_gerado = None
if 'imagem_gerada' not in st.session_state:
    st.session_state.imagem_gerada = None
if 'pesquisa_realizada' not in st.session_state:
    st.session_state.pesquisa_realizada = None

def main():
    # Cabeçalho principal
    st.markdown('<div class="main-header">✍️ Redator Automático com IA</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Inicializar gerenciador de memória
    gerenciador = GerenciadorMemoria()
    
    # Sidebar - Menu lateral
    with st.sidebar:
        st.header("📋 Menu")
        
        # Seção de Projetos
        st.subheader("📁 Projetos")
        projetos_lista = gerenciador.listar_projetos()
        
        if projetos_lista:
            # Criar botões para cada projeto
            for proj in projetos_lista:
                # Destaque visual para projeto selecionado
                is_selected = st.session_state.get('projeto_selecionado') == proj
                button_type = "primary" if is_selected else "secondary"
                
                if st.button(
                    f"{'✓ ' if is_selected else ''}📂 {proj}", 
                    key=f"sidebar_proj_{proj}", 
                    use_container_width=True,
                    type=button_type
                ):
                    st.session_state.projeto_select = proj
                    st.session_state.projeto_selecionado = proj
                    st.session_state.categoria_selecionada = None  # Reset categoria
                    st.rerun()
        else:
            st.info("Nenhum projeto criado ainda")
        
        st.markdown("---")
        
        # Seção de Categorias (só aparece se projeto selecionado)
        if st.session_state.get('projeto_selecionado'):
            projeto_atual = st.session_state.projeto_selecionado
            st.subheader("📂 Categorias")
            st.caption(f"Projeto: {projeto_atual}")
            
            categorias_lista = gerenciador.listar_categorias(projeto_atual)
            
            if categorias_lista:
                # Criar botões para cada categoria
                for cat in categorias_lista:
                    # Destaque visual para categoria selecionada
                    is_selected = st.session_state.get('categoria_selecionada') == cat
                    button_type = "primary" if is_selected else "secondary"
                    
                    if st.button(
                        f"{'✓ ' if is_selected else ''}📄 {cat}", 
                        key=f"sidebar_cat_{cat}", 
                        use_container_width=True,
                        type=button_type
                    ):
                        st.session_state.categoria_select = cat
                        st.session_state.categoria_selecionada = cat
                        st.rerun()
            else:
                st.info("Nenhuma categoria criada ainda")
            
            st.markdown("---")
        
        
        # Status das APIs (colapsável)
        with st.expander("🔧 Status das APIs", expanded=False):
            apis_status = {
                "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
                "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
                "SUPABASE_URL": os.getenv("SUPABASE_URL"),
                "GOOGLE_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            }
            
            for api_name, api_value in apis_status.items():
                if api_value and len(str(api_value)) > 10:
                    # Mostrar primeiros caracteres para debug
                    preview = str(api_value)[:15] + "..." if len(str(api_value)) > 15 else str(api_value)
                    st.success(f"✅ {api_name}")
                    if st.checkbox(f"Ver {api_name[:10]}", key=f"show_{api_name}"):
                        st.code(preview)
                else:
                    st.error(f"❌ {api_name}")
                    if api_name == "OPENAI_API_KEY":
                        st.caption("⚠️ Verifique se a chave foi configurada corretamente em Settings → Secrets")
        
        st.markdown("---")
        
        # Botão para limpar sessão
        if st.button("🔄 Reiniciar Processo", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # ETAPA 1: Seleção do Projeto
    st.markdown('<div class="step-header">📁 Etapa 1: Selecione o Projeto</div>', unsafe_allow_html=True)
    
    projetos = gerenciador.listar_projetos()
    
    # Se há um projeto no session_state, usar como índice padrão
    default_index = 0
    if st.session_state.get('projeto_selecionado') and st.session_state.projeto_selecionado in projetos:
        default_index = projetos.index(st.session_state.projeto_selecionado)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        projeto = st.selectbox(
            "Escolha o projeto:",
            options=projetos,
            index=default_index,
            key="projeto_select"
        )
        
        # Atualizar session_state quando selectbox muda
        if projeto:
            st.session_state.projeto_selecionado = projeto
    
    with col2:
        if st.button("➕ Novo Projeto", use_container_width=True):
            st.session_state.mostrar_novo_projeto = True
    
    if st.session_state.get('mostrar_novo_projeto', False):
        with st.form("novo_projeto_form"):
            nome_projeto = st.text_input("Nome do novo projeto:")
            descricao_projeto = st.text_area("Descrição do projeto:")
            
            if st.form_submit_button("Criar Projeto"):
                if nome_projeto:
                    gerenciador.criar_projeto(nome_projeto, descricao_projeto)
                    st.success(f"✅ Projeto '{nome_projeto}' criado com sucesso!")
                    st.session_state.mostrar_novo_projeto = False
                    st.rerun()
    
    st.markdown("---")
    
    # ETAPA 2: Seleção da Categoria
    if projeto:
        st.markdown('<div class="step-header">📂 Etapa 2: Selecione a Categoria</div>', unsafe_allow_html=True)
        
        categorias = gerenciador.listar_categorias(projeto)
        
        # Se há uma categoria no session_state, usar como índice padrão
        default_cat_index = 0
        if st.session_state.get('categoria_selecionada') and st.session_state.categoria_selecionada in categorias:
            default_cat_index = categorias.index(st.session_state.categoria_selecionada)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            categoria = st.selectbox(
                "Escolha a categoria:",
                options=categorias,
                index=default_cat_index,
                key="categoria_select"
            )
            
            # Atualizar session_state quando selectbox muda
            if categoria:
                st.session_state.categoria_selecionada = categoria
        
        with col2:
            if st.button("➕ Nova Categoria", use_container_width=True):
                st.session_state.mostrar_nova_categoria = True
        
        if st.session_state.get('mostrar_nova_categoria', False):
            with st.form("nova_categoria_form"):
                nome_categoria = st.text_input("Nome da nova categoria:")
                exemplo_conteudo = st.text_area("Exemplo de conteúdo desta categoria:", height=150)
                regras_categoria = st.text_area("Regras e boas práticas desta categoria:", height=150)
                
                if st.form_submit_button("Criar Categoria"):
                    if nome_categoria:
                        gerenciador.adicionar_categoria(projeto, nome_categoria, exemplo_conteudo, regras_categoria)
                        st.success(f"✅ Categoria '{nome_categoria}' criada com sucesso!")
                        st.session_state.mostrar_nova_categoria = False
                        del st.session_state['categoria_select']  # Limpar cache do selectbox
                        st.rerun()
                    else:
                        st.error("Por favor, digite o nome da categoria!")
        
        st.markdown("---")
        
        # ETAPA 3: Palavra-chave e Geração de Conteúdo
        if categoria:
            st.markdown('<div class="step-header">🔍 Etapa 3: Palavra-chave e Geração</div>', unsafe_allow_html=True)
            
            palavra_chave = st.text_input("Digite a palavra-chave para o conteúdo:", key="palavra_chave_input")
            
            # Mostrar exemplos e regras da categoria
            with st.expander("📚 Ver Exemplos e Regras desta Categoria"):
                memoria_categoria = gerenciador.obter_memoria_categoria(projeto, categoria)
                
                if memoria_categoria.get("exemplo"):
                    st.subheader("Exemplo de Conteúdo:")
                    st.info(memoria_categoria["exemplo"])
                
                if memoria_categoria.get("regras"):
                    st.subheader("Regras e Boas Práticas:")
                    st.warning(memoria_categoria["regras"])
            
            st.markdown("---")
            
            # Botão de geração
            if palavra_chave:
                if st.button("🚀 Gerar Conteúdo Completo", type="primary", use_container_width=True):
                    
                    # Criar containers para feedback em tempo real
                    status_container = st.container()
                    
                    with status_container:
                        # PASSO 1: Pesquisa
                        with st.spinner("🔍 Pesquisando informações sobre a palavra-chave..."):
                            pesquisador = AgentePesquisador()
                            pesquisa_resultado = pesquisador.pesquisar(palavra_chave)
                            st.session_state.pesquisa_realizada = pesquisa_resultado
                            st.success("✅ Pesquisa concluída!")
                        
                        # PASSO 2: Geração de Conteúdo
                        with st.spinner("✍️ Gerando conteúdo otimizado para SEO..."):
                            redator = Agente
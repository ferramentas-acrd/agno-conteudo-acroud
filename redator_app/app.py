"""
Aplicação Streamlit - Redator Automático com IA
Automatiza a criação de conteúdo otimizado para SEO com imagens e publicação no Google Docs
"""

import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

# Importar módulos customizados
from memoria.gerenciador_memoria import GerenciadorMemoria
from agents.agente_pesquisador import AgentePesquisador
from agents.agente_redator import AgenteRedator
from agents.gerador_imagem import GeradorImagem
from utils.google_docs_handler import GoogleDocsHandler

# Carregar variáveis de ambiente
load_dotenv()

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
    
    # Sidebar - Configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Verificar APIs configuradas
        st.subheader("📡 Status das APIs")
        
        apis_status = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
            "SUPABASE_URL": os.getenv("SUPABASE_URL"),
            "GOOGLE_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        }
        
        for api_name, api_value in apis_status.items():
            if api_value:
                st.success(f"✅ {api_name}")
            else:
                st.error(f"❌ {api_name}")
        
        st.markdown("---")
        
        # Botão para limpar sessão
        if st.button("🔄 Reiniciar Processo", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Inicializar gerenciador de memória
    gerenciador = GerenciadorMemoria()
    
    # ETAPA 1: Seleção do Projeto
    st.markdown('<div class="step-header">📁 Etapa 1: Selecione o Projeto</div>', unsafe_allow_html=True)
    
    projetos = gerenciador.listar_projetos()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        projeto = st.selectbox(
            "Escolha o projeto:",
            options=projetos,
            key="projeto_select"
        )
    
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
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            categoria = st.selectbox(
                "Escolha a categoria:",
                options=categorias,
                key="categoria_select"
            )
        
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
                            redator = AgenteRedator()
                            memoria_categoria = gerenciador.obter_memoria_categoria(projeto, categoria)
                            
                            conteudo = redator.gerar_conteudo(
                                palavra_chave=palavra_chave,
                                pesquisa_resultado=pesquisa_resultado,
                                exemplo_categoria=memoria_categoria.get("exemplo", ""),
                                regras_categoria=memoria_categoria.get("regras", "")
                            )
                            st.session_state.conteudo_gerado = conteudo
                            st.success("✅ Conteúdo gerado!")
                        
                        # PASSO 3: Geração de Imagem
                        with st.spinner("🎨 Gerando imagem para o conteúdo..."):
                            gerador_img = GeradorImagem()
                            imagem_path = gerador_img.gerar_imagem(
                                titulo=conteudo.get("titulo", palavra_chave),
                                descricao=conteudo.get("resumo", "")
                            )
                            st.session_state.imagem_gerada = imagem_path
                            st.success("✅ Imagem gerada!")
                        
                        # PASSO 4: Salvar no histórico (Supabase se configurado)
                        if gerenciador.usar_supabase:
                            with st.spinner("💾 Salvando no histórico..."):
                                conteudo_completo = {
                                    **conteudo,
                                    "imagem_path": imagem_path
                                }
                                gerenciador.salvar_conteudo_gerado(
                                    projeto, categoria, palavra_chave, conteudo_completo
                                )
                                st.success("✅ Salvo no histórico!")
                        
                        st.balloons()
                        st.success("🎉 Todo o conteúdo foi gerado com sucesso!")
            
            # Mostrar resultado
            if st.session_state.conteudo_gerado:
                st.markdown("---")
                st.markdown('<div class="step-header">📄 Etapa 4: Revisão do Conteúdo</div>', unsafe_allow_html=True)
                
                conteudo = st.session_state.conteudo_gerado
                
                # Mostrar imagem
                if st.session_state.imagem_gerada:
                    st.image(st.session_state.imagem_gerada, use_container_width=True)
                
                # Mostrar conteúdo
                st.markdown(f"### {conteudo.get('titulo', '')}")
                st.markdown(conteudo.get('conteudo_formatado', ''))
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Salvar no Google Docs", type="primary", use_container_width=True):
                        with st.spinner("Salvando no Google Docs..."):
                            try:
                                docs_handler = GoogleDocsHandler()
                                doc_url = docs_handler.criar_documento(
                                    titulo=conteudo.get('titulo', ''),
                                    conteudo=conteudo.get('conteudo_formatado', ''),
                                    imagem_path=st.session_state.imagem_gerada
                                )
                                st.success(f"✅ Documento criado com sucesso!")
                                st.markdown(f"[🔗 Abrir documento no Google Docs]({doc_url})")
                            except Exception as e:
                                st.error(f"Erro ao salvar no Google Docs: {str(e)}")
                
                with col2:
                    # Baixar como HTML
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>{conteudo.get('titulo', '')}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            img {{ max-width: 100%; height: auto; }}
                            h1, h2, h3 {{ color: #333; }}
                        </style>
                    </head>
                    <body>
                        {conteudo.get('conteudo_formatado', '')}
                    </body>
                    </html>
                    """
                    st.download_button(
                        label="💾 Baixar HTML",
                        data=html_content,
                        file_name=f"{palavra_chave.replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                
                with col3:
                    if st.button("🔄 Regenerar Conteúdo", use_container_width=True):
                        st.session_state.conteudo_gerado = None
                        st.session_state.imagem_gerada = None
                        st.rerun()

if __name__ == "__main__":
    main()


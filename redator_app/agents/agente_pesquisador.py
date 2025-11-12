"""
Agente Pesquisador
Realiza pesquisas detalhadas usando Tavily para coletar informações atualizadas
Usa GPT-4 Turbo da OpenAI para análise inteligente
"""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv

load_dotenv()

class AgentePesquisador:
    """Agente especializado em pesquisar informações atualizadas sobre temas"""
    
    def __init__(self):
        """Inicializa o agente pesquisador com GPT-4 Turbo e ferramentas Tavily"""
        self.agent = Agent(
            name="Agente Pesquisador",
            model=OpenAIChat(id="gpt-4-turbo-preview"),
            tools=[TavilyTools()],
            instructions=[
                "Você é um pesquisador especializado em coletar informações detalhadas e atualizadas.",
                "Sempre busque as informações mais recentes e relevantes sobre o tema solicitado.",
                "Cite todas as fontes encontradas.",
                "Organize as informações de forma estruturada.",
                "Foque em dados, estatísticas e fatos verificáveis.",
                "Identifique tendências atuais relacionadas ao tema.",
                "Responda sempre em português."
            ],
            markdown=True,
            add_datetime_to_context=True
        )
    
    def pesquisar(self, palavra_chave: str, profundidade: str = "detalhada") -> dict:
        """
        Realiza uma pesquisa detalhada sobre a palavra-chave
        
        Args:
            palavra_chave: O termo ou tema a ser pesquisado
            profundidade: "rapida" ou "detalhada"
            
        Returns:
            dict com resultados da pesquisa estruturados
        """
        
        prompt_pesquisa = f"""
        Realize uma pesquisa {profundidade} sobre: {palavra_chave}
        
        Por favor, organize a pesquisa nos seguintes tópicos:
        
        1. VISÃO GERAL
        - O que é e para que serve
        - Contexto atual e relevância
        
        2. DADOS E ESTATÍSTICAS
        - Números e fatos importantes
        - Tendências de mercado
        - Dados demográficos relevantes
        
        3. INFORMAÇÕES ATUALIZADAS
        - Novidades recentes (últimos 6 meses)
        - Desenvolvimentos importantes
        - Previsões e perspectivas futuras
        
        4. ASPECTOS PRÁTICOS
        - Como funciona
        - Aplicações práticas
        - Benefícios e desafios
        
        5. FONTES E REFERÊNCIAS
        - Liste todas as fontes consultadas com URLs
        
        Use suas ferramentas de pesquisa para encontrar informações atualizadas e confiáveis.
        """
        
        try:
            # Executar pesquisa usando o agente
            response = self.agent.run(prompt_pesquisa)
            
            resultado = {
                "palavra_chave": palavra_chave,
                "conteudo": response.content if hasattr(response, 'content') else str(response),
                "fontes": self._extrair_fontes(response),
                "timestamp": self._obter_timestamp()
            }
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao pesquisar: {e}")
            return {
                "palavra_chave": palavra_chave,
                "conteudo": f"Erro ao realizar pesquisa: {str(e)}",
                "fontes": [],
                "timestamp": self._obter_timestamp()
            }
    
    def pesquisar_especifico(self, pergunta: str) -> str:
        """
        Faz uma pergunta específica ao agente pesquisador
        
        Args:
            pergunta: Pergunta específica a ser respondida
            
        Returns:
            str com a resposta
        """
        try:
            response = self.agent.run(pergunta)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Erro ao pesquisar: {str(e)}"
    
    def _extrair_fontes(self, response) -> list:
        """Extrai URLs das fontes mencionadas na resposta"""
        fontes = []
        try:
            conteudo = response.content if hasattr(response, 'content') else str(response)
            
            # Procurar por URLs no conteúdo
            import re
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', conteudo)
            
            for url in urls:
                if url not in fontes:
                    fontes.append(url)
        except:
            pass
        
        return fontes
    
    def _obter_timestamp(self) -> str:
        """Retorna o timestamp atual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


"""
Agente Redator
Cria conteúdo otimizado para SEO com formatação profissional
Usa GPT-4 Turbo da OpenAI para máxima qualidade
"""

import os
from agno.agent import Agent
from agno.models.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AgenteRedator:
    """Agente especializado em criar conteúdo otimizado para SEO"""
    
    def __init__(self):
        """Inicializa o agente redator com GPT-4 Turbo"""
        self.agent = Agent(
            name="Agente Redator",
            model=OpenAI(id="gpt-4-turbo-preview"),
            instructions=[
                "Você é um redator profissional especializado em conteúdo otimizado para SEO.",
                "Sempre crie conteúdo original, informativo e envolvente.",
                "Use técnicas de copywriting para manter o leitor interessado.",
                "Aplique boas práticas de SEO: headings estruturados (H1, H2, H3), parágrafos curtos, listas.",
                "Inclua palavras-chave de forma natural no texto.",
                "Escreva em tom profissional mas acessível.",
                "Sempre responda em português do Brasil.",
                "Use formatação Markdown para estruturar o conteúdo.",
                "Inclua meta descriptions e títulos SEO-friendly."
            ],
            markdown=True,
            add_datetime_to_context=True
        )
    
    def gerar_conteudo(
        self,
        palavra_chave: str,
        pesquisa_resultado: dict,
        exemplo_categoria: str = "",
        regras_categoria: str = ""
    ) -> dict:
        """
        Gera conteúdo completo otimizado para SEO
        
        Args:
            palavra_chave: Palavra-chave principal do conteúdo
            pesquisa_resultado: Resultado da pesquisa realizada
            exemplo_categoria: Exemplo de conteúdo da categoria
            regras_categoria: Regras específicas da categoria
            
        Returns:
            dict com o conteúdo gerado e metadados
        """
        
        prompt_redacao = f"""
        Crie um artigo completo e otimizado para SEO sobre: **{palavra_chave}**
        
        ## INFORMAÇÕES DE PESQUISA
        {pesquisa_resultado.get('conteudo', '')}
        
        ## ESTILO E FORMATO ESPERADO
        {exemplo_categoria if exemplo_categoria else 'Use um estilo profissional e informativo'}
        
        ## REGRAS E BOAS PRÁTICAS
        {regras_categoria if regras_categoria else 'Siga boas práticas gerais de redação web'}
        
        ## ESTRUTURA OBRIGATÓRIA DO ARTIGO
        
        1. **Título Principal (H1)**
           - Deve conter a palavra-chave
           - Máximo 60 caracteres
           - Chamativo e claro
        
        2. **Meta Description**
           - Resumo de 150-160 caracteres
           - Incluir palavra-chave
           - Call-to-action quando apropriado
        
        3. **Introdução** (100-150 palavras)
           - Apresente o tema
           - Explique a relevância
           - Gancho para manter o leitor
        
        4. **Desenvolvimento** (mínimo 800 palavras)
           - Use H2 para seções principais
           - Use H3 para subseções
           - Inclua listas (bullets ou numeradas)
           - Parágrafos de 3-4 linhas
           - Use negritos para destacar pontos importantes
           - Inclua dados e estatísticas da pesquisa
           - Cite fontes quando relevante
        
        5. **Conclusão** (80-100 palavras)
           - Resumo dos pontos principais
           - Call-to-action ou reflexão final
        
        ## REQUISITOS DE SEO
        - Densidade de palavra-chave: 1-2%
        - Use sinônimos e variações da palavra-chave
        - URLs internas sugeridas (se aplicável)
        - Alt text para imagens sugerido
        - Responda perguntas comuns sobre o tema
        
        ## FORMATO DE RESPOSTA
        Por favor, formate sua resposta EXATAMENTE assim:
        
        TITULO: [seu título aqui]
        
        META_DESCRIPTION: [sua meta description aqui]
        
        RESUMO: [um resumo de 2-3 frases]
        
        CONTEUDO:
        [todo o conteúdo formatado em Markdown]
        
        PALAVRAS_CHAVE_SECUNDARIAS: [liste 5-7 palavras-chave relacionadas]
        
        ALT_TEXT_IMAGEM: [sugestão de texto alternativo para a imagem principal]
        """
        
        try:
            # Gerar conteúdo
            response = self.agent.run(prompt_redacao)
            conteudo_bruto = response.content if hasattr(response, 'content') else str(response)
            
            # Parsear resposta
            conteudo_parseado = self._parsear_conteudo(conteudo_bruto)
            
            resultado = {
                "palavra_chave": palavra_chave,
                "titulo": conteudo_parseado.get("titulo", palavra_chave.title()),
                "meta_description": conteudo_parseado.get("meta_description", ""),
                "resumo": conteudo_parseado.get("resumo", ""),
                "conteudo_formatado": conteudo_parseado.get("conteudo", conteudo_bruto),
                "palavras_chave_secundarias": conteudo_parseado.get("palavras_chave_secundarias", []),
                "alt_text_imagem": conteudo_parseado.get("alt_text_imagem", palavra_chave),
                "timestamp": self._obter_timestamp(),
                "estatisticas": self._calcular_estatisticas(conteudo_parseado.get("conteudo", conteudo_bruto))
            }
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao gerar conteúdo: {e}")
            return {
                "palavra_chave": palavra_chave,
                "titulo": palavra_chave.title(),
                "meta_description": f"Artigo sobre {palavra_chave}",
                "resumo": f"Conteúdo sobre {palavra_chave}",
                "conteudo_formatado": f"Erro ao gerar conteúdo: {str(e)}",
                "palavras_chave_secundarias": [],
                "alt_text_imagem": palavra_chave,
                "timestamp": self._obter_timestamp(),
                "estatisticas": {}
            }
    
    def revisar_conteudo(self, conteudo: str, foco: str = "seo") -> str:
        """
        Revisa e melhora o conteúdo existente
        
        Args:
            conteudo: Conteúdo a ser revisado
            foco: "seo", "gramatica", ou "clareza"
            
        Returns:
            str com o conteúdo revisado
        """
        prompt_revisao = f"""
        Revise o seguinte conteúdo com foco em {foco}:
        
        {conteudo}
        
        Forneça sugestões de melhoria e uma versão revisada.
        """
        
        try:
            response = self.agent.run(prompt_revisao)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Erro ao revisar: {str(e)}"
    
    def _parsear_conteudo(self, conteudo_bruto: str) -> dict:
        """Parseia o conteúdo bruto em componentes estruturados"""
        resultado = {}
        
        try:
            linhas = conteudo_bruto.split('\n')
            conteudo_principal = []
            capturando_conteudo = False
            
            for linha in linhas:
                if linha.startswith('TITULO:'):
                    resultado['titulo'] = linha.replace('TITULO:', '').strip()
                elif linha.startswith('META_DESCRIPTION:'):
                    resultado['meta_description'] = linha.replace('META_DESCRIPTION:', '').strip()
                elif linha.startswith('RESUMO:'):
                    resultado['resumo'] = linha.replace('RESUMO:', '').strip()
                elif linha.startswith('CONTEUDO:'):
                    capturando_conteudo = True
                    continue
                elif linha.startswith('PALAVRAS_CHAVE_SECUNDARIAS:'):
                    capturando_conteudo = False
                    palavras = linha.replace('PALAVRAS_CHAVE_SECUNDARIAS:', '').strip()
                    resultado['palavras_chave_secundarias'] = [p.strip() for p in palavras.split(',')]
                elif linha.startswith('ALT_TEXT_IMAGEM:'):
                    resultado['alt_text_imagem'] = linha.replace('ALT_TEXT_IMAGEM:', '').strip()
                elif capturando_conteudo:
                    conteudo_principal.append(linha)
            
            if conteudo_principal:
                resultado['conteudo'] = '\n'.join(conteudo_principal)
            else:
                resultado['conteudo'] = conteudo_bruto
                
        except Exception as e:
            print(f"Erro ao parsear conteúdo: {e}")
            resultado['conteudo'] = conteudo_bruto
        
        return resultado
    
    def _calcular_estatisticas(self, conteudo: str) -> dict:
        """Calcula estatísticas do conteúdo"""
        palavras = conteudo.split()
        
        return {
            "total_palavras": len(palavras),
            "total_caracteres": len(conteudo),
            "total_paragrafos": conteudo.count('\n\n') + 1,
            "tempo_leitura_min": round(len(palavras) / 200, 1)  # ~200 palavras/minuto
        }
    
    def _obter_timestamp(self) -> str:
        """Retorna o timestamp atual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


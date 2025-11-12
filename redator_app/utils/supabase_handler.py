"""
Supabase Handler
Gerencia conexão e operações com Supabase para armazenamento persistente
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Tentar importar Supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase não instalado. Use: uv add supabase")

class SupabaseHandler:
    """Gerencia operações com Supabase"""
    
    def __init__(self):
        """Inicializa conexão com Supabase"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.client: Optional[Client] = None
        self.connected = False
        
        if not SUPABASE_AVAILABLE:
            print("⚠️ Supabase não disponível. Usando armazenamento local.")
            return
        
        if self.supabase_url and self.supabase_key:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                self.connected = True
                print("✅ Conectado ao Supabase!")
            except Exception as e:
                print(f"❌ Erro ao conectar Supabase: {e}")
                self.connected = False
        else:
            print("⚠️ SUPABASE_URL ou SUPABASE_KEY não configurados")
    
    # ==================== PROJETOS ====================
    
    def criar_projeto(self, nome: str, descricao: str = "") -> bool:
        """Cria um novo projeto no Supabase"""
        if not self.connected:
            return False
        
        try:
            data = {
                "nome": nome,
                "descricao": descricao,
                "criado_em": datetime.now().isoformat()
            }
            
            result = self.client.table("projetos").insert(data).execute()
            return True
        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            return False
    
    def listar_projetos(self) -> List[str]:
        """Lista todos os projetos"""
        if not self.connected:
            return []
        
        try:
            result = self.client.table("projetos").select("nome").execute()
            return [p["nome"] for p in result.data]
        except Exception as e:
            print(f"Erro ao listar projetos: {e}")
            return []
    
    def obter_projeto(self, nome: str) -> Optional[Dict]:
        """Obtém detalhes de um projeto"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table("projetos").select("*").eq("nome", nome).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Erro ao obter projeto: {e}")
            return None
    
    # ==================== CATEGORIAS ====================
    
    def adicionar_categoria(self, projeto_nome: str, categoria_nome: str, 
                           exemplo: str = "", regras: str = "") -> bool:
        """Adiciona categoria a um projeto"""
        if not self.connected:
            return False
        
        try:
            # Buscar ID do projeto
            projeto = self.client.table("projetos").select("id").eq("nome", projeto_nome).execute()
            
            if not projeto.data:
                return False
            
            projeto_id = projeto.data[0]["id"]
            
            data = {
                "projeto_id": projeto_id,
                "nome": categoria_nome,
                "exemplo": exemplo,
                "regras": regras,
                "criado_em": datetime.now().isoformat()
            }
            
            self.client.table("categorias").insert(data).execute()
            return True
        except Exception as e:
            print(f"Erro ao adicionar categoria: {e}")
            return False
    
    def listar_categorias(self, projeto_nome: str) -> List[str]:
        """Lista categorias de um projeto"""
        if not self.connected:
            return []
        
        try:
            # Buscar projeto
            projeto = self.client.table("projetos").select("id").eq("nome", projeto_nome).execute()
            
            if not projeto.data:
                return []
            
            projeto_id = projeto.data[0]["id"]
            
            # Buscar categorias
            result = self.client.table("categorias").select("nome").eq("projeto_id", projeto_id).execute()
            
            return [c["nome"] for c in result.data]
        except Exception as e:
            print(f"Erro ao listar categorias: {e}")
            return []
    
    def obter_categoria(self, projeto_nome: str, categoria_nome: str) -> Optional[Dict]:
        """Obtém detalhes de uma categoria"""
        if not self.connected:
            return None
        
        try:
            # Buscar projeto
            projeto = self.client.table("projetos").select("id").eq("nome", projeto_nome).execute()
            
            if not projeto.data:
                return None
            
            projeto_id = projeto.data[0]["id"]
            
            # Buscar categoria
            result = self.client.table("categorias").select("*").eq("projeto_id", projeto_id).eq("nome", categoria_nome).execute()
            
            if result.data:
                return {
                    "exemplo": result.data[0].get("exemplo", ""),
                    "regras": result.data[0].get("regras", "")
                }
            return None
        except Exception as e:
            print(f"Erro ao obter categoria: {e}")
            return None
    
    # ==================== CONTEÚDOS GERADOS ====================
    
    def salvar_conteudo(self, projeto_nome: str, categoria_nome: str, 
                       palavra_chave: str, conteudo_data: Dict) -> bool:
        """Salva conteúdo gerado no histórico"""
        if not self.connected:
            return False
        
        try:
            # Buscar projeto
            projeto = self.client.table("projetos").select("id").eq("nome", projeto_nome).execute()
            
            if not projeto.data:
                return False
            
            projeto_id = projeto.data[0]["id"]
            
            # Buscar categoria
            categoria = self.client.table("categorias").select("id").eq("projeto_id", projeto_id).eq("nome", categoria_nome).execute()
            
            categoria_id = categoria.data[0]["id"] if categoria.data else None
            
            data = {
                "projeto_id": projeto_id,
                "categoria_id": categoria_id,
                "palavra_chave": palavra_chave,
                "titulo": conteudo_data.get("titulo", ""),
                "meta_description": conteudo_data.get("meta_description", ""),
                "conteudo": conteudo_data.get("conteudo_formatado", ""),
                "palavras_chave_secundarias": conteudo_data.get("palavras_chave_secundarias", []),
                "imagem_path": conteudo_data.get("imagem_path", ""),
                "estatisticas": conteudo_data.get("estatisticas", {}),
                "criado_em": datetime.now().isoformat()
            }
            
            self.client.table("conteudos_gerados").insert(data).execute()
            return True
        except Exception as e:
            print(f"Erro ao salvar conteúdo: {e}")
            return False
    
    def listar_conteudos(self, projeto_nome: str = None, categoria_nome: str = None, 
                        limite: int = 50) -> List[Dict]:
        """Lista conteúdos gerados"""
        if not self.connected:
            return []
        
        try:
            query = self.client.table("conteudos_gerados").select("*")
            
            if projeto_nome:
                projeto = self.client.table("projetos").select("id").eq("nome", projeto_nome).execute()
                if projeto.data:
                    query = query.eq("projeto_id", projeto.data[0]["id"])
            
            query = query.order("criado_em", desc=True).limit(limite)
            
            result = query.execute()
            return result.data
        except Exception as e:
            print(f"Erro ao listar conteúdos: {e}")
            return []
    
    def obter_conteudo(self, conteudo_id: int) -> Optional[Dict]:
        """Obtém um conteúdo específico"""
        if not self.connected:
            return None
        
        try:
            result = self.client.table("conteudos_gerados").select("*").eq("id", conteudo_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Erro ao obter conteúdo: {e}")
            return None
    
    # ==================== ESTATÍSTICAS ====================
    
    def obter_estatisticas_projeto(self, projeto_nome: str) -> Dict:
        """Obtém estatísticas de um projeto"""
        if not self.connected:
            return {}
        
        try:
            # Buscar projeto
            projeto = self.client.table("projetos").select("id").eq("nome", projeto_nome).execute()
            
            if not projeto.data:
                return {}
            
            projeto_id = projeto.data[0]["id"]
            
            # Contar conteúdos
            conteudos = self.client.table("conteudos_gerados").select("*").eq("projeto_id", projeto_id).execute()
            
            total_conteudos = len(conteudos.data)
            
            # Calcular estatísticas
            total_palavras = sum([c.get("estatisticas", {}).get("total_palavras", 0) for c in conteudos.data])
            
            return {
                "total_conteudos": total_conteudos,
                "total_palavras": total_palavras,
                "ultimo_conteudo": conteudos.data[0].get("criado_em") if conteudos.data else None
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}


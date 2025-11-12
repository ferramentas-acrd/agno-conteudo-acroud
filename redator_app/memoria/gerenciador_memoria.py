"""
Gerenciador de Memória
Gerencia projetos, categorias, exemplos e regras de conteúdo
Suporta Supabase (nuvem) com fallback para JSON (local)
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

# Tentar importar Supabase
try:
    from utils.supabase_handler import SupabaseHandler
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class GerenciadorMemoria:
    """Gerencia a memória de projetos, categorias e regras de conteúdo"""
    
    def __init__(self, memoria_dir: str = "memoria/dados"):
        self.memoria_dir = Path(__file__).parent / "dados"
        self.memoria_dir.mkdir(parents=True, exist_ok=True)
        self.projetos_file = self.memoria_dir / "projetos.json"
        
        # Tentar conectar ao Supabase
        self.supabase = None
        self.usar_supabase = False
        
        if SUPABASE_AVAILABLE:
            try:
                self.supabase = SupabaseHandler()
                self.usar_supabase = self.supabase.connected
                if self.usar_supabase:
                    print("✅ Usando Supabase para armazenamento")
                else:
                    print("📝 Usando armazenamento local (JSON)")
            except Exception as e:
                print(f"⚠️ Erro ao conectar Supabase: {e}")
                print("📝 Usando armazenamento local (JSON)")
        else:
            print("📝 Usando armazenamento local (JSON)")
        
        self._inicializar_memoria()
    
    def _inicializar_memoria(self):
        """Inicializa o arquivo de memória se não existir"""
        if not self.projetos_file.exists():
            dados_iniciais = {
                "projetos": {}
            }
            self._salvar_dados(dados_iniciais)
    
    def _carregar_dados(self) -> Dict:
        """Carrega os dados da memória"""
        try:
            with open(self.projetos_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return {"projetos": {}}
    
    def _salvar_dados(self, dados: Dict):
        """Salva os dados na memória"""
        try:
            with open(self.projetos_file, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def criar_projeto(self, nome: str, descricao: str = ""):
        """Cria um novo projeto"""
        # Tentar Supabase primeiro
        if self.usar_supabase and self.supabase:
            sucesso = self.supabase.criar_projeto(nome, descricao)
            if sucesso:
                # Também salvar localmente para sincronização
                dados = self._carregar_dados()
                if nome not in dados["projetos"]:
                    dados["projetos"][nome] = {
                        "descricao": descricao,
                        "categorias": {}
                    }
                    self._salvar_dados(dados)
                return True
        
        # Fallback para JSON local
        dados = self._carregar_dados()
        
        if nome not in dados["projetos"]:
            dados["projetos"][nome] = {
                "descricao": descricao,
                "categorias": {}
            }
            self._salvar_dados(dados)
            return True
        return False
    
    def listar_projetos(self) -> List[str]:
        """Lista todos os projetos"""
        # Tentar Supabase primeiro
        if self.usar_supabase and self.supabase:
            projetos = self.supabase.listar_projetos()
            if projetos:
                return projetos
        
        # Fallback para JSON local
        dados = self._carregar_dados()
        return list(dados["projetos"].keys())
    
    def adicionar_categoria(
        self, 
        projeto: str, 
        categoria: str, 
        exemplo: str = "", 
        regras: str = ""
    ):
        """Adiciona uma categoria a um projeto"""
        # Tentar Supabase primeiro
        if self.usar_supabase and self.supabase:
            sucesso = self.supabase.adicionar_categoria(projeto, categoria, exemplo, regras)
            if sucesso:
                # Também salvar localmente
                dados = self._carregar_dados()
                if projeto in dados["projetos"]:
                    dados["projetos"][projeto]["categorias"][categoria] = {
                        "exemplo": exemplo,
                        "regras": regras
                    }
                    self._salvar_dados(dados)
                return True
        
        # Fallback para JSON local
        dados = self._carregar_dados()
        
        if projeto in dados["projetos"]:
            dados["projetos"][projeto]["categorias"][categoria] = {
                "exemplo": exemplo,
                "regras": regras
            }
            self._salvar_dados(dados)
            return True
        return False
    
    def listar_categorias(self, projeto: str) -> List[str]:
        """Lista todas as categorias de um projeto"""
        # Tentar Supabase primeiro
        if self.usar_supabase and self.supabase:
            categorias = self.supabase.listar_categorias(projeto)
            if categorias:
                return categorias
        
        # Fallback para JSON local
        dados = self._carregar_dados()
        
        if projeto in dados["projetos"]:
            return list(dados["projetos"][projeto]["categorias"].keys())
        return []
    
    def obter_memoria_categoria(self, projeto: str, categoria: str) -> Dict:
        """Obtém a memória completa de uma categoria"""
        # Tentar Supabase primeiro
        if self.usar_supabase and self.supabase:
            memoria = self.supabase.obter_categoria(projeto, categoria)
            if memoria:
                return memoria
        
        # Fallback para JSON local
        dados = self._carregar_dados()
        
        if projeto in dados["projetos"]:
            if categoria in dados["projetos"][projeto]["categorias"]:
                return dados["projetos"][projeto]["categorias"][categoria]
        
        return {"exemplo": "", "regras": ""}
    
    def atualizar_categoria(
        self, 
        projeto: str, 
        categoria: str, 
        exemplo: Optional[str] = None, 
        regras: Optional[str] = None
    ):
        """Atualiza a memória de uma categoria"""
        dados = self._carregar_dados()
        
        if projeto in dados["projetos"] and categoria in dados["projetos"][projeto]["categorias"]:
            if exemplo is not None:
                dados["projetos"][projeto]["categorias"][categoria]["exemplo"] = exemplo
            if regras is not None:
                dados["projetos"][projeto]["categorias"][categoria]["regras"] = regras
            
            self._salvar_dados(dados)
            return True
        return False
    
    def deletar_categoria(self, projeto: str, categoria: str):
        """Deleta uma categoria de um projeto"""
        dados = self._carregar_dados()
        
        if projeto in dados["projetos"]:
            if categoria in dados["projetos"][projeto]["categorias"]:
                del dados["projetos"][projeto]["categorias"][categoria]
                self._salvar_dados(dados)
                return True
        return False
    
    def deletar_projeto(self, projeto: str):
        """Deleta um projeto completo"""
        dados = self._carregar_dados()
        
        if projeto in dados["projetos"]:
            del dados["projetos"][projeto]
            self._salvar_dados(dados)
            return True
        return False
    
    def salvar_conteudo_gerado(self, projeto: str, categoria: str, 
                               palavra_chave: str, conteudo_data: Dict) -> bool:
        """Salva conteúdo gerado no histórico (Supabase ou local)"""
        if self.usar_supabase and self.supabase:
            return self.supabase.salvar_conteudo(projeto, categoria, palavra_chave, conteudo_data)
        
        # Se não usar Supabase, apenas retorna True (JSON local não salva histórico por padrão)
        return True


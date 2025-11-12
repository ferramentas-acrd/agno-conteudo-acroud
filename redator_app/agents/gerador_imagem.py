"""
Gerador de Imagem
Gera imagens personalizadas para os artigos (1200x630px)
Suporta: DALL-E 3 (OpenAI), Replicate (Flux/Stable Diffusion), ou fallback com texto
"""

import os
import requests
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

class GeradorImagem:
    """Gera imagens para os artigos usando IA"""
    
    def __init__(self, output_dir: str = "redator_app/imagens_geradas"):
        """Inicializa o gerador de imagens"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.largura = 1200
        self.altura = 630
        
        # Configurar APIs disponíveis
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.replicate_key = os.getenv("REPLICATE_API_TOKEN")
    
    def gerar_imagem(self, titulo: str, descricao: str = "") -> str:
        """
        Gera uma imagem para o artigo
        
        Prioridade de APIs:
        1. DALL-E 3 (OpenAI) - Melhor qualidade
        2. Replicate (Flux/Stable Diffusion) - Bom custo-benefício
        3. Fallback: Imagem com texto estilizado
        
        Args:
            titulo: Título do artigo
            descricao: Descrição ou resumo
            
        Returns:
            str: caminho da imagem gerada
        """
        
        print(f"🎨 Gerando imagem para: {titulo}")
        
        # Tentar DALL-E 3 primeiro
        if self.openai_key:
            try:
                print("→ Usando DALL-E 3 (OpenAI)...")
                return self._gerar_com_dalle3(titulo, descricao)
            except Exception as e:
                print(f"⚠️ DALL-E 3 falhou: {e}")
        
        # Tentar Replicate
        if self.replicate_key:
            try:
                print("→ Usando Replicate (Flux)...")
                return self._gerar_com_replicate(titulo, descricao)
            except Exception as e:
                print(f"⚠️ Replicate falhou: {e}")
        
        # Fallback: imagem com texto
        print("→ Usando gerador de texto estilizado...")
        return self._gerar_imagem_texto(titulo, descricao)
    
    def _gerar_com_dalle3(self, titulo: str, descricao: str) -> str:
        """
        Gera imagem usando DALL-E 3 da OpenAI
        
        Vantagens:
        - Melhor qualidade
        - Compreende texto em português
        - Gera imagens realistas e artísticas
        
        Custo: ~$0.04 por imagem (1024x1024) ou $0.08 (1792x1024)
        """
        
        # Criar prompt otimizado
        prompt = self._criar_prompt_dalle(titulo, descricao)
        
        url = "https://api.openai.com/v1/images/generations"
        
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1792x1024",  # Formato landscape, próximo de 1200x630
            "quality": "standard",  # "standard" ou "hd"
            "style": "natural"  # "natural" ou "vivid"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            image_url = data['data'][0]['url']
            
            # Baixar e redimensionar para 1200x630
            return self._baixar_e_redimensionar(image_url, titulo)
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    def _gerar_com_replicate(self, titulo: str, descricao: str) -> str:
        """
        Gera imagem usando Replicate (Flux ou Stable Diffusion)
        
        Vantagens:
        - Mais barato (~$0.003 por imagem)
        - Vários modelos disponíveis
        - Boa qualidade
        
        Modelos recomendados:
        - black-forest-labs/flux-schnell (rápido e gratuito!)
        - black-forest-labs/flux-pro (melhor qualidade)
        - stability-ai/sdxl (Stable Diffusion XL)
        """
        
        # Criar prompt otimizado
        prompt = self._criar_prompt_replicate(titulo, descricao)
        
        url = "https://api.replicate.com/v1/predictions"
        
        headers = {
            "Authorization": f"Token {self.replicate_key}",
            "Content-Type": "application/json"
        }
        
        # Usando Flux Schnell (GRATUITO e rápido!)
        payload = {
            "version": "f2ab8a5569479b796f8986afbd7f96745c4d0c81be6d7dddeb8f71a34e5f3e3c",  # flux-schnell
            "input": {
                "prompt": prompt,
                "width": 1216,  # Múltiplo de 32 próximo de 1200
                "height": 640,  # Múltiplo de 32 próximo de 630
                "num_outputs": 1,
                "num_inference_steps": 4,  # Schnell usa poucos steps
                "guidance_scale": 0,  # Schnell não usa guidance
                "output_format": "png"
            }
        }
        
        # Criar predição
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 201:
            prediction = response.json()
            prediction_url = prediction['urls']['get']
            
            # Aguardar conclusão (polling)
            image_url = self._aguardar_replicate(prediction_url, headers)
            
            # Baixar e ajustar tamanho
            return self._baixar_e_redimensionar(image_url, titulo)
        else:
            raise Exception(f"Replicate API error: {response.status_code} - {response.text}")
    
    def _aguardar_replicate(self, prediction_url: str, headers: dict, max_tentativas: int = 60) -> str:
        """Aguarda a conclusão da geração no Replicate"""
        import time
        
        for i in range(max_tentativas):
            response = requests.get(prediction_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                prediction = response.json()
                status = prediction['status']
                
                if status == 'succeeded':
                    return prediction['output'][0]  # URL da imagem
                elif status == 'failed':
                    raise Exception(f"Replicate generation failed: {prediction.get('error')}")
                
                # Ainda processando, aguardar
                time.sleep(1)
            else:
                raise Exception(f"Error checking status: {response.status_code}")
        
        raise Exception("Timeout waiting for image generation")
    
    def _criar_prompt_dalle(self, titulo: str, descricao: str) -> str:
        """Cria prompt otimizado para DALL-E 3"""
        prompt = f"""Create a professional featured image for a blog article.

Article Title: {titulo}

Style Requirements:
- Modern and clean design
- Professional and eye-catching
- Suitable for social media (landscape orientation)
- High quality and detailed
- Appropriate for the article topic

Context: {descricao if descricao else 'General article about ' + titulo}

Make it visually appealing and relevant to the article subject."""
        
        return prompt
    
    def _criar_prompt_replicate(self, titulo: str, descricao: str) -> str:
        """Cria prompt otimizado para Replicate (Flux/Stable Diffusion)"""
        prompt = f"""Professional featured image for article: {titulo}. 
Modern, clean design, high quality, detailed, professional photography style, 
trending on artstation, 8k resolution, vibrant colors, suitable for blog header.
{descricao if descricao else ''}"""
        
        return prompt
    
    def _baixar_e_redimensionar(self, url: str, titulo: str) -> str:
        """Baixa imagem de URL e redimensiona para 1200x630"""
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Abrir imagem
            img = Image.open(BytesIO(response.content))
            
            # Redimensionar mantendo proporção e cropando se necessário
            img_redimensionada = self._crop_to_size(img, self.largura, self.altura)
            
            # Salvar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self._sanitizar_nome(titulo)}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            img_redimensionada.save(filepath, 'PNG', quality=95)
            
            return str(filepath)
        
        raise Exception(f"Error downloading image: {response.status_code}")
    
    def _crop_to_size(self, img: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """Redimensiona e cropa imagem para tamanho exato mantendo proporção"""
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Imagem mais larga - ajustar pela altura
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # Imagem mais alta - ajustar pela largura
            new_width = target_width
            new_height = int(new_width / img_ratio)
        
        # Redimensionar
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Crop central para tamanho exato
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        return img_resized.crop((left, top, right, bottom))
    
    def _gerar_com_ai(self, titulo: str, descricao: str, api_key: str) -> str:
        """
        Gera imagem usando API de IA (RapidAPI + DALL-E ou similar)
        
        Para configurar:
        1. Acesse https://rapidapi.com/
        2. Procure por "Text to Image" ou "DALL-E"
        3. Subscribe em um plano (tem opções gratuitas)
        4. Copie sua API Key
        5. Adicione no .env: RAPIDAPI_KEY=sua_chave
        6. Adicione também: RAPIDAPI_HOST=nome_do_host
        """
        
        prompt = f"Professional featured image for article about: {titulo}. Style: modern, clean, professional. Size: 1200x630px"
        
        # Exemplo com RapidAPI (ajustar conforme API escolhida)
        rapidapi_host = os.getenv("RAPIDAPI_HOST", "ai-image-generator3.p.rapidapi.com")
        
        url = f"https://{rapidapi_host}/generate"
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": rapidapi_host,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "width": self.largura,
            "height": self.altura
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Baixar imagem (ajustar conforme formato da API)
            if 'url' in data or 'image_url' in data:
                image_url = data.get('url') or data.get('image_url')
                return self._baixar_imagem(image_url, titulo)
        
        raise Exception(f"API retornou erro: {response.status_code}")
    
    def _baixar_imagem(self, url: str, titulo: str) -> str:
        """Baixa imagem de uma URL"""
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self._sanitizar_nome(titulo)}_{timestamp}.png"
            filepath = self.output_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return str(filepath)
        
        raise Exception(f"Erro ao baixar imagem: {response.status_code}")
    
    def _gerar_imagem_texto(self, titulo: str, descricao: str = "") -> str:
        """
        Gera uma imagem com texto estilizado (fallback)
        Cria uma imagem profissional com gradiente e texto
        """
        
        # Criar imagem com gradiente
        img = Image.new('RGB', (self.largura, self.altura), color='white')
        draw = ImageDraw.Draw(img)
        
        # Criar gradiente
        for i in range(self.altura):
            # Gradiente azul profissional
            r = int(25 + (i / self.altura) * 30)
            g = int(100 + (i / self.altura) * 50)
            b = int(200 + (i / self.altura) * 55)
            draw.rectangle([(0, i), (self.largura, i+1)], fill=(r, g, b))
        
        # Tentar carregar fonte (ou usar padrão)
        try:
            # Usar fonte do sistema
            fonte_titulo = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
            fonte_desc = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except:
            fonte_titulo = ImageFont.load_default()
            fonte_desc = ImageFont.load_default()
        
        # Quebrar título em linhas
        palavras_titulo = titulo.split()
        linhas_titulo = []
        linha_atual = []
        
        for palavra in palavras_titulo:
            linha_teste = ' '.join(linha_atual + [palavra])
            bbox = draw.textbbox((0, 0), linha_teste, font=fonte_titulo)
            if bbox[2] - bbox[0] < self.largura - 100:
                linha_atual.append(palavra)
            else:
                if linha_atual:
                    linhas_titulo.append(' '.join(linha_atual))
                linha_atual = [palavra]
        
        if linha_atual:
            linhas_titulo.append(' '.join(linha_atual))
        
        # Limitar a 3 linhas
        linhas_titulo = linhas_titulo[:3]
        
        # Calcular posição vertical para centralizar
        altura_total_texto = len(linhas_titulo) * 80
        y_inicial = (self.altura - altura_total_texto) // 2
        
        # Desenhar título
        y_pos = y_inicial
        for linha in linhas_titulo:
            bbox = draw.textbbox((0, 0), linha, font=fonte_titulo)
            largura_texto = bbox[2] - bbox[0]
            x_pos = (self.largura - largura_texto) // 2
            
            # Sombra do texto
            draw.text((x_pos + 3, y_pos + 3), linha, font=fonte_titulo, fill=(0, 0, 0, 128))
            # Texto principal
            draw.text((x_pos, y_pos), linha, font=fonte_titulo, fill='white')
            y_pos += 80
        
        # Adicionar borda decorativa
        draw.rectangle([(50, 50), (self.largura-50, self.altura-50)], outline='white', width=5)
        
        # Salvar imagem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self._sanitizar_nome(titulo)}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        img.save(filepath, 'PNG', quality=95)
        
        return str(filepath)
    
    def redimensionar_imagem(self, caminho_imagem: str) -> str:
        """Redimensiona uma imagem existente para 1200x630"""
        img = Image.open(caminho_imagem)
        img_redimensionada = img.resize((self.largura, self.altura), Image.Resampling.LANCZOS)
        
        # Salvar com novo nome
        path = Path(caminho_imagem)
        novo_caminho = path.parent / f"{path.stem}_1200x630{path.suffix}"
        img_redimensionada.save(novo_caminho)
        
        return str(novo_caminho)
    
    def _sanitizar_nome(self, nome: str) -> str:
        """Remove caracteres especiais do nome do arquivo"""
        import re
        nome_limpo = re.sub(r'[^\w\s-]', '', nome)
        nome_limpo = re.sub(r'[-\s]+', '_', nome_limpo)
        return nome_limpo[:50]  # Limitar tamanho


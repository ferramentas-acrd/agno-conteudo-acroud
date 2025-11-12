# ⚡ Quick Start - Redator Automático

Comece a usar em 5 minutos!

## 🚀 Instalação Rápida

### Opção 1: Script Automático (Recomendado)

```bash
cd redator_app
./install.sh
```

### Opção 2: Manual

```bash
cd redator_app

# Instalar dependências
pip install streamlit agno google-auth google-auth-oauthlib google-api-python-client pillow

# Criar diretórios
mkdir -p config memoria/dados imagens_geradas
```

## ⚙️ Configuração Mínima (2 minutos)

### 1. Verificar .env

Já está configurado! ✅

```bash
cd /Users/caiobessa/Desktop/Agno\ Acroud
cat .env
```

Deve ter:
```
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...
```

### 2. Google APIs (Opcional - pode fazer depois)

Se quiser salvar no Google Docs agora:
- Siga: [GOOGLE_API_SETUP.md](./GOOGLE_API_SETUP.md) (10 min)

Se não, pode usar sem Google Docs:
- Baixe como HTML
- Configure depois quando precisar

## 🎮 Usar Agora!

```bash
cd /Users/caiobessa/Desktop/Agno\ Acroud/redator_app
streamlit run app.py
```

Abrirá em: http://localhost:8501

## 📝 Primeiro Uso

### 1. Criar Projeto

- Nome: "Meu Blog"
- Descrição: "Artigos sobre tecnologia"

### 2. Criar Categoria

- Nome: "Tutorial"
- Exemplo: (cole um exemplo de tutorial seu)
- Regras: "Tom didático, mínimo 800 palavras"

### 3. Gerar Conteúdo

- Palavra-chave: "como usar Python"
- Clique: **"Gerar Conteúdo Completo"**
- Aguarde 30-60 segundos
- Pronto! 🎉

## 🎨 Recursos Disponíveis

### ✅ Funciona Sem Google APIs

- ✅ Pesquisa na internet (Tavily)
- ✅ Redação com IA (Groq)
- ✅ Geração de imagens com texto
- ✅ Download como HTML
- ❌ Salvar no Google Docs (precisa configurar)

### ✅ Com Google APIs Configuradas

Tudo acima +
- ✅ Salvar direto no Google Docs
- ✅ Formatação automática
- ✅ Imagem inserida no documento

## 💡 Dicas

### Melhores Resultados

1. **Exemplos Detalhados**: Quanto melhor o exemplo da categoria, melhor o resultado
2. **Regras Claras**: Defina tom, estrutura e requisitos específicos
3. **Palavras-chave Específicas**: "tutorial Python para iniciantes" > "Python"

### Economia de Tempo

- Crie várias categorias de uma vez
- Use a memória para treinar o estilo
- Salve bons resultados como exemplos

### Solução Rápida de Problemas

**Erro de API?**
- Verifique .env no diretório pai
- Certifique-se que as keys começam com `gsk_` e `tvly-`

**Conteúdo não ficou bom?**
- Clique em "Regenerar"
- Melhore o exemplo da categoria
- Adicione mais detalhes nas regras

**Imagem não aparece?**
- Normal! Ela está sendo gerada
- Aguarde até ver "Imagem gerada!"

## 🎯 Casos de Uso

### Blog Pessoal
- Categorias: Tutorial, Review, Opinião
- Gere 3-5 artigos por semana
- Publique direto no WordPress (futuro)

### E-commerce
- Categorias: Descrição de Produto, Guia de Compra
- SEO otimizado automaticamente
- Imagens profissionais

### Agência de Marketing
- Múltiplos projetos (um por cliente)
- Categorias customizadas por cliente
- Escala produção de conteúdo

## 📞 Precisa de Ajuda?

### Problemas Comuns

**"Module not found"**
```bash
cd /Users/caiobessa/Desktop/Agno\ Acroud
uv add streamlit agno
```

**"API Key not set"**
```bash
cd /Users/caiobessa/Desktop/Agno\ Acroud
cat .env  # Verificar se tem as keys
```

**"Port already in use"**
```bash
streamlit run app.py --server.port 8502
```

### Documentação Completa

- [README.md](./README.md) - Documentação completa
- [GOOGLE_API_SETUP.md](./GOOGLE_API_SETUP.md) - Guia de APIs do Google

---

## ✅ Checklist

- [ ] Dependências instaladas
- [ ] .env configurado (GROQ + TAVILY)
- [ ] App rodando (streamlit run app.py)
- [ ] Projeto criado
- [ ] Categoria criada
- [ ] Primeiro conteúdo gerado!

**Pronto! Agora é só criar conteúdo! 🚀**


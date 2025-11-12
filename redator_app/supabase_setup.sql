-- ================================================
-- SETUP SUPABASE - REDATOR AUTOMÁTICO COM IA
-- ================================================
-- Execute este script no SQL Editor do Supabase
-- para criar as tabelas necessárias

-- ================================================
-- 1. TABELA DE PROJETOS
-- ================================================

CREATE TABLE IF NOT EXISTS projetos (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para busca rápida por nome
CREATE INDEX IF NOT EXISTS idx_projetos_nome ON projetos(nome);

-- ================================================
-- 2. TABELA DE CATEGORIAS
-- ================================================

CREATE TABLE IF NOT EXISTS categorias (
    id BIGSERIAL PRIMARY KEY,
    projeto_id BIGINT NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    nome TEXT NOT NULL,
    exemplo TEXT,
    regras TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(projeto_id, nome)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_categorias_projeto ON categorias(projeto_id);
CREATE INDEX IF NOT EXISTS idx_categorias_nome ON categorias(nome);

-- ================================================
-- 3. TABELA DE CONTEÚDOS GERADOS
-- ================================================

CREATE TABLE IF NOT EXISTS conteudos_gerados (
    id BIGSERIAL PRIMARY KEY,
    projeto_id BIGINT NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    categoria_id BIGINT REFERENCES categorias(id) ON DELETE SET NULL,
    palavra_chave TEXT NOT NULL,
    titulo TEXT NOT NULL,
    meta_description TEXT,
    conteudo TEXT NOT NULL,
    palavras_chave_secundarias TEXT[],
    imagem_path TEXT,
    estatisticas JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para busca e performance
CREATE INDEX IF NOT EXISTS idx_conteudos_projeto ON conteudos_gerados(projeto_id);
CREATE INDEX IF NOT EXISTS idx_conteudos_categoria ON conteudos_gerados(categoria_id);
CREATE INDEX IF NOT EXISTS idx_conteudos_palavra_chave ON conteudos_gerados(palavra_chave);
CREATE INDEX IF NOT EXISTS idx_conteudos_criado_em ON conteudos_gerados(criado_em DESC);

-- Índice para busca full-text no conteúdo
CREATE INDEX IF NOT EXISTS idx_conteudos_busca ON conteudos_gerados USING gin(to_tsvector('portuguese', conteudo));

-- ================================================
-- 4. TABELA DE IMAGENS GERADAS
-- ================================================

CREATE TABLE IF NOT EXISTS imagens_geradas (
    id BIGSERIAL PRIMARY KEY,
    conteudo_id BIGINT REFERENCES conteudos_gerados(id) ON DELETE CASCADE,
    nome_arquivo TEXT NOT NULL,
    url_publica TEXT,
    api_utilizada TEXT,
    prompt_usado TEXT,
    largura INT DEFAULT 1200,
    altura INT DEFAULT 630,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_imagens_conteudo ON imagens_geradas(conteudo_id);

-- ================================================
-- 5. FUNÇÕES AUXILIARES
-- ================================================

-- Função para atualizar timestamp automaticamente
CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para atualização automática
CREATE TRIGGER trigger_atualizar_projeto
BEFORE UPDATE ON projetos
FOR EACH ROW
EXECUTE FUNCTION atualizar_timestamp();

CREATE TRIGGER trigger_atualizar_categoria
BEFORE UPDATE ON categorias
FOR EACH ROW
EXECUTE FUNCTION atualizar_timestamp();

-- ================================================
-- 6. VIEWS ÚTEIS
-- ================================================

-- View com estatísticas por projeto
CREATE OR REPLACE VIEW estatisticas_projetos AS
SELECT 
    p.id,
    p.nome,
    p.descricao,
    COUNT(DISTINCT c.id) as total_categorias,
    COUNT(DISTINCT cg.id) as total_conteudos,
    SUM((cg.estatisticas->>'total_palavras')::int) as total_palavras,
    MAX(cg.criado_em) as ultimo_conteudo
FROM projetos p
LEFT JOIN categorias c ON p.id = c.projeto_id
LEFT JOIN conteudos_gerados cg ON p.id = cg.projeto_id
GROUP BY p.id, p.nome, p.descricao;

-- View com últimos conteúdos gerados
CREATE OR REPLACE VIEW ultimos_conteudos AS
SELECT 
    cg.id,
    p.nome as projeto,
    cat.nome as categoria,
    cg.palavra_chave,
    cg.titulo,
    (cg.estatisticas->>'total_palavras')::int as total_palavras,
    cg.criado_em
FROM conteudos_gerados cg
JOIN projetos p ON cg.projeto_id = p.id
LEFT JOIN categorias cat ON cg.categoria_id = cat.id
ORDER BY cg.criado_em DESC
LIMIT 50;

-- ================================================
-- 7. POLÍTICAS DE SEGURANÇA (RLS)
-- ================================================

-- Habilitar Row Level Security
ALTER TABLE projetos ENABLE ROW LEVEL SECURITY;
ALTER TABLE categorias ENABLE ROW LEVEL SECURITY;
ALTER TABLE conteudos_gerados ENABLE ROW LEVEL SECURITY;
ALTER TABLE imagens_geradas ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso (permitir tudo por enquanto - ajuste conforme necessário)
CREATE POLICY "Permitir acesso total a projetos" ON projetos FOR ALL USING (true);
CREATE POLICY "Permitir acesso total a categorias" ON categorias FOR ALL USING (true);
CREATE POLICY "Permitir acesso total a conteudos" ON conteudos_gerados FOR ALL USING (true);
CREATE POLICY "Permitir acesso total a imagens" ON imagens_geradas FOR ALL USING (true);

-- ================================================
-- 8. DADOS DE EXEMPLO (OPCIONAL)
-- ================================================

-- Inserir projeto de exemplo
INSERT INTO projetos (nome, descricao) 
VALUES ('Blog de Tecnologia', 'Blog sobre tecnologia, programação e inovação')
ON CONFLICT (nome) DO NOTHING;

-- Inserir categorias de exemplo
INSERT INTO categorias (projeto_id, nome, exemplo, regras)
SELECT 
    p.id,
    'Tutorial',
    'Neste tutorial, você aprenderá passo a passo como...',
    '- Use tom didático e claro
- Explique cada passo detalhadamente
- Inclua exemplos práticos'
FROM projetos p
WHERE p.nome = 'Blog de Tecnologia'
ON CONFLICT (projeto_id, nome) DO NOTHING;

-- ================================================
-- 9. CONFIRMAÇÃO
-- ================================================

-- Verificar tabelas criadas
SELECT 
    tablename, 
    schemaname 
FROM pg_tables 
WHERE schemaname = 'public' 
    AND tablename IN ('projetos', 'categorias', 'conteudos_gerados', 'imagens_geradas')
ORDER BY tablename;

-- ================================================
-- FIM DO SETUP
-- ================================================
-- Agora você pode usar o Supabase com a aplicação!
-- Lembre-se de configurar SUPABASE_URL e SUPABASE_KEY no .env


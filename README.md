# Blog Content Scraper

## Visão geral

`Blog Content Scraper` é um script em Python para extrair títulos e textos de posts publicados em um site WordPress por meio da REST API nativa.

A ferramenta percorre as páginas do endpoint de posts, remove marcações HTML do conteúdo renderizado e salva o material em um arquivo de texto único, facilitando inventários editoriais, análises offline, auditorias simples de conteúdo e preparação de bases textuais para outros processos.

## Funcionalidades

- Coleta posts a partir do endpoint `/wp-json/wp/v2/posts`.
- Pagina automaticamente os resultados usando `per_page=100`.
- Extrai o título renderizado e o conteúdo renderizado de cada post.
- Remove tags HTML com BeautifulSoup, preservando o texto limpo.
- Gera um arquivo `.txt` com separador entre os posts.
- Registra no terminal erros de acesso, páginas vazias e posts sem conteúdo aproveitável.

## Quando usar

Use este script quando precisar obter rapidamente o conteúdo textual publicado em um blog WordPress para backup simples, revisão editorial, análise de SEO, migração preliminar, comparação de conteúdo ou alimentação de outros fluxos de análise.

A ferramenta trabalha com posts acessíveis pela REST API pública do WordPress. Ela não autentica usuários, não coleta rascunhos, não exporta metadados completos e não substitui um backup estrutural do banco de dados.

## Pré-requisitos

- Python 3.x.
- WordPress com REST API acessível.
- Bibliotecas Python:
  - `requests`
  - `beautifulsoup4`

Instale as dependências com:

```sh
pip install requests beautifulsoup4
```

## Configuração

Abra o arquivo `blog-content-scraper.py` e ajuste a variável:

```python
api_url = 'https://DOMINIO/wp-json/wp/v2/posts'
```

Substitua `DOMINIO` pelo domínio do site WordPress que será analisado.

Exemplo:

```python
api_url = 'https://exemplo.com.br/wp-json/wp/v2/posts'
```

## Execução

No terminal, execute:

```sh
python blog-content-scraper.py
```

Durante a execução, o script acessa a API em páginas sucessivas até encontrar uma página vazia ou receber uma resposta diferente de `200`.

## Arquivo gerado

- `posts_titulos_e_textos.txt`: arquivo em UTF-8 contendo título e texto de cada post, separados por uma linha de `=`.

## Observações

- O resultado depende da disponibilidade pública da REST API do WordPress.
- Sites com bloqueios por firewall, CDN ou autenticação podem impedir a coleta.
- O script remove HTML, mas não preserva estrutura editorial avançada, blocos, categorias, tags, autores ou datas.
- Em sites grandes, a execução pode levar mais tempo e depender da estabilidade do servidor de origem.

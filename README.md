# Blog Content Scraper

## Visão geral

`Blog Content Scraper` é uma ferramenta em Python para extrair títulos e textos de posts públicos de sites WordPress por meio da REST API nativa.

A ferramenta percorre automaticamente todas as páginas do endpoint de posts, remove marcações HTML do conteúdo renderizado e salva o material em um único arquivo de texto UTF-8. É útil para inventários editoriais, análises offline, auditorias de conteúdo, preparação de bases textuais e fluxos de SEO.

## Funcionalidades

- Aceita a URL principal do site WordPress ou o endpoint completo `/wp-json/wp/v2/posts`.
- Normaliza automaticamente a URL para o endpoint de posts.
- Pagina automaticamente os resultados com até 100 posts por requisição.
- Usa os cabeçalhos de paginação do WordPress quando disponíveis.
- Extrai título e conteúdo renderizados de cada post.
- Remove tags HTML com BeautifulSoup.
- Gera um arquivo `.txt` em UTF-8 com separador entre os posts.
- Permite definir o arquivo de saída.
- Permite configurar o timeout das requisições HTTP.
- Trata erros de rede, respostas HTTP inválidas e JSON inesperado.
- Encerra corretamente quando a API informa o fim da paginação.

## Escopo

O Blog Content Scraper trabalha apenas com conteúdo disponibilizado pelo site através da REST API do WordPress. Ele não autentica usuários, não acessa rascunhos privados, não contorna mecanismos de autenticação ou controle de acesso e não substitui um backup completo do WordPress.

Use a ferramenta somente em conteúdo que você esteja autorizado a acessar e processar. Respeite termos de uso, direitos autorais, privacidade, limites do servidor e regras aplicáveis ao site de origem.

## Pré-requisitos

- Python 3.x.
- WordPress com REST API acessível.
- Acesso HTTP ao site de origem.

As dependências Python estão declaradas em `requirements.txt`:

- `requests`
- `beautifulsoup4`

## Instalação

Clone o repositório ou baixe os arquivos e instale as dependências:

```sh
pip install -r requirements.txt
```

## Uso

Informe a URL do site WordPress com `--url`:

```sh
python blog-content-scraper.py --url https://exemplo.com
```

Também é possível informar diretamente o endpoint de posts:

```sh
python blog-content-scraper.py --url https://exemplo.com/wp-json/wp/v2/posts
```

Nos dois casos, a ferramenta utilizará o endpoint:

```text
https://exemplo.com/wp-json/wp/v2/posts
```

### Definir arquivo de saída

Por padrão, o resultado é salvo em `posts_titulos_e_textos.txt`.

Para escolher outro arquivo:

```sh
python blog-content-scraper.py --url https://exemplo.com --output conteudo.txt
```

Também é possível informar um caminho:

```sh
python blog-content-scraper.py --url https://exemplo.com --output exportacao/posts.txt
```

### Definir timeout

O timeout padrão é de 10 segundos por requisição.

Para alterar:

```sh
python blog-content-scraper.py --url https://exemplo.com --timeout 20
```

## Ajuda da linha de comando

```sh
python blog-content-scraper.py --help
```

## Arquivo gerado

O arquivo de saída contém o título e o texto limpo de cada post, separados por uma linha de `=`.

O arquivo padrão `posts_titulos_e_textos.txt` está incluído no `.gitignore` para reduzir o risco de conteúdo coletado ser versionado acidentalmente.

## Comportamento da paginação

A ferramenta solicita até 100 posts por página, conforme permitido pela REST API padrão do WordPress.

Quando o servidor fornece o cabeçalho `X-WP-TotalPages`, ele é usado para determinar o fim da coleta. A ferramenta também reconhece a resposta padrão `rest_post_invalid_page_number` como término normal da paginação em páginas subsequentes.

## Limitações

- Apenas posts públicos acessíveis pela REST API são coletados.
- O script não exporta banco de dados, configurações, usuários, comentários ou arquivos de mídia.
- Categorias, tags, autores, datas e outros metadados não são incluídos na saída atual.
- A conversão para texto remove a estrutura HTML e pode simplificar formatação editorial.
- Firewalls, WAFs, CDNs, autenticação, rate limiting ou REST API desabilitada podem impedir a coleta.
- Sites grandes podem exigir mais tempo de execução e maior tolerância de timeout.

## Segurança e privacidade

Não inclua credenciais, tokens, chaves de API ou outros segredos na linha de comando, no código, em issues ou em pull requests.

O conteúdo exportado pode estar sujeito a direitos autorais, regras de privacidade e outras obrigações. O usuário da ferramenta é responsável por verificar se possui autorização e base adequada para coletar, armazenar e processar o conteúdo.

Vulnerabilidades de segurança não devem ser relatadas em issues públicas. Consulte [`SECURITY.md`](SECURITY.md).

## Contribuições

Contribuições são bem-vindas. Consulte [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de enviar alterações.

## Teste básico

Para verificar a sintaxe do script:

```sh
python -m py_compile blog-content-scraper.py
```

## Licença

Este projeto é distribuído sob a MIT License.

Copyright (c) 2024-2026 Rede Piabanha.

Consulte o arquivo [`LICENSE`](LICENSE) para os termos completos.

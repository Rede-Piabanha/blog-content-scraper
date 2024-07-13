# Blog Content Scrapper

## Descrição

Este script, `Blog Content Scrapper`, foi desenvolvido para acessar a API REST do WordPress, obter todos os títulos e textos das postagens de um blog e salvá-los em um arquivo `.txt`. É uma ferramenta útil para quem deseja fazer backup do conteúdo de um blog ou analisar o conteúdo offline.

## Funcionalidades

- **Obter Conteúdo das Postagens**: Acessa a API REST do WordPress para obter o título e o conteúdo de todas as postagens de um blog.
- **Salvar Conteúdo em Arquivo**: Salva os títulos e textos das postagens em um arquivo `.txt`, separados por linhas de "===", para facilitar a leitura e organização.

## Utilidade

Este script é útil para proprietários de blogs, profissionais de SEO e desenvolvedores que precisam acessar e salvar o conteúdo de um blog WordPress de forma programática. Ele permite fazer backup do conteúdo e realizar análises offline.

## Pré-requisitos

- Python 3.x
- Biblioteca Python: requests, beautifulsoup4

## Como Usar

1. **Configurar o Ambiente**: Certifique-se de ter o Python 3.x instalado e instale as bibliotecas necessárias:
    ```sh
    pip install requests beautifulsoup4
    ```

2. **Editar o Script**: Atualize a variável `api_url` no script com o URL da API REST do seu site WordPress.

3. **Executar o Script**: Execute o script:
    ```sh
    python blog-content-scrapper.py
    ```

4. **Verificar os Resultados**: Os títulos e textos das postagens serão salvos em um arquivo chamado `posts_titulos_e_textos.txt`.

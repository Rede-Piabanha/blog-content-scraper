import requests
from bs4 import BeautifulSoup

api_url = 'https://DOMAIN/wp-json/wp/v2/posts'

def get_all_posts_content(api_url):
    posts_content = []
    page = 1
    while True:
        response = requests.get(f"{api_url}?page={page}&per_page=100")
        if response.status_code != 200:
            print(f"Erro ao acessar a API na página {page}: {response.status_code}")
            break
        posts = response.json()
        if not posts:
            print(f"Nenhum post encontrado na página {page}")
            break
        for post in posts:
            content = BeautifulSoup(post['content']['rendered'], 'html.parser').get_text()
            title = post['title']['rendered']
            full_text = f"{title}\n\n{content}\n\n"
            if full_text.strip() == "":
                print(f"Post vazio encontrado: {post['link']}")
            else:
                posts_content.append(full_text)
        page += 1
    return posts_content

posts_content = get_all_posts_content(api_url)

with open('posts_titulos_e_textos.txt', 'w', encoding='utf-8') as file:
    for content in posts_content:
        file.write(content)
        file.write("\n" + "="*80 + "\n")  # Separador entre posts

print("Os títulos e textos dos posts foram salvos em 'posts_titulos_e_textos.txt'")

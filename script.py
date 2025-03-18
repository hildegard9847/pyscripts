import os
import requests

# Defina o caminho onde você quer salvar as imagens
caminho_pasta = r"E:\SBA\imagens_baixadas"

# Crie a pasta, se ela não existir
os.makedirs(caminho_pasta, exist_ok=True)

# Caminho para o arquivo de links
arquivo_links = r"E:\SBA\links.txt"

# Abra e leia o arquivo com os links
with open(arquivo_links, 'r') as file:
    links = file.readlines()

# Para cada link no arquivo
for i, link in enumerate(links, start=1):
    link = link.strip()  # Remover espaços extras e quebras de linha
    try:
        # Baixar o conteúdo do link
        response = requests.get(link)
        response.raise_for_status()  # Verificar se houve erro no download

        # Extrair o nome do arquivo da URL
        nome_arquivo = f"imagem_{i}.jpg"  # Aqui você pode personalizar o nome

        # Caminho completo onde a imagem será salva
        caminho_imagem = os.path.join(caminho_pasta, nome_arquivo)

        # Salvar a imagem no diretório especificado
        with open(caminho_imagem, 'wb') as img_file:
            img_file.write(response.content)

        print(f"Imagem {nome_arquivo} baixada com sucesso!")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem do link {link}: {e}")

print("Download completo!")

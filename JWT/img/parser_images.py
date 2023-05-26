import os
import re

# Define o padrão de nome do arquivo
pattern = r'^Pasted_image_[0-9]{14}\.png$'

# Procura por todos os arquivos no diretório atual
files = os.listdir()

# Loop para processar cada arquivo encontrado
for filename in files:
    print(filename)
    # Verifica se o nome do arquivo corresponde ao padrão esperado
    if re.match(pattern, filename):
        # Obtém o novo nome do arquivo substituindo os espaços em branco por "%20"
        new_filename = filename.replace("%20", "_")
        
        # Renomeia o arquivo
        os.rename(filename, new_filename)
        
        print(f"O arquivo {filename} foi renomeado para {new_filename}")

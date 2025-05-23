from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
from tqdm import tqdm


# 📁 Diretório local de destino
output_dir = '/workspace/eda/raw-data/fiap_dl'
os.makedirs(output_dir, exist_ok=True)


# 🔐 Autenticação OAuth interativa
gauth = GoogleAuth()

# 🔧 Usa credenciais locais salvas para não precisar autenticar sempre
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Primeira autenticação interativa
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh do token automaticamente
    gauth.Refresh()
else:
    # Já autenticado
    gauth.Authorize()

# 🔒 Salva as credenciais para uso futuro
gauth.SaveCredentialsFile("mycreds.txt")


# 🚩 Solicita ao usuário o ID da pasta
folder_id = input("🔗 Cole aqui o ID da pasta do Google Drive que deseja baixar: ").strip()

# 🔍 Listar arquivos na pasta
drive = GoogleDrive(gauth)

# Query para pegar todos os arquivos da pasta
file_list = drive.ListFile(
    {'q': f"'{folder_id}' in parents and trashed=false"}
).GetList()

print(f'📑 {len(file_list)} arquivos encontrados na pasta.')

# ⬇️ Download com barra de progresso
for file in tqdm(file_list, desc="⬇️ Baixando arquivos"):
    file_title = file['title']
    file_path = os.path.join(output_dir, file_title)
    print(f"➡️ Baixando {file_title}...")
    file.GetContentFile(file_path)

print("✅ Download concluído!")

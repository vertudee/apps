#!/bin/bash

# Configuração de Identidade
git config --global user.name "vertudee"
git config --global user.email "vertudee@gmail.com"

echo "--- 🧊 Z-SYSTEM: INICIANDO UPLOAD MUNDIAL ---"

# Adicionando os arquivos (help.md, z_engine.c, etc)
git add .

# Criando a versão
git commit -m "Global Release: Z-Block Universal Symmetry"

# Pedindo o Token (ele não vai aparecer enquanto você cola)
echo "Cole seu Personal Access Token (PAT) do GitHub:"
read -s MY_TOKEN

# Configurando a URL com o Token e enviando
git remote set-url origin https://vertudee:$MY_TOKEN@github.com/vertudee/apps.git

# Tenta enviar para main ou master (ajusta conforme seu repo)
git push origin main || git push origin master

echo "--- ✅ PROCESSO CONCLUÍDO ---"


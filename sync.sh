#!/usr/bin/env bash
echo "=== Sync run: $(date) ==="
# Sincronização automática do repositório INFRAESTRUTURA

cd /home/wrm/INFRAESTRUTURA

# Atualiza referências remotas sem misturar no branch
git fetch origin

# Prepara todas as mudanças (exceto as no .gitignore)
git add .

# Se houver algo novo, commita com timestamp
git diff-index --quiet HEAD || git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"

# Envia para o branch main no remoto
git push origin main

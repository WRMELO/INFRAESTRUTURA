
## **Configuração de Container Jupyter com DevContainers no Cursor IDE**

### **📋 Resumo do que foi configurado**

Criamos uma integração completa entre um container Docker jupyter-cpu e o Cursor IDE usando DevContainers, permitindo desenvolvimento remoto com acesso total ao sistema de arquivos local e autenticação GitHub.

---

### **🏗️ Estrutura criada**

```
/home/wrm/INFRAESTRUTURA/
├── docker-compose.yml      # Configuração dos serviços Docker
├── .devcontainer/         # Pasta de configuração do DevContainer
│   └── devcontainer.json  # Configuração do ambiente de desenvolvimento
└── [outros arquivos do projeto]
```

---

### **📄 Arquivo: docker-compose.yml**

```yaml
services:
  jupyter-cpu:
    image: jupyter-cpu:latest
    container_name: jupyter_cpu
    ports:
      - "8888:8888"
    environment:
      JUPYTER_ENABLE_LAB: "yes"
      JUPYTER_TOKEN: "senhasegura"
    volumes:
      - /home/wrm:/home/wrm:rw                              # Acesso total ao home
      - /home/wrm/INFRAESTRUTURA:/home/jovyan/work:rshared  # Workspace Jupyter
      - ~/.ssh:/root/.ssh:ro                                # Chaves SSH (read-only)
      - ~/.gitconfig:/root/.gitconfig:ro                    # Config Git (read-only)
    restart: unless-stopped
```

**Explicação dos volumes:**

- `/home/wrm:/home/wrm:rw` - Monta todo o diretório home com leitura/escrita
- `/home/jovyan/work:rshared` - Workspace padrão do Jupyter com compartilhamento recursivo
- `~/.ssh:/root/.ssh:ro` - Compartilha chaves SSH em modo somente-leitura para segurança
- `~/.gitconfig:/root/.gitconfig:ro` - Compartilha configurações do Git

---

### **📄 Arquivo: .devcontainer/devcontainer.json**

```json
{
  "name": "Jupyter CPU Development",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "jupyter-cpu",
  "workspaceFolder": "/home/wrm",
  "remoteUser": "root",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-keymap",
        "ms-toolsai.jupyter-renderers",
        "ms-toolsai.vscode-jupyter-cell-tags",
        "ms-toolsai.vscode-jupyter-slideshow",
        "ms-azuretools.vscode-docker",
        "github.copilot",
        "github.copilot-chat",
        "eamodio.gitlens",
        "mhutchie.git-graph",
        "donjayamanne.githistory",
        "streetsidesoftware.code-spell-checker",
        "streetsidesoftware.code-spell-checker-portuguese-brazilian",
        "yzhang.markdown-all-in-one",
        "bierner.markdown-mermaid",
        "davidanson.vscode-markdownlint"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/opt/conda/bin/python",
        "jupyter.jupyterServerType": "local",
        "terminal.integrated.defaultProfile.linux": "bash",
        "editor.formatOnSave": true,
        "python.formatting.provider": "black",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000
      }
    }
  },
  "postCreateCommand": "echo 'Container pronto para desenvolvimento!'",
  "features": {}
}
```

**Principais configurações:**

- **workspaceFolder**: Define `/home/wrm` como pasta de trabalho principal
- **remoteUser**: Usa `root` para ter permissões totais
- **extensions**: Conjunto completo de extensões para Python, Jupyter, Git e Markdown
- **settings**: Configurações otimizadas para desenvolvimento Python/Jupyter

---

### **🔧 O que foi configurado**

1. **Acesso ao Sistema de Arquivos**
    
    - Container tem acesso total a `/home/wrm`
    - Pode ler/escrever em qualquer arquivo do usuário
    - Workspace Jupyter mapeado para facilitar navegação
2. **Autenticação GitHub via SSH**
    
    - Chaves SSH Ed25519 compartilhadas com o container
    - Configuração do Git (nome: Wilson Melo, email: GitHub noreply)
    - Permite fazer commits e push diretamente do container
3. **Ambiente de Desenvolvimento**
    
    - Cursor IDE conecta diretamente ao container
    - Extensões Python, Jupyter e Git pré-configuradas
    - Terminal integrado com acesso root
    - Auto-save e formatação automática habilitados

---

### **🚀 Como usar**

1. **Iniciar o container:**
    
    ```bash
    cd /home/wrm/INFRAESTRUTURA
    docker-compose up -d
    ```
    
2. **Abrir no Cursor:**
    
    - Pressione `Ctrl+Shift+P`
    - Digite: "Dev Containers: Open Folder in Container"
    - Selecione `/home/wrm/INFRAESTRUTURA`
3. **Verificar funcionamento:**
    
    ```bash
    # No terminal do Cursor (dentro do container)
    ssh -T git@github.com  # Deve mostrar: Hi WRMELO!
    git config --list      # Deve mostrar suas configurações
    ls -la /home/wrm       # Deve listar seus arquivos
    ```
    

---

### **✅ Benefícios da configuração**

- **Desenvolvimento isolado**: Ambiente Python/Jupyter consistente
- **Acesso total**: Pode editar qualquer arquivo em `/home/wrm`
- **Git integrado**: Commits com suas credenciais reais
- **Extensões prontas**: Todas as ferramentas necessárias pré-instaladas
- **Segurança**: Chaves SSH em modo read-only, container isolado

---

### **📝 Notas importantes**

- O token do Jupyter está definido como "senhasegura" (recomenda-se alterar)
- O container roda como root para ter acesso total aos arquivos
- As chaves SSH são montadas em modo somente-leitura por segurança
- O workspace principal é `/home/wrm`, mas o Jupyter vê `/home/jovyan/work`
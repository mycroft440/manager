#!/bin/bash
#
# Script de Instalação do Gerenciador MultiFlow
#
# Este script automatiza a instalação do Gerenciador MultiFlow,
# incluindo a verificação do sistema, instalação de dependências,
# configuração do ambiente e criação de um comando de atalho.
#

# --- Definição de Cores para o Terminal ---
# Usado para formatar as saídas do script e melhorar a visualização.
cor_vermelha='\033[0;31m'
cor_verde='\033[0;32m'
cor_amarela='\033[0;33m'
cor_azul='\033[0;34m'
cor_reset='\033[0m' # Reseta a cor para o padrão do terminal

# --- Funções Auxiliares ---

# Função para exibir mensagens formatadas com cores.
# Argumentos:
#   $1: Código da cor a ser usada.
#   $2: Texto da mensagem a ser exibida.
mensagem() {
    local cor="$1"
    local texto="$2"
    echo -e "${cor}${texto}${cor_reset}"
}

# Função para verificar se o script está sendo executado com privilégios de root.
verificar_root() {
    if [ "$(id -u)" -ne 0 ]; then
        mensagem "${cor_vermelha}" "Erro: Este script precisa ser executado como root."
        mensagem "${cor_amarela}" "Tente novamente usando 'sudo bash install.sh'"
        exit 1
    fi
}

# Função para verificar se o sistema operacional é compatível (Debian ou Ubuntu).
verificar_sistema() {
    mensagem "${cor_azul}" "Verificando o sistema operacional..."
    if [ -f /etc/os-release ]; then
        # Carrega as variáveis do arquivo para identificar o SO
        . /etc/os-release
        if [[ "$ID" == "ubuntu" || "$ID" == "debian" ]]; then
            mensagem "${cor_verde}" "Sistema operacional compatível ($NAME) detectado."
        else
            mensagem "${cor_vermelha}" "Erro: Este script é compatível apenas com sistemas Debian ou Ubuntu."
            exit 1
        fi
    else
        mensagem "${cor_vermelha}" "Erro: Não foi possível determinar o sistema operacional."
        exit 1
    fi
}

# Função para instalar as dependências necessárias para o script.
instalar_dependencias() {
    mensagem "${cor_azul}" "Atualizando a lista de pacotes do sistema..."
    if ! apt-get update -y; then
        mensagem "${cor_vermelha}" "Falha ao atualizar a lista de pacotes. Verifique sua conexão e repositórios."
        exit 1
    fi

    mensagem "${cor_azul}" "Instalando dependências necessárias..."
    # Lista de pacotes que o script principal e suas ferramentas precisam.
    local dependencias=("python3" "python3-pip" "screen" "unzip" "wget" "git" "curl")
    
    for dep in "${dependencias[@]}"; do
        # Utiliza dpkg-query para uma verificação mais robusta se o pacote está instalado.
        if ! dpkg-query -W -f='${Status}' "$dep" 2>/dev/null | grep -q "ok installed"; then
            mensagem "${cor_amarela}" "Instalando ${dep}..."
            if ! apt-get install -y "$dep"; then
                mensagem "${cor_vermelha}" "Falha ao instalar o pacote '${dep}'. A instalação será abortada."
                exit 1
            fi
        else
            mensagem "${cor_verde}" "Dependência '${dep}' já está instalada."
        fi
    done
}

# Função para configurar o ambiente, criando diretórios e copiando arquivos.
configurar_ambiente() {
    local diretorio_manager="/etc/manager"
    
    mensagem "${cor_azul}" "Configurando o ambiente em '${diretorio_manager}'..."
    
    if ! mkdir -p "${diretorio_manager}"; then
        mensagem "${cor_vermelha}" "Falha ao criar o diretório base: ${diretorio_manager}."
        exit 1
    fi

    # Copia todos os arquivos do diretório atual (incluindo ocultos) para o destino.
    # O uso de 'cp -a' preserva as permissões dos arquivos.
    mensagem "${cor_azul}" "Copiando arquivos do projeto..."
    if ! cp -a ./. "${diretorio_manager}/"; then
        mensagem "${cor_vermelha}" "Falha ao copiar os arquivos para ${diretorio_manager}."
        exit 1
    fi

    # Lista de scripts que precisam de permissão de execução.
    local scripts_executaveis=(
        "${diretorio_manager}/install.sh"
        "${diretorio_manager}/multiflow.py"
        "${diretorio_manager}/multiflow_wrapper.sh"
        "${diretorio_manager}/conexoes/badvpn_wrapper"
        "${diretorio_manager}/conexoes/openvpn.sh"
        "${diretorio_manager}/conexoes/multiflowproxy/instalar_deps_multiflowpx.py"
    )

    mensagem "${cor_azul}" "Concedendo permissões de execução..."
    for script in "${scripts_executaveis[@]}"; do
        if [ -f "$script" ]; then
            if ! chmod +x "$script"; then
                 mensagem "${cor_vermelha}" "Falha ao conceder permissão de execução para '$script'."
                 # Não abortamos a instalação, mas avisamos o usuário.
            fi
        else
            mensagem "${cor_amarela}" "Aviso: O arquivo de script '$script' não foi encontrado para dar permissão."
        fi
    done
}

# Função para criar um atalho global para o script principal.
criar_comando() {
    local caminho_comando="/usr/local/bin/manager"
    mensagem "${cor_azul}" "Criando o comando de atalho 'manager'..."

    # Usa 'tee' para criar o script wrapper que executa o programa principal.
    # Isso permite que o usuário chame 'manager' de qualquer lugar no sistema.
    if ! tee "${caminho_comando}" > /dev/null <<EOF
#!/bin/bash
# Wrapper para executar o script principal do Gerenciador MultiFlow.
# Muda para o diretório do script e o executa com os argumentos passados.
cd /etc/manager && python3 multiflow.py "\$@"
EOF
    then
        mensagem "${cor_vermelha}" "Falha ao criar o arquivo de comando em ${caminho_comando}."
        exit 1
    fi

    if ! chmod +x "${caminho_comando}"; then
        mensagem "${cor_vermelha}" "Falha ao dar permissão de execução para o comando ${caminho_comando}."
        exit 1
    fi
}

# --- Função Principal de Execução ---
main() {
    clear # Limpa a tela para uma apresentação mais limpa
    mensagem "${cor_verde}" "--- Iniciando Instalação do Gerenciador MultiFlow ---"
    
    verificar_root
    verificar_sistema
    instalar_dependencias
    configurar_ambiente
    criar_comando
    
    echo # Linha em branco para espaçamento
    mensagem "${cor_verde}" "====================================================="
    mensagem "${cor_verde}" "  Instalação concluída com sucesso!                  "
    mensagem "${cor_verde}" "====================================================="
    mensagem "${cor_amarela}" "Para iniciar, basta executar o comando: manager"
    echo # Linha em branco para espaçamento
}

# Ponto de entrada do script: executa a função principal.
main

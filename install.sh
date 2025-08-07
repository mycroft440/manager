#!/bin/bash
# Script de Instalação do Gerenciador MultiFlow
#
# Este script automatiza a instalação do Gerenciador MultiFlow,
# incluindo a verificação do sistema, instalação de dependências,
# configuração do ambiente e criação de um comando de atalho.
#

# --- Definição de Cores para o Terminal ---
# Usado para formatar as saídas do script e melhorar a visualização.
cor_vermelha="\033[0;31m"
cor_verde="\033[0;32m"
cor_amarela="\033[0;33m"
cor_azul="\033[0;34m"
cor_reset="\033[0m" # Reseta a cor para o padrão do terminal

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
        if [ "$ID" == "ubuntu" ] || [ "$ID" == "debian" ]; then
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
}



# Execução principal do script
verificar_root
verificar_sistema
instalar_dependencias


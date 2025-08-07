import os
import subprocess
import time

# --- Início da Correção ---
# Determina o caminho absoluto para o diretório raiz do projeto (a pasta 'manager')
# Isso torna o script funcional independentemente de onde ele é executado.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Constrói os caminhos corretos para os arquivos e diretórios do multiflowproxy
PROXY_DIR = os.path.join(BASE_DIR, 'conexoes', 'multiflowproxy')
BUILD_DIR = os.path.join(PROXY_DIR, 'build')
EXECUTABLE_PATH = os.path.join(BUILD_DIR, 'proxy')
SERVICE_FILE_SRC = os.path.join(PROXY_DIR, 'multiflowpx.service')
SERVICE_FILE_DEST = '/etc/systemd/system/multiflowpx.service'
DEPS_INSTALLER_SCRIPT = os.path.join(PROXY_DIR, 'instalar_deps_multiflowpx.py')
# --- Fim da Correção ---

# Cores para o menu
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'
W = '\033[0m'

def print_header():
    """Imprime o cabeçalho do menu."""
    os.system('clear')
    print(f'{C}=================================================={W}')
    print(f'{C}      Gerenciador de Conexão MultiFlow Proxy      {W}')
    print(f'{C}=================================================={W}\n')

def run_command(command, cwd=None):
    """Executa um comando no shell e mostra a saída."""
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f'{R}Erro ao executar o comando: {e}{W}')
        return False
    return True

def is_service_active():
    """Verifica se o serviço multiflowpx está ativo."""
    try:
        # Usamos 'is-active' e suprimimos a saída para apenas obter o status
        subprocess.check_call(
            'systemctl is-active --quiet multiflowpx.service',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def mostrar_status():
    """Mostra o status atual do serviço MultiFlow Proxy."""
    print_header()
    print(f'{Y}Verificando status do MultiFlow Proxy...{W}\n')
    if is_service_active():
        print(f'{G}Serviço MultiFlow Proxy está ATIVO.{W}')
        # Mostra as últimas linhas do log do serviço
        run_command('journalctl -u multiflowpx.service -n 10 --no-pager')
    else:
        print(f'{R}Serviço MultiFlow Proxy está INATIVO.{W}')
    print('\nPressione Enter para voltar ao menu...')
    input()

def instalar_multiflow_proxy():
    """Instala as dependências e compila o MultiFlow Proxy."""
    print_header()
    print(f'{Y}Iniciando a instalação do MultiFlow Proxy...{W}\n')
    
    # 1. Instalar dependências
    print(f'{C}Instalando dependências necessárias...{W}')
    if not run_command(f'python3 {DEPS_INSTALLER_SCRIPT}'):
        print(f'{R}Falha ao instalar dependências. A instalação foi abortada.{W}')
        return

    # 2. Criar diretório de build se não existir
    if not os.path.exists(BUILD_DIR):
        print(f'{C}Criando diretório de build...{W}')
        os.makedirs(BUILD_DIR)

    # 3. Compilar o proxy
    print(f'{C}Compilando o proxy... Isso pode levar alguns minutos.{W}')
    if not run_command('cmake ..', cwd=BUILD_DIR):
        print(f'{R}Erro durante a execução do CMake. A compilação falhou.{W}')
        return
    if not run_command('make', cwd=BUILD_DIR):
        print(f'{R}Erro durante a execução do make. A compilação falhou.{W}')
        return

    print(f'\n{G}MultiFlow Proxy compilado com sucesso!{W}')
    print(f'{Y}O executável está em: {EXECUTABLE_PATH}{W}')
    print('\nPressione Enter para voltar ao menu...')
    input()

def iniciar_multiflow_proxy():
    """Inicia o serviço do MultiFlow Proxy."""
    print_header()
    if not os.path.exists(EXECUTABLE_PATH):
        print(f'{R}Executável não encontrado!{W}')
        print(f'{Y}Por favor, instale o MultiFlow Proxy primeiro (opção 1).{W}')
        time.sleep(3)
        return

    if is_service_active():
        print(f'{G}O serviço já está em execução.{W}')
        print(f'{Y}Se desejar reiniciar, pare o serviço primeiro.{W}')
        time.sleep(3)
        return

    print(f'{Y}Iniciando o serviço MultiFlow Proxy...{W}\n')
    
    # Copia o arquivo de serviço e o configura
    print(f'{C}Configurando o serviço systemd...{W}')
    run_command(f'sudo cp {SERVICE_FILE_SRC} {SERVICE_FILE_DEST}')
    run_command('sudo systemctl daemon-reload')
    run_command('sudo systemctl enable multiflowpx.service')
    
    # Inicia o serviço
    if run_command('sudo systemctl start multiflowpx.service'):
        print(f'\n{G}Serviço MultiFlow Proxy iniciado com sucesso!{W}')
    else:
        print(f'\n{R}Falha ao iniciar o serviço. Verifique os logs com a opção 3.{W}')
    
    time.sleep(2)

def parar_multiflow_proxy():
    """Para o serviço do MultiFlow Proxy."""
    print_header()
    if not is_service_active():
        print(f'{R}O serviço não está em execução.{W}')
        time.sleep(2)
        return

    print(f'{Y}Parando o serviço MultiFlow Proxy...{W}\n')
    if run_command('sudo systemctl stop multiflowpx.service'):
        print(f'\n{G}Serviço parado com sucesso!{W}')
    else:
        print(f'\n{R}Falha ao parar o serviço.{W}')
    
    time.sleep(2)

def desinstalar_multiflow_proxy():
    """Para o serviço e remove os arquivos de instalação."""
    print_header()
    print(f'{R}ATENÇÃO: Isso irá parar o serviço e remover os arquivos do MultiFlow Proxy.{W}')
    confirm = input(f'{Y}Você tem certeza que deseja desinstalar? (s/n): {W}').lower()

    if confirm != 's':
        print(f'\n{G}Desinstalação cancelada.{W}')
        time.sleep(2)
        return

    print(f'\n{Y}Iniciando a desinstalação...{W}')
    
    # Parar e desabilitar o serviço
    if os.path.exists(SERVICE_FILE_DEST):
        print(f'{C}Parando e desabilitando o serviço...{W}')
        run_command('sudo systemctl stop multiflowpx.service')
        run_command('sudo systemctl disable multiflowpx.service')
        run_command(f'sudo rm {SERVICE_FILE_DEST}')
        run_command('sudo systemctl daemon-reload')

    # Remover o diretório do proxy
    # Opcional: descomente a linha abaixo se quiser remover a pasta inteira
    # print(f'{C}Removendo o diretório {PROXY_DIR}...{W}')
    # run_command(f'rm -rf {PROXY_DIR}')
    
    print(f'\n{G}MultiFlow Proxy desinstalado com sucesso!{W}')
    print('\nPressione Enter para voltar ao menu...')
    input()

def main():
    """Função principal que exibe o menu."""
    while True:
        print_header()
        
        status_str = f'{G}Ativo{W}' if is_service_active() else f'{R}Inativo{W}'
        print(f'Status do Serviço: [{status_str}]\n')

        print(f'{Y}1.{W} {C}Instalar/Recompilar MultiFlow Proxy{W}')
        print(f'{Y}2.{W} {G}Iniciar MultiFlow Proxy{W}')
        print(f'{Y}3.{W} {R}Parar MultiFlow Proxy{W}')
        print(f'{Y}4.{W} {C}Verificar Status/Logs{W}')
        print(f'{Y}5.{W} {R}Desinstalar MultiFlow Proxy{W}')
        print(f'\n{Y}0.{W} {C}Voltar ao menu principal{W}')
        print(f'{C}=================================================={W}\n')

        try:
            choice = input(f'Escolha uma opção: {W}')
            if choice == '1':
                instalar_multiflow_proxy()
            elif choice == '2':
                iniciar_multiflow_proxy()
            elif choice == '3':
                parar_multiflow_proxy()
            elif choice == '4':
                mostrar_status()
            elif choice == '5':
                desinstalar_multiflow_proxy()
            elif choice == '0':
                break
            else:
                print(f'\n{R}Opção inválida. Tente novamente.{W}')
                time.sleep(1)
        except (KeyboardInterrupt, EOFError):
            print(f'\n\n{R}Saindo do menu...{W}')
            break

if __name__ == '__main__':
    # Verifica se o script está sendo executado como root, se necessário
    if os.geteuid() != 0:
        print(f"{R}Atenção: Algumas operações (como gerenciar o serviço) podem exigir privilégios de root.{W}")
        time.sleep(2)
    main()

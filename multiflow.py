import os
import time
import subprocess

# --- Início da Atualização ---
# Importa os módulos dos menus, incluindo o novo para o MultiFlow Proxy
from ssh_user_manager import main as ssh_manager_main
from menus.menu_badvpn import main as badvpn_main
from menus.menu_proxysocks import main as proxysocks_main
from menus.menu_multiflowproxy import main as multiflowproxy_main
from ferramentas.swap import gerenciar_swap
from ferramentas.zram import gerenciar_zram
from ferramentas.otimizadorvps import main as otimizar_vps
# --- Fim da Atualização ---

# Cores
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'
W = '\033[0m'

def print_header(title):
    """Função para imprimir um cabeçalho padronizado."""
    os.system('clear')
    print(f'{C}=================================================={W}')
    print(f'{C}{title.center(50)}{W}')
    print(f'{C}=================================================={W}\n')

def run_script(script_path):
    """Função para executar um script shell."""
    try:
        subprocess.run(['bash', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{R}Erro ao executar o script {script_path}: {e}{W}")
    except FileNotFoundError:
        print(f"{R}Erro: Script {script_path} não encontrado.{W}")
    print(f"\n{Y}Pressione Enter para continuar...{W}")
    input()

def gerenciar_conexoes():
    """Menu para gerenciar diferentes tipos de conexões."""
    while True:
        print_header("Gerenciar Conexões")
        # --- Início da Atualização ---
        # Adicionada a opção para o MultiFlow Proxy
        print(f"{Y}1.{W} {C}Gerenciar BadVPN{W}")
        print(f"{Y}2.{W} {C}Gerenciar Proxy Socks{W}")
        print(f"{Y}3.{W} {C}Gerenciar MultiFlow Proxy{W}")
        print(f"{Y}4.{W} {C}Instalar OpenVPN{W}")
        print(f"\n{Y}0.{W} {C}Voltar ao Menu Principal{W}")
        # --- Fim da Atualização ---
        print(f'{C}=================================================={W}\n')

        choice = input(f"Escolha uma opção: {W}")

        if choice == '1':
            badvpn_main()
        elif choice == '2':
            proxysocks_main()
        # --- Início da Atualização ---
        # Adicionado o case para chamar o menu do MultiFlow Proxy
        elif choice == '3':
            multiflowproxy_main()
        elif choice == '4':
            run_script('conexoes/openvpn.sh')
        # --- Fim da Atualização ---
        elif choice == '0':
            break
        else:
            print(f"\n{R}Opção inválida. Tente novamente.{W}")
            time.sleep(1)

def ferramentas_utilitarios():
    """Menu para ferramentas e utilitários da VPS."""
    while True:
        print_header("Ferramentas e Utilitários")
        print(f"{Y}1.{W} {C}Otimizador de VPS{W}")
        print(f"{Y}2.{W} {C}Gerenciar Memória SWAP{W}")
        print(f"{Y}3.{W} {C}Gerenciar ZRAM{W}")
        print(f"\n{Y}0.{W} {C}Voltar ao Menu Principal{W}")
        print(f'{C}=================================================={W}\n')

        choice = input(f"Escolha uma opção: {W}")

        if choice == '1':
            otimizar_vps()
        elif choice == '2':
            gerenciar_swap()
        elif choice == '3':
            gerenciar_zram()
        elif choice == '0':
            break
        else:
            print(f"\n{R}Opção inválida. Tente novamente.{W}")
            time.sleep(1)

def main_menu():
    """Função principal que exibe o menu principal."""
    while True:
        print_header("MultiFlow Manager")
        print(f"{Y}1.{W} {C}Gerenciar Usuários SSH{W}")
        print(f"{Y}2.{W} {C}Gerenciar Conexões{W}")
        print(f"{Y}3.{W} {C}Ferramentas e Utilitários{W}")
        print(f"\n{Y}0.{W} {R}Sair{W}")
        print(f'{C}=================================================={W}\n')

        choice = input(f"Escolha uma opção: {W}")

        if choice == '1':
            ssh_manager_main()
        elif choice == '2':
            gerenciar_conexoes()
        elif choice == '3':
            ferramentas_utilitarios()
        elif choice == '0':
            print(f"\n{Y}Saindo do MultiFlow Manager...{W}")
            break
        else:
            print(f"\n{R}Opção inválida. Tente novamente.{W}")
            time.sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{R}Este script precisa ser executado como root para funcionar corretamente.{W}")
        print(f"{Y}Por favor, execute com 'sudo python3 multiflow.py'{W}")
        exit(1)
    main_menu()



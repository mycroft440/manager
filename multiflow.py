#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo principal do Gerenciador MultiFlow.

Este script serve como ponto de entrada para um painel de gerenciamento de
serviços de SSH, VPN e proxies. Ele fornece um menu interativo no console
para acessar diferentes funcionalidades, como gerenciamento de usuários,
serviços de conexão e ferramentas de otimização de servidor.
"""

import os
import sys
import subprocess
import time

# --- Importações de Módulos Locais ---
# Importa funções e menus de outros arquivos do projeto.
# A estrutura modular facilita a manutenção e expansão do código.
try:
    from menus.menu_style_utils import (
        print_header, print_menu, print_error, print_success, print_info,
        get_user_input, clear_screen
    )
    from ssh_user_manager import main as ssh_manager_main
    from menus.menu_badvpn import menu_badvpn_main
    from menus.menu_proxysocks import menu_proxysocks_main
    from menus.menu_multiflowproxy import menu_multiflowproxy_main
    from ferramentas.otimizadorvps import optimize_vps
    from ferramentas.swap import manage_swap
    from ferramentas.zram import manage_zram
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Verifique se todos os arquivos do script estão no lugar correto e tente novamente.")
    sys.exit(1)

# --- Constantes ---
# Define o diretório base do script para garantir que os caminhos de arquivos funcionem corretamente.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def check_root():
    """
    Verifica se o script está sendo executado com privilégios de superusuário (root).
    O script encerra se não for executado como root, pois muitas de suas
    funções exigem permissões elevadas para modificar configurações do sistema.
    """
    if os.geteuid() != 0:
        print_error("Este script precisa ser executado como superusuário (root).")
        sys.exit(1)


def tools_menu():
    """
    Exibe e gerencia o submenu de ferramentas e otimizações.
    """
    while True:
        clear_screen()
        print_header("Ferramentas e Otimizações")
        
        tools_options = {
            "1": "Otimizador de VPS (TCP BBR, etc)",
            "2": "Gerenciar Memória SWAP",
            "3": "Gerenciar ZRAM",
            "0": "Voltar ao Menu Principal"
        }
        print_menu(tools_options)
        
        choice = get_user_input("Escolha uma opção")

        if choice == "1":
            optimize_vps()
        elif choice == "2":
            manage_swap()
        elif choice == "3":
            manage_zram()
        elif choice == "0":
            break
        else:
            print_error("Opção inválida. Por favor, tente novamente.")
            time.sleep(2)


def update_script():
    """
    Atualiza o script para a versão mais recente a partir do repositório Git.
    """
    print_info("Tentando atualizar o script a partir do repositório Git...")
    try:
        # Garante que o comando git seja executado no diretório do script.
        os.chdir(BASE_DIR)
        
        # Executa 'git pull' para buscar e aplicar atualizações.
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True,
            check=True,  # Lança uma exceção se o comando falhar.
            encoding='utf-8'
        )
        
        if "Already up to date." in result.stdout:
            print_info("O script já está na versão mais recente.")
        else:
            print_success("Script atualizado com sucesso!")
            print_info("Recomenda-se reiniciar o script para aplicar as alterações.")
        
        time.sleep(3)

    except FileNotFoundError:
        print_error("O comando 'git' não foi encontrado. A atualização automática não é possível.")
        print_info("Por favor, instale o git com 'sudo apt-get install git'.")
        time.sleep(4)
    except subprocess.CalledProcessError as e:
        print_error("Ocorreu um erro ao tentar atualizar via Git.")
        print_error(f"Detalhes do erro: {e.stderr}")
        time.sleep(5)
    except Exception as e:
        print_error(f"Um erro inesperado ocorreu durante a atualização: {e}")
        time.sleep(3)


def main_menu():
    """
    Exibe o menu principal e gerencia a navegação do usuário.
    Este é o loop principal do programa.
    """
    while True:
        clear_screen()
        print_header("Gerenciador MultiFlow v1.0")
        
        menu_options = {
            "1": "Gerenciar Usuários SSH",
            "2": "Gerenciar BadVPN",
            "3": "Gerenciar Proxy Socks",
            "4": "Gerenciar MultiFlow Proxy",
            "5": "Ferramentas e Otimizações",
            "9": "Atualizar Script",
            "0": "Sair"
        }
        
        print_menu(menu_options)
        choice = get_user_input("Escolha uma opção")

        if choice == "1":
            ssh_manager_main()
        elif choice == "2":
            menu_badvpn_main()
        elif choice == "3":
            menu_proxysocks_main()
        elif choice == "4":
            menu_multiflowproxy_main()
        elif choice == "5":
            tools_menu()
        elif choice == "9":
            update_script()
        elif choice == "0":
            print_success("Saindo do script. Até mais!")
            break
        else:
            print_error("Opção inválida. Por favor, tente novamente.")
            time.sleep(2)


if __name__ == "__main__":
    # Ponto de entrada do script.
    # Verifica se há o argumento --update para uma atualização rápida.
    # Caso contrário, inicia o menu principal.
    check_root()
    
    if "--update" in sys.argv:
        update_script()
    else:
        main_menu()

# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.api import settings
from fabric.contrib.console import confirm
import os

# Configurações para o servidor da FCFRP

username = 'galaxy'
FCFRP_server = '%s@143.107.203.166' % username
project_path = '/home/%s/galaxy/tools/protpred' % username
galaxy_path = '/home/%s/galaxy' % username
	
# Configurações Locais

tool_path = 'galaxy-dist/tools/protpred'
static_path = 'galaxy-dist/static/'

env.hosts = [FCFRP_server]

# ----------------------------------------------------------------------------------------------------

def server():
    """inicia o servidor do Galaxy local"""
    log('Iniciando servidor do Galaxy')
    local('sh galaxy-dist/run.sh --reload')

def update_tool_local(tool_name):
	"""Atualiza tool no diretório do Galaxy"""
	log('Atualizando tool no diretorio do Galaxy')
	if not os.path.exists(tool_path):
		os.mkdir(tool_path)
		warn("Criando o diretório raiz das tools")
	if not os.path.exists(os.path.join(os.getcwd(), ''.join([tool_name, '.xml']))):
		abort("Tool não encontrada.")
	else:
		local('cp %s.py %s.xml %s' % (tool_name, tool_name, tool_path))

def remote_pull():
    """git pull remoto"""
    log('Atualizando aplicação no servidor')
    with cd(project_path):
        run('git pull origin master')

def update_tool_server(tool_name, server=''):
	"""Atualiza tool no diretório do Galaxy no servidor"""
	log('Atualizando tool no diretorio do Galaxy no servidor')
	if not os.path.exists(os.path.join(os.getcwd(), ''.join([tool_name, '.xml']))):
		abort("Tool não encontrada.")
	else:
		local('scp %s.py %s.xml %s:%s' % (tool_name, tool_name, FCFRP_server, project_path))

def update_all_tools_local():
	pass

def reintialize_server(server=''):
	'''Reinitile the remote server'''
	log('Reinitilizing the remote server')
	with settings(warn_only=True):
		if run('screen -R -S "Galaxy" -p 0 -X exec sh %s/run.sh --reload' % galaxy_path).failed:
			log('There is no screen availabe. \nYou must create a new screen.\nAfter that, type CTRL + A + D to deatached it')
			if confirm("Do you want to create a new screen now? "):
				create_remote_screen()
				run('screen -R -S "Galaxy" -p 0 -X exec sh %s/run.sh --reload' % galaxy_path)
			else:
				abort("There is no screen available");

def create_remote_screen():
	'''Create a new screen'''
	log("Creating a new screen.")
	run('screen -R -S "Galaxy"')
	#disconnect_all()

def upload_public_key():
    """faz o upload da chave ssh para o servidor"""
    log('Adicionando chave publica no servidor')
    ssh_file = '~/.ssh/id_rsa.pub'
    target_path = '~/.ssh/uploaded_key.pub'
    put(ssh_file, target_path)
    run('echo `cat ~/.ssh/uploaded_key.pub` >> ~/.ssh/authorized_keys && rm -f ~/.ssh/uploaded_key.pub')

def login():
    local("ssh %s" % prod_server)

def log(message):
    print """
==============================================================
%s
==============================================================
    """ % message

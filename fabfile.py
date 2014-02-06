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
    '''Start the Galaxy local server'''
    log('Starting the Galaxy local server')
    local('sh galaxy-dist/run.sh --reload')

def update_tool_local(tool_name):
	'''Update tool at Galaxy path'''
	log('Updating tool at Galaxy path')
	if not os.path.exists(tool_path):
		os.mkdir(tool_path)
		warn("Creating the tools' root path")
	if not os.path.exists(os.path.join(os.getcwd(), ''.join([tool_name, '.xml']))):
		abort("Tool not found.")
	else:
		local('cp %s.py %s.xml %s' % (tool_name, tool_name, tool_path))

def remote_pull():
    """Execute git pull on server"""
    log('Update server application')
    with cd(project_path):
        run('git pull origin master')

def update_tool_server(tool_name, server=''):
	'''Update Galaxy path tool on server'''
	log('Updating Galaxy path tool on server')
	if not os.path.exists(os.path.join(os.getcwd(), ''.join([tool_name, '.xml']))):
		abort("Tool not found.")
	else:
		local('scp %s.py %s.xml %s:%s' % (tool_name, tool_name, FCFRP_server, project_path))

def update_all_tools_local():
	pass

def reinitialize_server(server=''):
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

def upload_public_key():
    '''Upload the ssh key to server'''
    log('Uploading the ssh public key to server')
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

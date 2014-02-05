#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
import shutil
import subprocess
import os
import smtplib
import mimetypes
from email.Utils import formatdate
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zipfile
import fnmatch
import datetime

user_email = sys.argv[1]
path = sys.argv[2]

path_ae = '/home/leandro/programas/ProtPred-Gromacs/'
_config = path + 'configuracao.conf'
_command = path_ae + 'src/protpred-Gromacs-Mono'

tipo_pop = sys.argv[5]

def GetPDBResultante(configuracao):
	try:
		stdout_file = open(path + "stdout_nerf.txt", "wr")
		_prog = path_ae + 'src/protpred-Gromacs_Nerf_Population'
		for line in file(configuracao, "r"):
			linha = line.split("=")
			linha[0] = linha[0].strip()
			if linha[0] == 'NumberGeration':
				NumberGeration = linha[1].strip()
		arquivo_pop = 'pop_' + NumberGeration + '.pop'
		retProcess = subprocess.Popen([_prog, configuracao, arquivo_pop],stdout=stdout_file,stderr=subprocess.STDOUT,shell=False)
		retProcess.wait()  		

		stdout_file.write("acabou o nerf...");
		#stdout_file.close()
		_prog = path_ae + 'src/protpred-Gromacs-RMSD'
		stdout_file_rmsd = open(path + "stdout_rmsd.txt", "wr")
		retProcess = subprocess.Popen([_prog, configuracao],stdout=stdout_file_rmsd,stderr=subprocess.STDOUT,shell=False)
		retProcess.wait()
		for rmsd in file(path + "protpred-Gromacs.rmsd", "r"):
			linha = rmsd.split()
			linha[0] = linha[0].strip()
			if not linha[0] == ';':
				pdb_resultante = linha[0].strip()
		renomeia = 'sudo cp ' + pdb_resultante + ' Final_PDB.pdb'
		os.system(renomeia)
		#return pdb_resultante
	except Exception as e:
		stdout_file.write("Erro ao encontrar pdb resultante")
		#stdout_file.write(e)
		stdout_file.close

def GeraPopulacaoInicial(tipo, configuracao):   
    try:       
      if tipo == '0': #gera aleatoria
        _prog = path_ae + 'src/protpred-Gromacs_pop_initial'
        stdout_file = open(path + "stdout_pop.txt", "wr")
        retProcess = subprocess.Popen([_prog, configuracao],stdout=stdout_file,stderr=subprocess.STDOUT,shell=False)       
        retProcess.wait()        
      else:
	stdout_file = open(path + "stdout_pop.txt", "wr")
        input_pop = sys.argv[18]			
        arq_pop = open(path + "pop_initial.txt", "wr")
        for line in file(input_pop, "r"):
            arq_pop.write(line)		  
    except Exception as e:
	stdout_file.write("Erro ao iniciar a populacao")
	#stdout_file.write(e)
	stdout_file.close


def envia_email(de, para, assunto, mensagem, arquivos, servidor):
	# Cria o objeto da mensagem
   	msg = MIMEMultipart()
   	# Define o cabeçalho
   	msg['From'] = de
   	msg['To'] = para
  	msg['Date'] = formatdate(localtime=True)
   	msg['Subject'] = assunto

   	# Atacha o texto da mensagem
  	msg.attach(MIMEText(mensagem))

   	# Atacha os arquivos
   	for arquivo in arquivos:
      		parte = MIMEBase('application', 'octet-stream')
      		parte.set_payload(open(arquivo, 'rb').read())
      		encoders.encode_base64(parte)
      		parte.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(arquivo))
      		msg.attach(parte)

   	# Conecta ao servidor SMTP
   	smtp = smtplib.SMTP(servidor, 587)
   	smtp.ehlo()
   	smtp.starttls()
   	smtp.ehlo()
	# Faz login no servidor
	smtp.login('endereco_email', 'senha_email')
	# Envia o e-mail
	smtp.sendmail(de, para, msg.as_string())
	# Desconecta do servidor
	smtp.close()


def execute(ShowError=True):
	print _command
	stdout_file = open(path + "stdout.txt", "wr")
	retProcess = subprocess.Popen([_command, _config],stdout=stdout_file,stderr=subprocess.STDOUT,shell=False)
	retProcess.wait()	

GeraPopulacaoInicial(tipo_pop, _config)

execute(True)

GetPDBResultante(_config)

def listDirectory(directory, extension):     
    try:  
       ereg = 'PROT_IND_FINAL_*.pdb'                                 
       fileList = [os.path.normcase(f)
                    for f in os.listdir(directory)]             
       fileList = [os.path.join(directory, f)
                    for f in fileList
                      if fnmatch.fnmatch(f, ereg)]
       return fileList	
    except Exception as e:
       zip_file = open(path + "stdout_zip.txt", "wr") 
       zip_file.write("Erro ao listar os arquivos para compactar")
       zip_file.write(e)
       zip_file.close
	
listaArquivos = listDirectory(path, '.pdb')

outfile = path + "ArquivosResultados.zip"
z = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED)

for arq in listaArquivos:
   z = zipfile.ZipFile(outfile, 'a', zipfile.ZIP_DEFLATED)
   z.write(arq)
   z.close()

z = zipfile.ZipFile(outfile, 'a', zipfile.ZIP_DEFLATED)
z.write(path+'Final_PDB.pdb')
z.close()

resultado = path + 'ArquivosResultados.zip'

path_output = sys.argv[3]
file_output = sys.argv[4]
dest = path_output + "/" + file_output
copia = "sudo cp " + resultado + " " + dest
os.system(copia)

#pdb_result = GetPDBResultante(_config)
#pdb_result = path + pdb_result


#renomeia = "sudo cp " + pdb_result + " " + path + "PDB_Final.pdb"
#os.system(renomeia)

now = datetime.datetime.now()
tupla = now.timetuple()
data = str(tupla[2]) + '/' + str(tupla[1]) + '/' + str(tupla[0]) + ' ' + str(tupla[3]) + ':' + str(tupla[4]) + ':' + str(tupla[5])

assunto_email = '''Hi, 

Your simulation has been conclued at ''' + data + '''. 

The Final PDB file is named as: 'Final_PDB.pdb'.

You have to go to your History and download it.

Best Regards.

2PG Tool '''

envia_email('adefelicibus@gmail.com', user_email, '2PG Execution on Galaxy', assunto_email, [], 'smtp.gmail.com')


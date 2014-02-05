#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, string
import shutil
import subprocess
import os, stat
import smtplib
import mimetypes
import re
from email.Utils import formatdate
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import zipfile
import fnmatch


path = '/home/galaxy/execute/'
path_ae = '/home/leandro/programas/ProtPred-Gromacs/'	
_command = path_ae + 'src/protpred-Gromacs-Mono'

def stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()

email = sys.argv[15]
email = email.replace('__at__', '@')

if not(re.match('(.+)@(.+)\.(.+)',email,re.IGNORECASE)):
    stop_err("Invalid email adress. Please, insert a valid email adress.")

user_email = sys.argv[16]
tipo_input = sys.argv[17]
tipo_pop = sys.argv[18]

#def execute(caminho, caminho_output, arquivo_output, populacao):
#	retProcess = subprocess.Popen(['nohup',_command, email, caminho, caminho_output, arquivo_output, populacao, '&'],0,None,None,None,False)

def execute(exec_path):
        #print _command
        stdout_file = open(exec_path + "stdout.txt", "wr")
        retProcess = subprocess.Popen([_command, _config],stdout=stdout_file,stderr=subprocess.STDOUT,shell=False)
        retProcess.wait()

def CriaDiretorioExecucao():
	now = datetime.datetime.now()
	tupla = now.timetuple()
	try:				#dia		#mes		#ano			#hora		#min		#seg
	  nome_diretorio = email + str(tupla[2]) + str(tupla[1]) + str(tupla[0]) + "_" + str(tupla[3]) + str(tupla[4]) + str(tupla[5]) + "/"
	  os.mkdir(os.path.join(path,nome_diretorio))
	  os.chmod(os.path.join(path,nome_diretorio), stat.S_IRWXU)
	  return nome_diretorio						    
	except Exception, e:
 	  stop_err("Error while creating the execution directory!\n%s" % e)

def CopiaArquivosNecessarios():
	novo_diretorio = path + dir_execucao	
	try:
	  os.chdir(novo_diretorio)
	  fileList = [os.path.normcase(f)
             for f in os.listdir(path)]             
          fileList = [os.path.join(path, f)
             for f in fileList]
	  for arquivo in fileList:
	     if not os.path.isdir(arquivo):	
	       shutil.copy(arquivo, novo_diretorio)
	except Exception, e:
	  stop_err("Error while copying the necessary files!\n%s" % e)

def CriaArquivoConfiguracao():
        try:
	    novo_diretorio = path + dir_execucao
	    arq = file(novo_diretorio + 'configuracao.conf', "wr")

	    arq.write('gromacs_energy_min = none' +'\n')
	    arq.write('gromacs_energy_min_gen_oper = none' +'\n')	
            arq.write('rotamer_library = none' + '\n')
	    arq.write('NumberObjective = 1' +'\n')	
 	    arq.write('ArqFimMulti = ' + novo_diretorio + 'arqFim_1VII.txt' +'\n')
	    arq.write('NumberGeration = ' + sys.argv[1] +'\n')
	    arq.write('SizePopulation = ' + sys.argv[2] +'\n')
	    arq.write('NumberIndividualReproduce = ' + sys.argv[3] +'\n')
	    arq.write('CrossoverRate = ' + sys.argv[4] +'\n')
	    arq.write('MutationRate = ' + sys.argv[5] +'\n')
	    arq.write('Individual_Mutation_Rate = ' + sys.argv[6] +'\n')
	    arq.write('blx_alfa = ' + sys.argv[7] +'\n')
	    arq.write('max_mutation_range = ' + sys.argv[8] +'\n')
	    arq.write('BLX_cros_Rate = ' + sys.argv[9] +'\n')
	    arq.write('1_point_cros_Rate = ' + sys.argv[10] +'\n')
	    arq.write('NativeProtein = ' + novo_diretorio + '1VII.pdb' +'\n')	
	    arq.write('SequenceAminoAcidsPathFileName = ' + novo_diretorio + 'none.fasta.txt' +'\n')
	    arq.write('StoreFitnessResultsPathFileName = ' + novo_diretorio + 'result_1VII.txt' +'\n')
	    arq.write('PDBBestIndividualPathFileName = ' + 'prot_1VII.pdb' +'\n')
	    arq.write('FinalPopulationPathFileName = ' + novo_diretorio + 'saida_1VII.txt' +'\n')
	    arq.write('NameExecutation = 1VII' + '\n')  
	    arq.write('Local_Execute = ' + novo_diretorio  + '\n')
	    arq.write('Database = ' + path_ae + 'Database/' +'\n')
	    arq.write('ComputeEnergyProgram = ' + path_ae + 'scripts/compute_energy/run_gromacs_compute_energy.sh' +'\n')
	    arq.write('MinimizationProgram = ' + path_ae + 'scripts/compute_energy/run_gromacs_energy_minimization.sh' +'\n')
	    arq.write('CleanGromacsSimulation = ' + path_ae + 'scripts/compute_energy/clean_simulation.sh' +'\n')
	    arq.write('GetEnergyProgram = ' + path_ae + 'scripts/compute_energy/run_g_energy.sh' +'\n')
	    arq.write('TopologyFile = ' + 'topol_ProtPred.top' +'\n')
	    arq.write('IniPopFileName = ' + 'pop_initial.txt' +'\n')
	    arq.write('z_matrix_fileName = ' + 'z_matrix_1VII.z' +'\n')
	    arq.write('Path_Gromacs_Programs = /usr/local/gromacs/bin/' +'\n')
	    arq.write('Computed_Energies_Gromacs_File = ' + 'file_energy_computed.ener.edr' +'\n')
	    arq.write('Energy_File_xvg = ' + 'energy.xvg' +'\n')
	    arq.write('Program_Read_Energy = ' + path_ae + 'scripts/compute_energy/run_read_energy.sh' +'\n')
	    arq.write('Computed_Energy_Value_File = ' + 'energy_computed.txt' +'\n')
	    arq.write('Fitness_Energy = ' + sys.argv[11] +'\n')
	    arq.write('Weights_Fitness = ' + sys.argv[12] +'\n')
	    arq.write('Program_Run_RMSD = ' + path_ae + 'scripts/compute_rmsd/run_g_rms.sh' +'\n')
 	    arq.write('Program_Run_g_sas = ' + path_ae + 'scripts/sas/run_g_sas.sh' +'\n')
	    arq.write('GetAreasFrom_g_sas = ' + path_ae + 'scripts/sas/run_read_areas.sh' +'\n')
	    arq.write('Computed_Areas_g_sas_File = ' + 'file_g_sas_areas.xvg' +'\n')
	    arq.write('Program_Run_g_gyrate = ' + path_ae + 'scripts/gyrate/run_g_gyrate.sh' +'\n')
	    arq.write('GetRadiusFrom_g_gyrate = ' + path_ae + 'scripts/gyrate/run_read_gyrate.sh' +'\n')
	    arq.write('Computed_Radius_g_gyrate_File = ' + 'file_g_gyrate_radius.xvg' +'\n')
	    arq.write('Program_Run_g_hbond = ' + path_ae + 'scripts/h_bond/run_g_hbond.sh' +'\n')
	    arq.write('GetValueFrom_g_hbond = ' + path_ae + 'scripts/h_bond/run_read_hbond.sh' +'\n')
	    arq.write('Computed_g_hbond_File = ' + 'file_g_hbond.xvg' +'\n')        
	    arq.close
        except Exception, e:
            stop_err("Error while creating the configuration file.\n%s" % e)    

def GeraPopulacaoInicial(tipo, configuracao, path_exec):
    try:
      if tipo == '0': #gera aleatoria
        _prog = path_ae + 'src/protpred-Gromacs_pop_initial'
        stdout_file = open(path_exec + "stdout_pop.txt", "wr")
        retProcess = subprocess.Popen([_prog, configuracao],stdout=stdout_file,stderr=subprocess.STDOUT,shell=False)
        retProcess.wait()
      else:
        stdout_file = open(path_exec + "stdout_pop.txt", "wr")
        input_pop = sys.argv[19]
        arq_pop = open(path_exec + "pop_initial.txt", "wr")
        for line in file(input_pop, "r"):
            arq_pop.write(line)
    except Exception, e:
        stdout_file.write("Erro ao iniciar a populacao:\n %s" % e)
        stdout_file.close
        stop_err("Error to create the initial population.\n %s" % e)


def envia_email(de, para, assunto, mensagem, arquivos, servidor):

        try:
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
            smtp = smtplib.SMTP(servidor,587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            # Faz login no servidor
            smtp.login('adefelicibus@gmail.com', 'mami1752')
	    try:
                # Envia o e-mail
                smtp.sendmail(de, para, msg.as_string())
            finally:
                # Desconecta do servidor
                smtp.close()
        except Exception, exc:
            sys.exit("Mail failed: %s" % str(exc) )


dir_execucao = CriaDiretorioExecucao()

new_path = path + dir_execucao

_config = new_path + 'configuracao.conf'

CriaArquivoConfiguracao()

CopiaArquivosNecessarios()

try:
    if tipo_input == '0':
        input_sequence = sys.argv[13]
    elif tipo_input == '1':
        input_filename = sys.argv[13]
    arq_fasta = open(new_path + "none.fasta.txt", "wr")
    if tipo_input == '0':
        arq_fasta.write("none:A|PDBID|CHAIN|SEQUENCE"+'\n')
        arq_fasta.write(input_sequence)
    elif tipo_input == '1':
        for line in file(input_filename, "r"):
            arq_fasta.write(line)
except Exception, e:
    stop_err("Error: %s\n" % e)

arq_fasta.close()

data = formatdate(localtime=True)

path_output, file_output = os.path.split(sys.argv[14])

GeraPopulacaoInicial(tipo_pop, _config, new_path)

execute(new_path)

def listDirectory(directory, extension):
    try:
       ereg = 'PROT_IND_FINAL*.pdb'
       fileList = [os.path.normcase(f)
                    for f in os.listdir(directory)]
       fileList = [os.path.normcase(f)
                    for f in fileList
                      if fnmatch.fnmatch(f, ereg)]
       return fileList
    except Exception, e:
       stop_err("Error while compacting the result files: %s\n" % e)
      # zip_file = open(directory + "stdout_zip.txt", "wr")
      # zip_file.write("Erro ao listar os arquivos para compactar")
      # zip_file.write(e)
      # zip_file.close

listaArquivos = listDirectory(new_path, '.pdb')

outfile = new_path + "ResultFiles2PG.zip"
z = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED)

for arq in listaArquivos:
   z = zipfile.ZipFile(outfile, 'a', zipfile.ZIP_DEFLATED)
   z.write(arq)
   z.close()

resultado = new_path + 'ResultFiles2PG.zip'

dest = path_output + "/" + file_output
copia = "cp " + resultado + " " + dest
os.system(copia)

now = datetime.datetime.now()
tupla = now.timetuple()
data = str(tupla[2]) + '/' + str(tupla[1]) + '/' + str(tupla[0]) + ' ' + str(tupla[3]) + ':' + str(tupla[4]) + ':' + str(tupla[5])

assunto_email = '''Hi, 

Your simulation has been conclued at ''' + data + '''. 

You have to go to your History and download it.

Best Regards.

2PG Tool '''

envia_email('adefelicibus@gmail.com', email, '2PG Execution on Galaxy', assunto_email, [], 'smtp.gmail.com')


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

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

path = '/home/galaxy/execute/'
path_ae = '/home/leandro/programas/ProtPred-Gromacs/'	
_command = '/home/galaxy/galaxy/tools/protpred/executa_3pg.py'	

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

#param = sys.argv

fe = string.split(sys.argv[11].rstrip(),',')

def execute(caminho, caminho_output, arquivo_output, populacao):
	retProcess = subprocess.Popen(['nohup',_command, email, caminho, caminho_output, arquivo_output, populacao, '&'],0,None,None,None,False)

def CriaDiretorioExecucao():
	now = datetime.datetime.now()
	tupla = now.timetuple()
	try:				#dia		#mes		#ano			#hora		#min		#seg
	  nome_diretorio = email + str(tupla[2]) + str(tupla[1]) + str(tupla[0]) + "_" + str(tupla[3]) + str(tupla[4]) + str(tupla[5]) + "/"
	  #os.mkdir(path + nome_diretorio)
	  os.mkdir(os.path.join(path,nome_diretorio))
	  os.chmod(os.path.join(path,nome_diretorio), stat.S_IRWXU) #S_IRWXU - Gives RWX permissions for user
	  return nome_diretorio						    
	except Exception as e:
 	  stop_err("Error while creating the execution directory!\n%s",e)   

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
	except Exception as e:
            stop_err("Error while copying the necessary files!\n%s",e)

def CriaArquivoConfiguracao():
        try:
            novo_diretorio = path + dir_execucao
	    arq = file(novo_diretorio + 'configuracao.conf', "wr")

	    arq.write('gromacs_energy_min = none' +'\n')
	    arq.write('gromacs_energy_min_gen_oper = none' +'\n')
	    arq.write('rotamer_library = cad_tuffery' + '\n')
 	    No = len(fe)
	    arq.write('NumberObjective = ' + str(No) + '\n') 
	    arq.write('ArqFimMulti = ' + novo_diretorio + 'arqFim_1VII.txt' +'\n')
 	    arq.write('NumberGeration = ' + sys.argv[1] +'\n')
	    arq.write('SizePopulation = ' + sys.argv[2] +'\n')
	    arq.write('number_archive = 3' + '\n')
	    arq.write('NumberIndividualReproduce = ' + sys.argv[3] +'\n')
	    arq.write('CrossoverRate = ' + sys.argv[4] +'\n')
	    arq.write('MutationRate = ' + sys.argv[5] +'\n')
	    arq.write('Individual_Mutation_Rate = ' + sys.argv[6] +'\n')
	    arq.write('blx_alfa = ' + sys.argv[7] +'\n')
	    arq.write('max_mutation_range = ' + sys.argv[8] +'\n')
	    arq.write('BLX_cros_Rate = ' + sys.argv[9] +'\n')
	    arq.write('1_point_cros_Rate = ' + sys.argv[10] +'\n')
	    arq.write('2_point_cros_Rate = 0.5' + '\n') 
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

	    fit = ''
	    wf = ''
	    for obj in fe:
                fit += '%s, ' % obj
                wf += '1.0, '
            fit = fit.strip(', ')
            wf = wf.strip(', ')

            arq.write('Fitness_Energy = ' + fit +'\n')       	
            arq.write('Weights_Fitness = ' + wf + '\n')
	    arq.write('Program_Run_RMSD = ' + path_ae + '/scripts/compute_rmsd/run_g_rms.sh' + '\n')
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
        except Exception as e:
            stop_err("Error while creating the configuration file.\n%s", e)

if fe[0] == 'None':
	sys.stderr.write('Please, use checkboxes to specify the objectives.\n')
	sys.exit()

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
    output_fasta_file = sys.argv[14]
    output_fasta = open(output_fasta_file, 'wr' )
    arq_fasta = open(new_path + "none.fasta.txt", "wr")
    if tipo_input == '0':
        arq_fasta.write("none:A|PDBID|CHAIN|SEQUENCE"+'\n')
        arq_fasta.write(input_sequence)
        output_fasta.write("none:A|PDBID|CHAIN|SEQUENCE"+'\n')
        output_fasta.write(input_sequence)
    elif tipo_input == '1':
        for line in file(input_filename, "r"):
            arq_fasta.write(line)
            output_fasta.write(line)
except Exception as e:
    stop_err("%s\n", e)

output_fasta.close()
arq_fasta.close()

data = formatdate(localtime=True)

path_output, file_output = os.path.split(output_fasta_file)

execute(new_path, path_output, file_output, tipo_pop) 

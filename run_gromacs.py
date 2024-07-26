import subprocess
import os

def find_file_with_extension(extension):
	"""Encontre o primeiro arquivo no diretório atual com a extensão fornecida."""
	for file in os.listdir('.'):
		if file.endswith(extension):
			return file
	return None
    
def run_command(command):
	"""Executa um comando no terminal e printa o output."""
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	if process.returncode != 0:
		print(f"Error running command: {command}")
		print(f"Error message: {stderr.decode('utf-8')}")
	else:
		print(stdout.decode('utf-8'))

def run_command_input(comando, input_text=None):
	"""Executa um comando no terminal com input de valores"""
	processo = subprocess.Popen(comando, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	if input_text:
		processo.communicate(input=input_text)
	else:
		processo.communicate()
	return processo

def run_command_background(comando, input_text=None, background=False):
	"""Executa um comando no terminal em segundo plano, para abrir arquivos em outros programas"""
	if background:
		processo = subprocess.Popen(comando, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	else:
		processo = subprocess.Popen(comando, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		if input_text:
			processo.communicate(input=input_text)
		else:
			processo.communicate()
	return processo
	
def identify_file():
	'''Identifica os arquivos no diretório de trabalho'''
	# Encontra os arquivos necessários
	protein_file = find_file_with_extension('.pdb')
	if not protein_file:
		print("No .pdb file found in the current directory.")
		return None, None
    
	mdp_file = find_file_with_extension('.mdp')
	if not mdp_file:
		print("No .mdp file found in the current directory.")
		return None, None
    
	# Remove a extensão do nome do arquivo de proteína
	protein_name = os.path.splitext(protein_file)[0]

	return protein_file, protein_name
	

def remove_HOH():
	'''Remove os cristais de água da estrutura'''
	protein_file, protein_name = identify_file()
	if protein_file and protein_name:
		# Remove os cristais de água
		run_command(f"grep -v HOH {protein_file} > {protein_name}_clean.pdb")
	else:
		print("Failed to identify necessary files for removing HOH.")
	
	#muda o nome da proteína para proteína_clean	
	protein_name = protein_name + "_clean"

def main():
	
	protein_file, protein_name = identify_file()
	
	#
	# Etapa 1: preparar o sistema (por exemplo, editconf, solvate, genion)
	#
	
	# Escolher o campo de força
	print ("""
Select o campo de força:

 1: AMBER03 protein, nucleic AMBER94 (Duan et al., J. Comp. Chem. 24, 1999-2012, 2003)
 2: AMBER94 force field (Cornell et al., JACS 117, 5179-5197, 1995)
 3: AMBER96 protein, nucleic AMBER94 (Kollman et al., Acc. Chem. Res. 29, 461-469, 1996)
 4: AMBER99 protein, nucleic AMBER94 (Wang et al., J. Comp. Chem. 21, 1049-1074, 2000)
 5: AMBER99SB protein, nucleic AMBER94 (Hornak et al., Proteins 65, 712-725, 2006)
 6: AMBER99SB-ILDN protein, nucleic AMBER94 (Lindorff-Larsen et al., Proteins 78, 1950-58, 2010)
 7: AMBERGS force field (Garcia & Sanbonmatsu, PNAS 99, 2782-2787, 2002)
 8: CHARMM27 all-atom force field (CHARM22 plus CMAP for proteins)
 9: GROMOS96 43a1 force field
10: GROMOS96 43a2 force field (improved alkane dihedrals)
11: GROMOS96 45a3 force field (Schuler JCC 2001 22 1205)
12: GROMOS96 53a5 force field (JCC 2004 vol 25 pag 1656)
13: GROMOS96 53a6 force field (JCC 2004 vol 25 pag 1656)
14: GROMOS96 54a7 force field (Eur. Biophys. J. (2011), 40,, 843-856, DOI: 10.1007/s00249-011-0700-9)
15: OPLS-AA/L all-atom force field (2001 aminoacid dihedrals)

Selecione o campo:
""")
	
	# Gera a topologia
	run_command(f"gmx pdb2gmx -f {protein_name}.pdb -o {protein_name}_processed.gro -water spce")
	# Define uma caixa
	run_command(f"gmx editconf -f {protein_name}_processed.gro -o {protein_name}_newbox.gro -c -d 1.0 -bt cubic")
	# Adiciona solvente
	run_command(f"gmx solvate -cp {protein_name}_newbox.gro -cs spc216.gro -o {protein_name}_solv.gro -p topol.top")
	# Adiciona Ions
	run_command(f"gmx grompp -f ions.mdp -c {protein_name}_solv.gro -p topol.top -o ions.tpr")
    
	print ("""
Selecione um grupo contínuo de moléculas de solvente

Group 0 (System) has 33892 elements
Group 1 (Protein) has 1960 elements
Group 2 (Protein-H) has 1001 elements
Group 3 (C-alpha) has 129 elements
Group 4 (Backbone) has 387 elements
Group 5 (MainChain) has 517 elements
Group 6 (MainChain+Cb) has 634 elements
Group 7 (MainChain+H) has 646 elements
Group 8 (SideChain) has 1314 elements
Group 9 (SideChain-H) has 484 elements
Group 10 (Prot-Masses) has 1960 elements
Group 11 (non-Protein) has 31932 elements
Group 12 (Water) has 31932 elements
Group 13 (SOL) has 31932 elements
Group 14 (non-Water) has 1960 elements

Selecione um grupo:
""")
	# Agora temos uma descrição em nível atômico do nosso sistema no arquivo binário ions.tpr. Passaremos este arquivo para o genion:
	run_command(f"gmx genion -s ions.tpr -o {protein_name}_solv_ions.gro -p topol.top -pname NA -nname CL -neutral")
    
	#
	# Etapa 2: Minimização de energia
	#
	
	run_command(f"gmx grompp -f minim.mdp -c {protein_name}_solv_ions.gro -p topol.top -o em.tpr")
	
	print ("Rodando energia de minimização", end='', flush=True)
	# realiza a miniminização
	run_command(f"gmx mdrun -v -deffnm em")
	
	# Gera gráfico de energia
	run_command_input(f"gmx energy -f em.edr -o potential.xvg", input_text="10 0\n")
	# Roda gráfico no xmgrace
	run_command_background(f"xmgrace potential.xvg", background=True)
    
    #
	# Etapa 3: Equilibração (NVT)
	#
	
	run_command(f"gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr")

	print ("Rodando equilibração de temperatura", end='', flush=True)
    # realiza a equilibração
	run_command(f"gmx mdrun -deffnm nvt")
    
    # Gera gráfico de temperatura
	run_command_input(f"gmx energy -f nvt.edr -o temperature.xvg", input_text="16 0\n")
	# Roda gráfico no xmgrace
	run_command_background(f"xmgrace temperature.xvg", background=True)
	
    #
	# Etapa 4: Equilibração (NPT)
	#
	
	run_command(f"gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr")
    
	print ("Rodando equilibração de pressão", end='', flush=True)
    # realiza a equilibração
	run_command(f"gmx mdrun -deffnm npt")
    
    # Gera gráfico de pressão
	run_command_input(f"gmx energy -f npt.edr -o pressure.xvg", input_text="18 0\n")
	# Roda gráfico no xmgrace
	run_command_background(f"xmgrace pressure.xvg", background=True)
	# Gera gráfico de densidade
	run_command_input(f"gmx energy -f npt.edr -o density.xvg", input_text="24 0\n")
	# Roda gráfico no xmgrace
	run_command_background(f"xmgrace density.xvg", background=True)
    

if __name__ == "__main__":
	print ("""
Para garantir a correta execução do programa, siga estas etapas:

1. Verifique se o arquivo da proteína no formato .pdb foi adicionado ao diretório de trabalho.
2. Assegure-se de que todos os arquivos de parâmetros de simulação (.mdp) estejam presentes no mesmo diretório.
3. Certifique-se de que o software xmgrace esteja instalado, pois ele é necessário para a visualização e leitura dos gráficos gerados.

""")
	need_removal = input("Gostaria de remover os cristais de água da estrutura? (Y/n): ")
	if need_removal == "Y" or need_removal == "y":
		remove_HOH()
	main()

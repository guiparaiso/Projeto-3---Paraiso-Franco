#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
import binascii
import logging
import logging.handlers

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def setup_logger(name, log_file, level=logging.INFO):
    """Função para configurar e retornar um logger."""
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger_imagem1 = setup_logger('logger_imagem1', 'comunicacao_imagem1.log')
logger_imagem2 = setup_logger('logger_imagem2', 'comunicacao_imagem2.log')


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()
        
        img1 = "img1.jpeg"
        img2 = "img2.jpeg"
        list_imgs = [open(img1,'rb').read(), open(img2,'rb').read()]
        eop = b'\xAA\xBB\xCC\xDD'
        
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        print("-------------------------")
        br = False
        for img in list_imgs:
            # print("enviando imagens {}" .format(img)
            if br:
                break
            x= int(len(img)/140)

            if img == list_imgs[0]:
                nmbr = 1
                logger_imagem1.info(f'Enviando imagem 1')
            else:
                nmbr=2
                logger_imagem2.info(f'Enviando imagem 2')

            for i in range(x+1):
                if i != x:
                    sending_bytes = img[i*140:(i+1)*140]
                else:
                    sending_bytes = img[i*140:]
                pct_waiting = int.to_bytes(x-i, length=1, byteorder='big')
                tamanho = int.to_bytes(len(sending_bytes), length=1, byteorder='big')
                pct_sent = int.to_bytes(i+1, length=1, byteorder='big')
                protocol = b'\x01' + b'\x00' + b'\x00' + tamanho + b'\x00'  + pct_sent + pct_waiting  +  b'\x00' + b'\x00' + b'\x00'
                txBuffer = protocol + sending_bytes + eop
                com1.sendData(txBuffer)
                time.sleep(1)
                print("Da imagem {}, mandei : {} e falta mandar {} pacotes, cada pacote  com : {} bytes" .format(nmbr,txBuffer[5],txBuffer[6],txBuffer[3]))
                print("-------------------------")
                y = time.time()
                s = 0
                while time.time() - y < 10 and com1.rx.getIsEmpty():
                    if s == 0:
                        print("esperando resposta")
                        print("-------------------------")
                        s=1
                if com1.rx.getIsEmpty():
                    print('Time out')
                    br = True
                    break
                rxBuffer, nRx = com1.getData(com1.rx.getBufferLen())
                print(" RxBuffer : {}".format(rxBuffer))
                ss=0
                y = time.time()
                while time.time() - y < 10 and rxBuffer != b'\x00':
                    if not com1.rx.getIsEmpty():
                        if rxBuffer[4] == 0:
                            print("------------------------- \n ENTROU \n-------------------------")
                            if img == list_imgs[0]:
                                msg = f'Pacote numero {i+1} da imagem 1 enviado com problema '
                                logger_imagem1.info(msg)
                                print(msg)
                            else:
                                msg = f'Pacote numero {i+1} da imagem 2 enviado com problema'
                                logger_imagem2.info(msg)
                                print(msg)
                            print("Reenviando {} pacote" .format(rxBuffer[5]))
                            protocol = b'\x01' + b'\x00' + b'\x00' + tamanho + b'\x00'  + rxBuffer[5].to_bytes(1,byteorder='big') + pct_waiting  +  b'\x00' + b'\x00' + b'\x00'
                            txBuffer = protocol + img[rxBuffer[5]*140:(rxBuffer[5]+1)*140]+ eop
                            com1.sendData(txBuffer)
                            time.sleep(1)
                        rxBuffer, nRx = com1.getData(com1.rx.getBufferLen())
            
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
            
        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

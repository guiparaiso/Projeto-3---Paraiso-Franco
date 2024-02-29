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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        
    
        com1.enable()
        print("Abriu a comunicação")
  
        comandos = []
        quantidade = 0

        #com1.rx.clearBuffer()

        while True:
            
            time.sleep(0.08)
            rxBuffer, nRx = com1.getData(com1.rx.getBufferLen())
            if rxBuffer == b'acabou':
                break
            if rxBuffer != b'':
                quantidade += 1
                comandos.append(rxBuffer)

                #print(rxBuffer)
        
        print(f'quantidade {quantidade}')
        if comandos[0] == b'\xf0\xf0':
            print('entrei no zero 1')
            print(comandos[0])
            comandos.pop(0)
            print('após')
            print(comandos[0])
        
        if comandos[0] == b'00':
            print('entrei no zero zero')
            print(comandos[0])
            comandos.pop(0)
            print('após')
            print(comandos[0])
        
        print(f'quantidade {quantidade}')
        
        print('número de comandos enviados: {}'.format(len(comandos)))
        print(len(comandos))
        print(comandos)
        # for i in range(len(comandos)):
        #     print('comando {}: {}'.format(i+1, comandos[i]))
        numero = str(len(comandos)+1)
        com1.sendData(numero.encode('utf-8'))

    
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

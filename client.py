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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.5)
        com1.sendData(b'00')
        time.sleep(0.5)
        
        
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        comando1 = b'\x00\x00\x00\x00'
        comando2 = b'\x00\x00\xFF\x00'
        comando3 = b'\xFF\x00\x00'
        comando4 = b'\x00\xFF\x00'
        comando5 = b'\x00\x00\xFF'
        comando6 = b'\x00\xFF'
        comando7=b'\xFF\x00'
        comando8 = b'\x00'
        comando9 = b'\xFF'
        comandos = [comando1, comando2, comando3, comando4, comando5, comando6, comando7, comando8, comando9]
        comandos_nomes= ['comando1', 'comando2', 'comando3', 'comando4', 'comando5', 'comando6', 'comando7', 'comando8', 'comando9']
        quant_comandos = random.randint(10,30)
        # quant_comandos = 30
        qt = quant_comandos
        print("Quantidade de comandos a serem enviados: {}" .format(quant_comandos))
        comando_copy = comandos.copy()
        l_enviada = []
        while quant_comandos > 0:
            comando = random.choice(comando_copy)
            comando_copy.remove(comando)
            if len(comando_copy) == 0:
                comando_copy = comandos.copy()
            txBuffer = comando
            l_enviada.append(comandos.index(comando))
    
            #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        
        
            #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
            #faça um print para avisar que a transmissão vai começar.
            #tente entender como o método send funciona!
            #Cuidado! Apenas trasmita arrays de bytes!
                
            
            com1.sendData(bytearray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            
            print("enviando {} dos bytes : {}" .format(comandos_nomes[comandos.index(comando)],txBuffer))
            
            # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
            # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
            
            
            
            
            #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
            #Observe o que faz a rotina dentro do thread RX
            #print um aviso de que a recepção vai começar.
            
            #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
            #Veja o que faz a funcao do enlaceRX  getBufferLen
            quant_comandos -= 1
            time.sleep(.5)
        com1.sendData(b"acabou")
        time.sleep(1.5)
        #acesso aos bytes recebidos
        print("o numero de comandos enviados foi: {}" .format(len(l_enviada)))
        print("recebendo dados .... ")
        bol = True
        x = time.time()
        while time.time() - x < 5 :
            if bol:
                print("esperando resposta")
                bol = False
    
        if com1.rx.getBufferLen() > 0:
            rxBufferr,nRx = com1.getData(com1.rx.getBufferLen())
            print("recebeu {}" .format(rxBufferr))
            print("a quantidade recebida é: {} e a enviada é : {}" .format(rxBufferr.decode(), qt ))
            if rxBufferr.decode() == str(qt):
                print("recebeu a quantidade de comandos correta")
            else:
                
                print("recebeu a quantidade de comandos errada")
            
        else:
            print('Time out')
            
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

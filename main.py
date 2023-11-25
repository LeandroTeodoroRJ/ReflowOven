#*************************************************************************************************
#                PROGRAMA DE CONTROLE DO FORNO DE REFLOW PARA COMPONENTES SMD
#*************************************************************************************************
'''
Informações Gerais:
Placa: Raspberry Pi 3 Model B+
OS: Raspbian versão 10
Python versão 3.7.3

'''
#*************************************************************************************************
#INCLUDES
from tkinter import*                   #Importa a biblioteca gráfica
#from tkinter.ttk import*
import spidev                          #Biblioteca de controle da interface SPI
import time                            #Para delay de tempo
import matplotlib.pyplot as plt        #Biblioteca para geração de gráficos
from numpy import arange               #Para geração de matriz numérica
from threading import Timer            #Para processo paralelo de interrupção por tempo
import RPi.GPIO as GPIO   #Módulo de controle das portas GPIO
import _thread
from tecladonumerico import TecladoNumerico as NumKey

#*************************************************************************************************
#CONSTANTES E DEFINIÇÕES
resolucao = '800x600+0+0'
time_sample = 0.4            #Tempo em segundos entre as amostras de temperatura

#*************************************************************************************************
#VARIÁVEIS DO SISTEMA
flag_interrupcao = True     #Se falso fecha as threads paralelas
tempo = []                  #Tempos das aquisições de dados
valor_temp = []             #Valores de temperatura
cont = 0                    #Contador de posição de amostra

#Módulo de potência
DIM = 21         #Saída de ativação para o triac. GPIO29 - pino 40 - BCM 21
ZC = 20          #Detector de cruzamento em zero. GPIO28 - Pino 38 - BCM 20
DELAY_TIME = 0.002      #Tempo para disparar o triac
PULSE_TIME = 0.0001      #Duração do pulso de disparo do triac
TIME_ZC_CHECK = 0.001   #Tempo da interrupção de checagem de passagem por zero

flag_end_thread = False
flag_malha_aberta = False    #Se True elimina o controle  PID e a malha fica aberta

#Controle
ideal_value = 0     #Set point atual
integral = 0
kp = 2              #Valores dos ganhos proporcinal, integral e derivativo
ki = 0.01
kd = 0.1

#*************************************************************************************************
#SUB-ROTINAS DO SISTEMA
def gera_grafico():
    plt.plot(tempo, valor_temp)
    plt.grid()
    plt.title("Dados do Ciclo de Soldagem")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura")
    plt.show()

def pid_control():
    global DELAY_TIME, integral
    measure = valor_temp[cont]
    error_meas = ideal_value - measure
    proportional = error_meas
    integral += error_meas * time_sample
    derivative = (valor_temp[cont-1] - measure)/time_sample
    PID = (kp*proportional) + (ki*integral) + (kd*derivative)
    PID = PID/22500         #Range 0-180Graus e delay 0.000-0.008
    pulse = 0.008 - PID

    if (pulse > 0.008):
        pulse = 0.008
    if (pulse < 0.001):
        pulse = 0.001
    DELAY_TIME = pulse
    lb3['text'] = 'Erro PID: ' + str(PID) + ' s'
    lb4['text'] = 'Valor Delay Time: ' + str(DELAY_TIME) + ' s'
    lb5['text'] = 'Tempo Decorrido: ' +str(cont*time_sample/60) + ' min'

def evento_timer1():                 #Interrupção de aquisição de dados
    global cont
    global tempo
    global valor_temp

    if(cont == 0):                   #Verifica se é a primeira amostra
        tempo.append(0)
    else:
        tempo.append(tempo[cont-1] + time_sample)

    valor_temp.append(sensor_read())  #Adiciona uma nova amostra de temperatura
    lb2['text'] = 'Temperatura atual: ' + str(valor_temp[cont]) + ' ºC'
    if (cont > 1 and flag_malha_aberta == False):
        pid_control()                    #Chama a rotina de controle PID, necessita 2 leituras
    cont += 1                        #Incrementa uma posição de amostra

    timer1 = Timer(time_sample, evento_timer1)
    if (flag_interrupcao == True):
        timer1.start()
    else:
        timer1.cancel()

def sensor_read():                   #Lê o sensor de temperatura e retorna um float
	t = spi.readbytes(2)

	msb = format(t[0], '#010b')
	lsb = format(t[1], '#010b')

	r_temp = msb[2:] + lsb[2:]
	t_bytes = "0b" + r_temp[0:13]
	temp = int(t_bytes, base=2)*0.25
	return temp

def encerra_ciclo_solda():          #Encerra o cliclo de soldagem atual
    global tempo, valor_temp, cont, flag_interrupcao
    print("Encerrando processo de soldadgem.")
    time.sleep(2*time_sample)
    gera_grafico()
    tempo = []                  #Apaga os valores coletados do ciclo de soldagem
    valor_temp = []
    cont = 0
    flag_interrupcao = True     #Inicia a aquisição de dados contínua

def inicia_controle_solda(null):
    global ideal_value
    print("Controle de solda iniciado")
    lb7['text'] = 'Status Soldagem: PRÉ-AQUECIMENTO'
    ideal_value = 125       #Set point pre-aquecimento
    time.sleep(100)

    lb7['text'] = 'Status Soldagem: SOAK'
    ideal_value = 160       #Set point soak
    time.sleep(80)

    lb7['text'] = 'Status Soldagem: REFLOW'
    ideal_value = 230       #Set point reflow
    time.sleep(60)

    lb7['text'] = 'Status Soldagem: FINALIZADO'
    print("Processo de controle de solda finalizado")
    ideal_value = 0

#Módulo de potência
def checa_zc(null):
    #Módulo de potência
    GPIO.setmode(GPIO.BCM)    #Configura o GPIO para ser usado como portas paralelas
    GPIO.setup(DIM, GPIO.OUT)  #Configura a porta GPIO como saída
    GPIO.setup(ZC, GPIO.IN)   #Configura a porta GPIO como entrada
    print(DELAY_TIME)
    while True:
        if (GPIO.input(ZC) == True):         #Testa a passagem por zero
            time.sleep(DELAY_TIME)           #Espera o tempo de disparo
            GPIO.output(DIM, GPIO.HIGH)      #Dispara o triac
            time.sleep(PULSE_TIME)           #Tempo do pulso
            GPIO.output(DIM, GPIO.LOW)       #Finaliza o pulso de disparo
        if (flag_end_thread == True):        #Checa se encerrou o processo
            GPIO.cleanup()
            exit()


#*************************************************************************************************
#EVENTOS DA INTERFACE GRÁFICA
#def apertou_tecla(event):                           #Função do evento de apertar a tecla
#    trata_tecla(event.char, event.keycode)

#def botao_direito(event):                           #O parâmetro event deve ser passado obrigatoriamente
#    lb2['text']= trata_direito()

#def on_leave(event):
#    trata_mouse_out()

#def on_enter(enter):
#    trata_mouse_in()

def clica_bt2(event):
    global flag_interrupcao, flag_end_thread, flag_malha_aberta
    flag_interrupcao = False
    flag_end_thread = True    #Encerra o processo paralelo
    flag_malha_aberta = False
    encerra_ciclo_solda()

def clica_bt1(event):       #Rotina que dá início do processo de soldadgem
    global flag_end_thread
    evento_timer1()         #Inicia o ciclo de aquisição de dados
    #Inicia o processo paralelo de chaveamento do triac
    _thread.start_new_thread(checa_zc, (1,))
    flag_end_thread = False
    if (flag_malha_aberta == False):
        _thread.start_new_thread(inicia_controle_solda, (1,))


def clica_bt3(event):
    global DELAY_TIME
    global flag_malha_aberta
    DELAY_TIME = float(ed1.get())
    print(DELAY_TIME)
    flag_malha_aberta = True

def carrega_teclado(event):
    numkey.open()

#*************************************************************************************************
#GUI
janela = Tk()
janela.geometry(resolucao)
#janela.bind('<Key>', apertou_tecla)         #<Key> é o evento de precionar a tecla e chama a rotina
                                            #que tratará esse evento apertou_tecla()

lb1 = Label(janela, text='PROGRAMA DESTINADO AO CONTROLE DO FORNO REFLOW SMD.')
lb2 = Label(janela, text='Temperatura atual: ')
lb3 = Label(janela, text='Erro PID: ')
lb4 = Label(janela, text='Valor Delay Time: ')
lb5 = Label(janela, text='Tempo Decorrido: ')
lb6 = Label(janela, text='   Insira o Valor do Time Delay[s]: ')
lb7 = Label(janela, text='Status Soldagem: ')
bt1 = Button(janela, text='Iniciar Soldagem', width=50, height=3)
bt2 = Button(janela, text='Encerra Soldagem - TEMPORÁRIO', width=50, height=3)
bt3 = Button(janela, text='Carrega Delay Time - Malha Aberta', width=50, height=3)
bt4 = Button(janela, text='123...', height=3)
ed1 = Entry(janela, width=7)
numkey = NumKey(ed1)     #Instância do objeto Teclado Numérico

#janela.bind('<Button-3>', botao_direito)    #Evento de apertar o botão direito do mouse
#bt1.bind('<Leave>', on_leave)               #Os eventos estão disponíveis também para os outros objetos
#bt1.bind('<Enter>', on_enter)               #Evento de colocar o ponteiro do mouse sobre o objeto
bt2.bind('<Button-1>', clica_bt2)
bt1.bind('<Button-1>', clica_bt1)
bt3.bind('<Button-1>', clica_bt3)
bt4.bind('<Button-1>', carrega_teclado)

#*************************************************************************************************
#Layout
lb1.grid(row=0, column=0, pady=10, sticky=W+E, columnspan=4)
bt1.grid(row=1, column=0, pady=5, sticky=W+E, columnspan=4)
bt2.grid(row=2, column=0, pady=5, sticky=W+E, columnspan=4)
bt3.grid(row=3, column=0, sticky=W, pady=5)
lb6.grid(row=3, column=1, sticky=W)
ed1.grid(row=3, column=2, sticky=W)
bt4.grid(row=3, column=3, sticky=W, pady=5)
lb2.grid(row=4, column=0, sticky=W, pady=5)
lb3.grid(row=5, column=0, sticky=W, pady=2)
lb4.grid(row=6, column=0, sticky=W, pady=2)
lb5.grid(row=7, column=0, sticky=W, pady=2)
lb7.grid(row=8, column=0, sticky=W, pady=2)

#*************************************************************************************************
#INICIALIZAÇÃO DO HARDWARE
spi = spidev.SpiDev()               #Inicialização da porta SPI
spi.open(0, 0)
spi.max_speed_hz = 3900000

#*************************************************************************************************
#INICIALIZAÇÃO DA INTERFACE GRÁFICA
#Run
janela.mainloop()

#Fechamento da interface gráfica e finalização
flag_interrupcao = False

#***********************************************************************************************
#                          MÓDULO TECLADO NUMÉRICO
#***********************************************************************************************
'''
Chamada:
obj = TecladoNumerico(ed, dot=True)
Onde:
ed é um objeto do tipo tkinter Entry
dot: True para botão ponto habilitado, False para desabilitado
'''
#Dependência de Módulos
from tkinter import *

#***************************** TECLADO NUMÉRICO *******************************************
class TecladoNumerico(object):       


#******************************** CONSTRUCTOR *********************************************
    def __init__(self, entrada, dot=True):
        self.resolucao = '355x370+0+0'
        self.obj = entrada
        self._valor = 0.0
        self._dot_enabled = dot
    
    def open(self):
        self.janela = Tk()
        self.janela.geometry(self.resolucao)
        self.janela.resizable(False, False)
        self.janela.title('Numeric')
       
      
        #Elementos Gráficos
        self.lb_valor = Label(self.janela, text='0', justify=RIGHT, font=("Arial", 20))
        self.bt9 = Button(self.janela, width=6, height=3, text='9', font=("Arial", 14), command=self.evento_botao9)
        self.bt8 = Button(self.janela, width=6, height=3, text='8', font=("Arial", 14), command=self.evento_botao8)
        self.bt7 = Button(self.janela, width=6, height=3, text='7', font=("Arial", 14), command=self.evento_botao7)
        self.bt6 = Button(self.janela, width=6, height=3, text='6', font=("Arial", 14), command=self.evento_botao6)
        self.bt5 = Button(self.janela, width=6, height=3, text='5', font=("Arial", 14), command=self.evento_botao5)
        self.bt4 = Button(self.janela, width=6, height=3, text='4', font=("Arial", 14), command=self.evento_botao4)
        self.bt3 = Button(self.janela, width=6, height=3, text='3', font=("Arial", 14), command=self.evento_botao3)
        self.bt2 = Button(self.janela, width=6, height=3, text='2', font=("Arial", 14), command=self.evento_botao2)
        self.bt1 = Button(self.janela, width=6, height=3, text='1', font=("Arial", 14), command=self.evento_botao1)
        self.bt0 = Button(self.janela, width=6, height=3, text='0', font=("Arial", 14), command=self.evento_botao0)
        self.bt_enter = Button(self.janela, width=6, height=3, text='Enter', font=("Arial", 14), command=self.evento_enter)
        self.bt_cancel = Button(self.janela, width=6, height=3, text='Cancel', font=("Arial", 14), command=self.evento_cancel)
        self.bt_clear = Button(self.janela, width=6, height=3, text='Clear', font=("Arial", 14), command=self.evento_clear)

        if (self._dot_enabled == True):
            self.bt_ponto = Button(self.janela, width=6, height=3, text='.', font=("Arial", 14),
                               command=self.evento_botao_ponto, state=NORMAL)
        else:
            self.bt_ponto = Button(self.janela, width=6, height=3, text='.', font=("Arial", 14),
                               command=self.evento_botao_ponto, state=DISABLED)
        
        
        #Layout
        self.lb_valor.grid(row=0, column=0, sticky=E, columnspan=4, pady=10)
        self.bt9.grid(row=1, column=2, sticky=W)
        self.bt8.grid(row=1, column=1, sticky=W)
        self.bt7.grid(row=1, column=0, sticky=W)
        self.bt6.grid(row=2, column=2, sticky=W)
        self.bt5.grid(row=2, column=1, sticky=W)
        self.bt4.grid(row=2, column=0, sticky=W)
        self.bt3.grid(row=3, column=2, sticky=W)
        self.bt2.grid(row=3, column=1, sticky=W)
        self.bt1.grid(row=3, column=0, sticky=W)
        self.bt0.grid(row=4, column=0, sticky=W+E, columnspan=2)
        self.bt_ponto.grid(row=4, column=2, sticky=W)
        self.bt_enter.grid(row=3, column=3, sticky=N+S, rowspan=2)
        self.bt_cancel.grid(row=2, column=3, sticky=W)
        self.bt_clear.grid(row=1, column=3, sticky=W)
        

# ****************************** DESTRUCTOR *********************************************
    def __del__(self):
        pass

#**************************** MÉTODOS DA CLASSE ****************************************
    def evento_botao9(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '9'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'9'
            self.lb_valor['text'] = self.lista
    
    def evento_botao8(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '8'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'8'
            self.lb_valor['text'] = self.lista

    def evento_botao7(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '7'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'7'
            self.lb_valor['text'] = self.lista

    def evento_botao6(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '6'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'6'
            self.lb_valor['text'] = self.lista

    def evento_botao5(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '5'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'5'
            self.lb_valor['text'] = self.lista

    def evento_botao4(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '4'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'4'
            self.lb_valor['text'] = self.lista

    def evento_botao3(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '3'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'3'
            self.lb_valor['text'] = self.lista

    def evento_botao2(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '2'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'2'
            self.lb_valor['text'] = self.lista

    def evento_botao1(self):
        if (self.lb_valor['text'] == '0'):
            self.lb_valor['text'] = '1'
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'1'
            self.lb_valor['text'] = self.lista

    def evento_botao0(self):
        if (self.lb_valor['text'] == '0'):
            pass
        else:
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'0'
            self.lb_valor['text'] = self.lista

    def evento_botao_ponto(self):
        if (self.lb_valor['text'].isnumeric()):    
            self.lista = self.lb_valor['text']
            self.lista = self.lista+'.'
            self.lb_valor['text'] = self.lista

    def evento_clear(self):
        self.lb_valor['text'] = '0'

    def evento_cancel(self):
        self.janela.destroy()

    def evento_enter(self):
        self.obj.delete(0, 'end')
        self.obj.insert(0, self.lb_valor['text'])
        self._valor = float(self.lb_valor['text'])
        self.janela.destroy()

    def get_last_value(self):
        return self._valor

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from pylab import rcParams
from sympy.sets import Interval
from sympy.calculus.util import continuous_domain

x, w = symbols('x w')

#função que calcula o polinômio interpolado pela fórmula de lagrange
def interpoladoLagrange(x, y):
    '''
    x: Valores dados em x
    y: f(x)

    espera-se dois numpy.Arrays ou pandas.Series de mesma dimensão
    '''
    #inicia o polinômio como uma expressão Sympy = 0(elemento nulo do somatório)
    poli = 0*w
    #inicia um loop que vai rodar 1 vez para cada termo em x
    for i in range(len(x)):
        #inicia um termo do polinômio como uma expressão Sympy = 1(elemento nulo do produtório)
        Li = 1 + 0*w
        #inicia um loop que vai rodar 1 vez para cada termo j que existe dentro de x
        for j in x:
            #para cada termo j que seja diferente do termo x[i] relacionado ao primeiro loop
            if j != x[i]:
                #atualiza o termo do polinômio, o multiplicando por (w-j)/(x[i] - j)
                Li = Li * ((w - j)/(x[i] - j))
        #soma o termo do polinomio, multiplicado pelo respectivo y[i] ao polinomio 
        poli = poli + y[i] * Li
    #retorna o polinomio expandido - expressão do sympy na variável 'w'
    return expand(poli)

#função que plota a interpretação gráfica do método do trapézio
def trapezioPlot(func, x_o, x_f, n):
    '''
    func: função a ser integrada - expressão do sympy na variável 'x'
    x_o: valor inicial do intervalo - float
    x_f: valor final do intervalo - float
    n: número de trapézios a ser usado - int

    '''
    #inicia a instância do Matplotlib
    fig, ax = plt.subplots()

    #gera um range com n*1000 valores dentro do intervalo
    xxFunc = np.linspace(x_o, x_f, n*1000)
    #calcula o f(x) desses valores gerados
    yyFunc = lambdify(x, func, "numpy")(xxFunc)
    # plota os intervalos calculados (gráfico da função em si)
    ax.plot(xxFunc, np.transpose(yyFunc), linewidth=2)

    #organiza o titulo e os labels dos eixos
    ax.set_title('Função - {}'.format(str(func)))
    ax.set_ylabel('y')
    ax.set_xlabel('x')

    #calcula o tamanho de cada trapézio
    h = (x_f - x_o)/n
    #inicia o x_iteração como inicio do intervalo
    x_i = x_o
    #abre um loop que rodará 1 vez para cada trapézio a ser usado: (n)
    for i in range(n):
        #define o x_h como final do primeiro trapézio
        x_h = x_i + h
        
        #define o x e o f(x), como esperado pela função da interpolação de lagrange
        dados = pd.DataFrame({'x': [x_i, x_i + h],
                              'y': [(func.subs(x, x_i)).evalf(), (func.subs(x, x_h)).evalf()]})
        #calcula o polinomio da reta
        reta = interpoladoLagrange(dados['x'], dados['y'])
        
        #repete o processo de criação do gráfico
        xx = np.linspace(x_i, x_h, 1000)
        yy = lambdify(w, reta, "numpy")(xx)
        ax.plot(xx, np.transpose(yy), color='#555555', linewidth=1)
        #preenche a aréa entre a reta e o eixo x
        ax.fill_between(xx, yy, 0, alpha=0.20, color='#555555', label='Areá Trapézio')
        #preenche a aréa entre a reta e o gráfico da função como erro
        yyFunc_fill = np.split(yyFunc, n)[i]
        ax.fill_between(xx, yy, yyFunc_fill, alpha=0.50, color='#555555', label='Erro')
        #insere as retas verticais referentes às bases do trapézio
        ax.vlines(x_i, 0, (func.subs(x, x_i)).evalf(), linestyles='dashed', color='#555555', linewidth=1)
        ax.vlines(x_h, 0, (func.subs(x, x_h)).evalf(), linestyles='dashed', color='#555555', linewidth=1)
        
        #atualiza o valor de inicio do trapézio, como o fim do trapézio anterior
        x_i = x_i + h
    
    #retorna a figura à ser plotada
    return fig

#calcula a soma das areas dos trapézio
def calculoArea(func, x_o, x_f, n):
    '''
    func: função a ser integrada - expressão do sympy na variável 'x'
    x_o: valor inicial do intervalo - float
    x_f: valor final do intervalo - float
    n: número de trapézios a ser usado - int

    '''
    #inicia a soma como 0(elemento nulo da soma)
    area = 0
    #calcula o tamanho de cada trapézio
    h = (x_f - x_o)/n
    #inicia o valor inicial do primeiro trapézio como o valor inicial do trapezio
    x_i = x_o
    #abre um loop que rodará 1 vez para cada trapézio
    for i in range(n):
        #atualiza a soma, somando o valor da área do trapézio em questão
        area = area + (func.subs(x, x_i).evalf() + func.subs(x, x_i + h).evalf())*h/2
        #atualiza o valor inicial do trapézio, como valor final do trapézio anterior
        x_i = x_i + h

    #retorna a soma total das areas - float
    return area

def calculoErro(func, x_o, x_f, n):
    '''
    func: função a ser integrada - expressão do sympy na variável 'x'
    x_o: valor inicial do intervalo - float
    x_f: valor final do intervalo - float
    n: número de trapézios a ser usado - int

    '''
    #calcula o tamanho de cada trapézio
    h = (x_f - x_o)/n
    
    #calcula a segunda derivada da função
    diff_2 = diff(diff(func, x), x)
    #testa vários valores na segunda derivada
    xx = np.linspace(x_o, x_f, 1000)
    yy = lambdify(x, diff_2, "numpy")(xx)
    #se possivel, define o valor M_2 como módulo do valor máximo da segunda derivada no intervalo
    try:
        M_2 = abs(float(max(yy)))
    #exceto quando a segunda derivada é constante:
    except:
        #define M_2 como módulo da segunda derivada
        M_2 = abs(float(yy))

    erro = n*M_2*h**3/12
    #retorna a estimativa do erro - float
    return erro

def calculoN(func, x_o, x_f, erro):
    '''
    func: função a ser integrada - expressão do sympy na variável 'x'
    x_o: valor inicial do intervalo - float
    x_f: valor final do intervalo - float
    erro: erro máximo à ser usado - float

    '''
    #calcula a segunda derivada da função
    diff_2 = diff(diff(func, x), x)
    #testa vários valores na segunda derivada
    xx = np.linspace(x_o, x_f, 1000)
    yy = lambdify(x, diff_2, "numpy")(xx)
    #se possivel, define o valor M_2 como módulo do valor máximo da segunda derivada no intervalo
    try:
        M_2 = abs(float(max(yy)))
    #exceto quando a segunda derivada é constante:
    except:
        #define M_2 como módulo da segunda derivada
        M_2 = abs(float(yy))
    
    #calcula o valor minimo de trapezios a serem usados para que o erro seja <= que o erro
    n = np.sqrt((M_2*(x_f - x_o)**3)/(12*erro))
    #se o n for >= que 1 retorna primeiro int tal que i >= n - int
    if int(np.ceil(n)) >= 1:
        return int(np.ceil(n))
    #caso o contrário retorna 1 - int
    else:
        return 1
        
def integralDefinida(func, x_o, x_f):
    '''
    func: função a ser integrada - expressão do sympy na variável 'x'
    x_o: valor inicial do intervalo - float
    x_f: valor final do intervalo - float

    '''
    try:
        #se possivel retorna o valor real da integral definida no intervalo - float
        return N(integrate(func, (x, x_o, x_f)))
    except:
        #se não possivel retorna a frase - str
        return "Função não integravel por métodos convencionais"

def verifica_continuidade(func, x_o, x_f):
    '''
    func: função a ser integrada - expressão do sympy na variável 'x'
    x_o: valor inicial do intervalo - float
    x_f: valor final do intervalo - float

    '''
    if continuous_domain(func, x, Interval(x_o, x_f)) == Interval(x_o, x_f):
        #se a função for continua no intervalo retorna '1' - str para verificação no formulário
        return '1'
    else:
        #se não for continua no ntervalo retorna a 'Frase'
        return "A Função não é continua no intervalo, Indique outro Intervalo"
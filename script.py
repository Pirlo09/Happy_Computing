import random as rd
from math import *


def Uniforme(a, b):
    return a+(b-a)*rd.random()


def Bernoulli(p):
    if Uniforme(0, 1) <= p:
        return 1
    return 0


def Exponencial(l):
    return -(1/l)*log(Uniforme(0, 1))


def NormalStandar():
    while True:
        Y = Exponencial(1)
        U = Uniforme(0, 1)
        if U <= e**(-((Y-1)**2)/2):
            X = Y
            if Bernoulli(1/2):
                return X
            else:
                return -X


def Normal(m, s):
    return NormalStandar()*s+m


def Poisson(l):
    p = 1
    n = 0
    while 1:
        U = Uniforme(0, 1)
        p *= U
        n += 1
        if p < e**(-l):
            break
    N = n - 1
    return N


def RandomVar(X, P):
    U = Uniforme(0, 1)
    Fx = 0
    n = len(X)
    for i in range(n):
        Fx += P[i]
        if U < Fx:
            return X[i]


t = 0  # linea de tiempo
ta = Poisson(20)  # tiempo de arribo de clientes
T = 480  # jornada laboral
tDv1 = inf  # tiempo de salida de vendedor 1
tDv2 = inf  # tiempo de salida de vendedor 2
tDe = inf  # tiempo de salida de especialista
tDt1 = inf  # tiempo de salida de tecnico 1
tDt2 = inf  # tiempo de salida de tecnico 2
tDt3 = inf  # tiempo de salida de tecnico 3
Na = 0  # cantidad de arribos
A = {}  # diccionario arribo:tiempo
nv = 0  # numero de clientes en vendedores
NDv1 = 0  # cantidad de salidas de vendedor 1
NDv2 = 0  # cantidad de salidas de vendedor 2
Dv1 = {}  # dicionario cliente:salida de vendedor 1
Dv2 = {}  # dicionario cliente:salida de vendedor 2
ne = 0  # numero de clientes en especialista
NDe = 0  # cantidad de salidas de especialista
De = {}  # dicionario cliente:salida de especialista
nt = 0  # numero de clientes en tecnicos
NDt1 = 0  # cantidad de salidas de tecnico 1
NDt2 = 0  # cantidad de salidas de tecnico 2
NDt3 = 0  # cantidad de salidas de tecnico 3
Dt1 = {}  # dicionario cliente:salida de tecnico 1
Dt2 = {}  # dicionario cliente:salida de tecnico 2
Dt3 = {}  # dicionario cliente:salida de tecnico 3
# precios de servicios 1, 2, 3, 4 respectivamente
P = [0, 350, 500, 750]
# [n, Ct1, Ct2, Ct3 Qt] | n: numero de clientes en tecnicos, Cti: cliente en tecnico i, Qt: cola de clientes en tecnicos
ST = [0, 0, 0, 0, []]
# [n, Cv1, Cv2, Qv] | n: numero de clientes en vendedores, Cvi: cliente en vendedor i, Qv: cola de clientes en vendedores
SV = [0, 0, 0, []]
# [n, Ce, Qe] | | n: numero de clientes en especialista, Ce: cliente en especialista, Qe: cola de clientes en especialista
SE = [0, 0, []]
G = 0 # ganancia total


def simular():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    while 1:
        Min = min(ta, tDv1, tDv2, tDt1, tDt2, tDt3, tDe)
        if Min == ta and ta <= T:
            evento_de_arribo()
        elif Min == tDv1 and tDv1 <= T:
            evento_de_salida_vendedor_1()
        elif Min == tDv2 and tDv2 <= T:
            evento_de_salida_vendedor_2()
        elif Min == tDe and tDe <= T:
            evento_de_salida_especialista()
        elif Min == tDt1 and tDt1 <= T:
            evento_de_salida_tecnico_1()
        elif Min == tDt2 and tDt2 <= T:
            evento_de_salida_tecnico_2()
        elif Min == tDt3 and tDt3 <= T:
            evento_de_salida_tecnico_3()
        elif Min == tDv1 and Min > T and nv > 0:
            evento_de_cierre_vendedor_1()
        elif Min == tDv2 and Min > T and nv > 0:
            evento_de_cierre_vendedor_2()
        elif Min == tDe and Min > T and ne > 0:
            evento_de_cierre_especialista()
        elif Min == tDt1 and Min > T and nt > 0:
            evento_de_cierre_tecnico_1()
        elif Min == tDt2 and Min > T and nt > 0:
            evento_de_cierre_tecnico_2()
        elif Min == tDt3 and Min > T and nt > 0:
            evento_de_cierre_tecnico_3()
        else:
            break


def evento_de_arribo():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = ta
    Na += 1
    ta = t + Poisson(20)
    if ta > T:
        ta = inf
    A[Na] = t
    s = RandomVar([1, 2, 4, 3], [.45, .25, .2, .1])
    G += P[s - 1]
    if s == 3:  # arribo a servicio cambio de equipo
        ne += 1
        if SE[1] == 0:
            SE = [ne, Na, SE[2]]
            tDe = t + Exponencial(1/15)
        else:
            SE = [ne, SE[1], SE[2] + [Na]]
    elif s == 4:  # arribo a servicio venta(para comprar en este caso :D)
        nv += 1
        if SV[1] == 0:
            SV = [nv, Na, SV[2], SV[3]]
            tDv1 = t + Normal(5, 2)
        elif SV[2] == 0:
            SV = [nv, SV[1], Na, SV[3]]
            tDv2 = t + Normal(5, 2)
        else:
            SV = [nv, SV[1],
                  SV[2], SV[3] + [Na]]
    # arribo a servicio de reparacion ya sea por garantia (1) o fuera de garantia (2)
    else:
        nt += 1
        if ST[1] == 0:
            ST = [nt, Na,
                  ST[2], ST[3], ST[4]]
            tDt1 = t + Exponencial(1/20)
        elif ST[2] == 0:
            ST = [nt, ST[1],
                  Na, ST[3], ST[4]]
            tDt2 = t + Exponencial(1/20)
        elif ST[3] == 0:
            ST = [nt, ST[1],
                  ST[2], Na, ST[4]]
            tDt3 = t + Exponencial(1/20)
        elif SE[2] == 0 and len(SE[3]) == 0:
            ne += 1
            nt -= 1
            SE = [ne, Na, []]
            tDe = t + Exponencial(1/20)
        else:
            ST = [nt, ST[1], ST[2],
                  ST[3], ST[4] + [Na]]


def evento_de_salida_vendedor_1():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDv1
    NDv1 += 1
    Dv1[SV[1]] = t
    if nv == 1:
        nv -= 1
        SV = [0, 0, 0, []]
        tDv1 = inf
    elif nv == 2:
        nv -= 1
        SV = [1, 0, SV[2], []]
        tDv1 = inf
    elif nv > 2:
        f = SV[3][0]
        SV[3].remove(f)
        nv -= 1
        SV = [nv, f, SV[2], SV[3]]
        tDv1 = t + Normal(5, 2)


def evento_de_salida_vendedor_2():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDv2
    NDv2 += 1
    Dv2[SV[2]] = t
    if nv == 1:
        nv -= 1
        SV = [0, 0, 0, []]
        tDv2 = inf
    elif nv == 2:
        nv -= 1
        SV = [1, SV[1], 0, []]
        tDv2 = inf
    elif nv > 2:
        nv -= 1
        f = SV[3][0]
        SV[3].remove(f)
        SV = [nv, SV[1], f, SV[3]]
        tDv2 = t + Normal(5, 2)


def evento_de_salida_especialista():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDe
    NDe += 1
    De[SE[1]] = t
    if len(SE[2]) == 0:
        if len(ST[4]) == 0:
            ne -= 1
            tDe = inf
            SE = [nv, 0, []]
        else:
            nt -= 1
            tDe = t + Exponencial(1/20)
            f = ST[2][0]
            ST[2].remove(f)
            SE = [ne, f, []]
            ST[0] = nt
    else:
        ne -= 1
        tDe = t + Exponencial(1/15)
        f = SE[2][0]
        SE[2].remove(f)
        SE = [ne, f, SE[2]]


def evento_de_salida_tecnico_1():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDt1
    NDt1 += 1
    Dt1[ST[1]] = t
    if nt == 1:
        nt -= 1
        ST = [0, 0, 0, 0, []]
        tDt1 = inf
    elif nt == 2 or nt == 3:
        nt -= 1
        ST = [1, 0, ST[2], ST[3], []]
        tDt1 = inf
    elif nt > 3:
        nt -= 1
        f = ST[4][0]
        ST[4].remove(f)
        ST = [nt, f, ST[2], ST[3], ST[4]]
        tDt1 = t + Exponencial(1/20)


def evento_de_salida_tecnico_2():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDt2
    NDt2 += 1
    Dt2[ST[2]] = t
    if nt == 1:
        nt -= 1
        ST = [0, 0, 0, 0, []]
        tDt2 = inf
    elif nt == 2 or nt == 3:
        nt -= 1
        ST = [1, ST[1], 0, ST[3], []]
        tDt2 = inf
    elif nt > 3:
        nt -= 1
        f = ST[4][0]
        ST[4].remove(f)
        ST = [nt, ST[1], f, ST[3], ST[4]]
        tDt2 = t + Exponencial(1/20)


def evento_de_salida_tecnico_3():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDt3
    NDt3 += 1
    Dt3[ST[3]] = t
    if nt == 1:
        nt -= 1
        ST = [0, 0, 0, 0, []]
        tDt3 = inf
    elif nt == 2 or nt == 3:
        nt -= 1
        ST = [1, ST[1], ST[2], 0, []]
        tDt3 = inf
    elif nt > 3:
        nt -= 1
        f = ST[4][0]
        ST[4].remove(f)
        ST = [nt, ST[1], ST[2], f, ST[4]]
        tDt3 = t + Exponencial(1/20)


def evento_de_cierre_vendedor_1():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDv1
    NDv1 += 1
    Dv1[SV[1]] = t
    if nv == 1:
        nv -= 1
        SV = [0, 0, 0, []]
        tDv1 = inf
    elif nv == 2:
        nv -= 1
        SV = [1, 0, SV[2], []]
        tDv1 = inf
    elif nv > 2:
        f = SV[3][0]
        SV[3].remove(f)
        nv -= 1
        SV = [nv, f, SV[2], SV[3]]
        tDv1 = t + Normal(5, 2)


def evento_de_cierre_vendedor_2():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDv2
    NDv2 += 1
    Dv2[SV[2]] = t
    if nv == 1:
        nv -= 1
        SV = [0, 0, 0, []]
        tDv2 = inf
    elif nv == 2:
        nv -= 1
        SV = [1, SV[1], 0, []]
        tDv2 = inf
    elif nv > 2:
        nv -= 1
        f = SV[3][0]
        SV[3].remove(f)
        SV = [nv, SV[1], f, SV[3]]
        tDv2 = t + Normal(5, 2)


def evento_de_cierre_especialista():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDe
    NDe += 1
    De[SE[1]] = t
    if len(SE[2]) == 0:
        if len(ST[4]) == 0:
            ne -= 1
            tDe = inf
            SE = [nv, 0, []]
        else:
            nt -= 1
            tDe = t + Exponencial(1/20)
            f = ST[2][0]
            ST[2].remove(f)
            SE = [ne, f, []]
            ST[0] = nt


def evento_de_cierre_tecnico_1():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDt1
    NDt1 += 1
    Dt1[ST[1]] = t
    if nt == 1:
        nt -= 1
        ST = [0, 0, 0, 0, []]
        tDt1 = inf
    elif nt == 2 or nt == 3:
        nt -= 1
        ST = [1, 0, ST[2], ST[3], []]
        tDt1 = inf
    elif nt > 3:
        nt -= 1
        f = ST[4][0]
        ST[4].remove(f)
        ST = [nt, f, ST[2], ST[3], ST[4]]
        tDt1 = t + Exponencial(1/20)


def evento_de_cierre_tecnico_2():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDt2
    NDt2 += 1
    Dt2[ST[2]] = t
    if nt == 1:
        nt -= 1
        ST = [0, 0, 0, 0, []]
        tDt2 = inf
    elif nt == 2 or nt == 3:
        nt -= 1
        ST = [1, ST[1], 0, ST[3], []]
        tDt2 = inf
    elif nt > 3:
        nt -= 1
        f = ST[4][0]
        ST[4].remove(f)
        ST = [nt, ST[1], f, ST[3], ST[4]]
        tDt2 = t + Exponencial(1/20)


def evento_de_cierre_tecnico_3():
    global t
    global ta
    global T
    global tDv1
    global tDv2
    global tDe
    global tDt1
    global tDt2
    global tDt3
    global G
    global Na
    global A
    global nv
    global NDv1
    global NDv2
    global Dv1
    global Dv2
    global ne
    global NDe
    global De
    global nt
    global NDt1
    global NDt2
    global NDt3
    global Dt1
    global Dt2
    global Dt3
    global P
    global ST
    global SV
    global SE

    t = tDt3
    NDt3 += 1
    Dt3[ST[3]] = t
    if nt == 1:
        nt -= 1
        ST = [0, 0, 0, 0, []]
        tDt3 = inf
    elif nt == 2 or nt == 3:
        nt -= 1
        ST = [1, ST[1], ST[2], 0, []]
        tDt3 = inf
    elif nt > 3:
        nt -= 1
        f = ST[4][0]
        ST[4].remove(f)
        ST = [nt, ST[1], ST[2], f, ST[4]]
        tDt3 = t + Exponencial(1/20)


simular()

print(f'Ganancia total: {G}')
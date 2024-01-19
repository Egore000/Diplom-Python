import numpy as np
from math import *
from datetime import date
import numba

from params import mu, eps


def reduce(x: float) -> float:
    '''
    Приведение угла к значению из интервала [0, 2pi]
    '''
    a = x - int(x/(pi*2))*pi*2
    if x<0:
        return a + pi*2
    return a

def anomaly(t0: float, t: float, ecc: float, 
            M0: float, n: float, eps: float) -> float:
    '''
    Вычисление аномалии Е
    * t0 - начальная эпоха
    * t - конечная эпоха
    * ecc - эксцентриситет орбиты
    * M0 - начальная средняя аномалия
    * n - среднее движение
    * eps - точность вычисления
    '''
    M = n*(t - t0) + M0
    
    dif = 1
    E0 = M
    
    while abs(dif) > eps:
        E = M + ecc*sin(E0)
        dif = E - E0
        E0 = E

    return E 

# @numba.njit()
def TwoBody(t0: float, t: float, M0: float, 
            a: float, w: float, Omega: float,
            i: float, ecc: float, n: float, eps: float) -> tuple[float]:
    '''
    Решение задачи двух тел
    Определение координат и скоростей тела по данным о
    элементах орбиты
    * t0 - начальная эпоха
    * t - конечная эпоха
    * M0 - начальная средняя аномалия
    * a - большая полуось
    * w - аргумент перицентра
    * Omega - долгота восходящего узла
    * i - наклонение орбиты
    * ecc - эксцентриситет орбиты
    * n - среднее движение
    * eps - точность вычисления
    
    Выходные значения:
    (x, y, z, Vx, Vy, Vz)
    '''
    E = anomaly(t0=t0,
                t=t, 
                ecc=ecc, 
                M0=M0, 
                n=n, 
                eps=eps)

    a1 = cos(w)*cos(Omega) - sin(w)*sin(Omega)*cos(i)
    b1 = cos(w)*sin(Omega) + sin(w)*cos(Omega)*cos(i)
    c1 = sin(w)*sin(i)

    a2 = -sin(w)*cos(Omega) - cos(w)*sin(Omega)*cos(i)
    b2 = -sin(w)*sin(Omega) + cos(w)*cos(Omega)*cos(i)
    c2 = cos(w)*sin(i)

    xi = a*(cos(E) - ecc)
    eta = a*sqrt(1 - ecc**2)*sin(E)

    Vxi = -a*n*sin(E)/(1 - ecc*cos(E))
    Veta = a*n*sqrt(1 - ecc**2)*cos(E)/(1 - ecc*cos(E))

    x = a1*xi + a2*eta
    y = b1*xi + b2*eta
    z = c1*xi + c2*eta

    Vx = a1*Vxi + a2*Veta 
    Vy = b1*Vxi + b2*Veta 
    Vz = c1*Vxi + c2*Veta 

    return (x, y, z, Vx, Vy, Vz)


# @numba.njit()
def CoordsToElements(coords: list, velocities: list) -> tuple[float]:
    '''
    Переход от координат и скоростей к элементам орбиты
    * coords - массив координат
    * velocities - массив скоростей

    Выходные значения:
    (ecc, i, a, Omega, w, M)
    '''
    x, y, z = coords[0], coords[1], coords[2]
    Vx, Vy, Vz = velocities[0], velocities[1], velocities[2]

    r = sqrt(x**2 + y**2 + z**2)
    V2 = Vx**2 + Vy**2 + Vz**2
    h = V2/2 - mu/r
    
    c1 = y*Vz - z*Vy
    c2 = z*Vx - x*Vz 
    c3 = x*Vy - y*Vx 

    l1 = -mu*x/r + Vy*c3 - Vz*c2
    l2 = -mu*y/r + Vz*c1 - Vx*c3
    l3 = -mu*z/r + Vx*c2 - Vy*c1

    c = sqrt(c1**2 + c2**2 + c3**2)
    l = sqrt(l1**2 + l2**2 + l3**2)

    a = -mu/(2*h)
    ecc = l/mu
    i = np.arctan2(sqrt(1 - c3**2/c**2), c3/c)

    if i == 0:
        i += 1e-12

    Omega = np.arctan2(c1/(c*sin(i)), -c2/(c*sin(i)))
    # Omega = np.arctan2(c1, -c2)

    w = np.arctan2(l3/(l*sin(i)), l1/l*cos(Omega) + l2/l*sin(Omega))

    E0 = np.arctan2((x*Vx + y*Vy + z*Vz)/(ecc*sqrt(mu*a)), (1-r/a)/ecc)
    M = E0 - ecc*sin(E0)
    
    return (ecc, i, a, Omega, w, M)

# @numba.njit()
def sid2000(jd: float) -> float:
    '''
    Вычисление sid2000
    * jd - юлианская дата
    '''
    jd2000 = 2451545
    jdyear = 36525

    m = jd - int(jd) - 0.5
    d = jd - m - jd2000
    # print(month)

    t = (d + m)/jdyear
    mm = m*86400
    s = (24110.54841+mm+236.555367908*(d+m)+(0.093104*t-6.21E-6*t**2)*t)/86400*2*pi
    return s


def transition(h: float, x: float) -> tuple[float]:
    A = np.array([
                [cos(h), sin(h), 0], 
                [-sin(h), cos(h), 0],
                [0, 0, 1]])
    
    y = A @ x
    r = sqrt(y[0]**2 + y[1]**2 + y[2]**2)
    lmd = np.arctan(y[1]/y[0])
    phi = np.arcsin(y[3]/r)

    return lmd, phi

# @numba.njit()
def resonance(year: int, month: int, day: float, 
            M: float, Omega: float, w: float, u: int, v: int) -> list[float]:
    '''
    Вычисление критических аргументов орбитального резонанса
    '''
    jd = date(year, month, day).toordinal() + 1721424.5
    theta = sid2000(jd)
    
    F1 = reduce(u * (M + Omega + w) - v * theta) * 180/pi
    F2 = reduce(u * (M + w) + v * (Omega - theta)) * 180/pi
    F3 = reduce(u * M + v * Omega) * 180/pi
    F4 = reduce(F1 - v * Omega) * 180/pi
    F5 = reduce(F3 + v * Omega - 2 * v * w) * 180/pi
    
    F = np.array([F1, F2, F3, F4, F5])
    return F

# @numba.njit()
def derivative_resonance(ecc: float, i: float, a: float, u: int, v: int) -> list[float]:
    '''
    Вычисление частот оритальных резонансов
    '''
    mL = 1/81.3005690699
    mS = 332946.048166
    J2 = 1.0826359e-3
    r0 = 6363.6726
    iL = iS = 23.45 * pi/180
    aL = 384748
    aS = 149597868
    nL = 2*pi/(27.32166 * 86400)
    nS = 2*pi/(365.25 * 86400)
    theta = 7.292115e-5

    n = sqrt(mu/a**3)

    OmegaJ2 = -1.5*J2 * n * (r0/a)**2 * cos(i) / (1-ecc**2)**2
    wJ2 = 0.75*J2 * n * (r0/a)**2 * (5*cos(i)**2 - 1)/(1-ecc**2)**2

    OmegaL = -3/16 * nL * mL * (a/aL)**3 * (2+3*ecc**2)/sqrt(1-ecc**2)*(2 - 3*sin(iL)**2)*cos(i)
    OmegaS = -3/16 * nS * mS * (a/aS)**3 * (2+3*ecc**2)/sqrt(1-ecc**2)*(2 - 3*sin(iS)**2)*cos(i)

    wL = 3/16 * nL * mL * (a/aL)**3 * (4-5*sin(i)**2 + ecc**2)/sqrt(1 - ecc**2) * (2 - 3*sin(iL)**2)
    wS = 3/16 * nS * mS * (a/aS)**3 * (4-5*sin(i)**2 + ecc**2)/sqrt(1 - ecc**2) * (2 - 3*sin(iS)**2)
    
    Omega = OmegaJ2 + OmegaL + OmegaS
    w = wJ2 + wL + wS

    F1 = u * (n + Omega + w) - v * theta
    F2 = u * (n + w) + v * (Omega - theta)
    F3 = u * n + v * (Omega + w - theta)
    F4 = F1 - v * Omega
    F5 = F3 + v * Omega - 2 * v * w
    F = [F1, F2, F3, F4, F5]
    return F

if __name__ == "__main__":
    jd = date(2023, 10, 20).toordinal() + 1721424.5
    print(jd)
    print(sid2000(jd))
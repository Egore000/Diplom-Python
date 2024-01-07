import matplotlib.pyplot as plt
import math

autosave = 0

# path_data = r'C:\Users\egorp\Desktop\диплом\файлы\ЧМ ИСЗ (для ПК) 28.04.20 Lobbie III'
# path_fig = r'C:\Users\egorp\Desktop\диплом\файлы\графики\Орбитальные резонансы'
# path_out = r'C:\Users\egorp\Desktop\диплом\файлы\Элементы'
# path_resonance = r'C:\Users\egorp\Desktop\диплом\файлы\Pascal\Вторичные резонансы.dat'

path_data = r'C:\Users\egorp\Desktop\диплом\файлы\Данные\1'
path_fig = r'C:\Users\egorp\Desktop\диплом\файлы\графики\Орбитальные резонансы\Спутники'
path_out = r'C:\Users\egorp\Desktop\диплом\файлы\Элементы'
path_resonance = r'C:\Users\egorp\Desktop\диплом\файлы\Данные\Выход\Вторичные\плюс'


mu = 3.986004418e+5
eps = 1e-12
toDeg = 180/math.pi
toRad = math.pi/180

def Degree(x: float) -> float:
    return x * toDeg

def Radian(x: float) -> float:
    return x * toRad

custom_rcParams = {
    'figure.figsize': (11, 4),
    'figure.subplot.hspace': 0, 
    'font.size': 10,
    'lines.linewidth': 0.7,
    'lines.color': 'black',
    # 'lines.linestyle': ':',
    'grid.alpha': 0.5,
    'font.family': 'Times New Roman'
}
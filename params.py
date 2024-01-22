import matplotlib.pyplot as plt
import math

autosave = 0
BASE_FOLDER = r'C:\Users\egorp\Desktop\диплом\файлы'

# PATH_DATA = BASE_FOLDER + r'\ЧМ ИСЗ (для ПК) 28.04.20 Lobbie III'
# PATH_FIG = BASE_FOLDER + r'\графики\Орбитальные резонансы'
# PATH_OUT = BASE_FOLDER + r'\Элементы'
# PATH_RESONANCE = BASE_FOLDER + r'\Вторичные резонансы.dat'

# PATH_DATA = BASE_FOLDER + r'\Данные\Без светового давления\1'
PATH_DATA = BASE_FOLDER + r'\Данные\Со световым давлением\1'
PATH_FIG = BASE_FOLDER + r'\графики\Орбитальные резонансы\Спутники'
PATH_OUT = BASE_FOLDER + r'\Элементы'
PATH_RESONANCE = BASE_FOLDER + r'\Данные\Выход\Вторичные\плюс'
PATH_CLASSIFICATION = BASE_FOLDER + r'\Rezonansy1_2.xlsx'
PATH_MAP = BASE_FOLDER + r'\графики\Зоны'

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
    # 'lines.linestyle': 'dotted',
    'grid.alpha': 0.5,
    'font.family': 'Times New Roman'
}
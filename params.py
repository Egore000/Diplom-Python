import matplotlib.pyplot as plt
import math

autosave = 0
BASE_FOLDER = 'C:\\Users\\egorp\\Desktop\\диплом\\файлы\\'

# PATH_DATA = BASE_FOLDER + r'\ЧМ ИСЗ (для ПК) 28.04.20 Lobbie III'
# PATH_FIG = BASE_FOLDER + r'\графики\Орбитальные резонансы'
# PATH_OUT = BASE_FOLDER + r'\Элементы'
# PATH_RESONANCE = BASE_FOLDER + r'\Вторичные резонансы.dat'

PATH_DATA = BASE_FOLDER + 'Исходные данные\\'
PATH_FIG = BASE_FOLDER + 'графики\\Орбитальные резонансы\\Спутники\\'
PATH_OUT = BASE_FOLDER + 'Элементы\\'
PATH_OUTDATA = BASE_FOLDER + 'Выходные данные\\'
# PATH_CLASSIFICATION = BASE_FOLDER + 'Rezonansy1_2__01012000.xlsx'
PATH_CLASSIFICATION = BASE_FOLDER + 'Rezonansy1_2_bez_LE.xlsx'
PATH_MAP = BASE_FOLDER + 'графики\\Зоны\\'

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

FIGSIZE = (8, 5)

marker_style = {
    'marker': '.',
    's': 0.3,
    'c': 'black',
    'alpha': 1,
}
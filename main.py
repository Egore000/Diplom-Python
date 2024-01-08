import time
import numpy as np
import matplotlib.pyplot as plt
from math import *
import asyncio

from itertools import product
from AnglesPy import Angles

from service import *
from mechanics import *
from params import *

plt.rcParams.update(custom_rcParams)

class Resonance:
    '''
    Класс для работы с данными о резонансах

    Параметры:
    ```
    infile: str    # путь к файлу с данными о резонансе
    outfile: str   # путь к файлу для записи элементов орбиты
    type_: str     # тип файла ('9000' - файлы из набора 9000 спутников
                   #            'NM' - файлы численной модели (ЧМ ИСЗ))
    '''
    def __init__(self, infile: str, outfile: str,  type_: str):
        self.infile = infile
        self.outfile = outfile
        
        self.path_data = path_data + '\\' + infile
        self.path_fig = path_fig
        self.path_out = path_out
        self.path_resonance = path_resonance + '\\' + infile.split('_')[1]
        self.type = type_ 

    # async def orbital(self, *args, **kwargs) -> None:
    def orbital(self, *args, **kwargs) -> None:
        '''
        Орбитальные резонансы (1 порядок)

        Параметры:
        ```
        ang: int = 0   #графики углов резонанса
        freq: int = 0   #графики частот резонанса
        pair: int = 1   #парные графики для компонент резонанса
        write: int = 0   #запись в файл (default=0)
        graph: int = 1   #графики (default=1)
        show: int = 1   #отрисовка графика (default=1)
        line: int = 0   #отрисовка линии y=0
        res: list = [1, 2, 3, 4, 5]   #построение графиков для выбранных резонансов
        grid: tuple = None   #построение сетки
        '''
        # await asyncio.sleep(0.1)
        print(f'[INFO] file: {self.path_data}')
        ang = kwargs.get('ang', 0)
        freq = kwargs.get('freq', 0)
        pair = kwargs.get('pair', 1)
        write = kwargs.get('write', 0)
        graph = kwargs.get('graph', 1)
        show = kwargs.get('show', 1)
        line = kwargs.get('line', 0)
        res = kwargs.get('res', [1, 2, 3, 4, 5])
        grid = kwargs.get('grid', None)
        plot_type = kwargs.get('plot_type', { 
            'ang': [0, 0, 0, 0, 0],
            'freq': [1, 1, 1, 1, 1],
            'pair': [0, 1]
        })
        annotate = kwargs.get('annotate', 0)

        time, coords, velocities, megno, mean_megno, date = ReadFile(self.path_data, type_=self.type)

        ecc_arr = []
        i_arr = []
        a_arr = []
        Omega_arr = []
        w_arr = []
        M_arr = []
        data = []
        F = []
        dF = []
        for idx, (x, v) in enumerate(zip(coords, velocities)):
            ecc, i, a, Omega, w, M = CoordsToElements(x, v)
            ecc_arr.append(ecc)
            i_arr.append(i)
            a_arr.append(a)
            Omega_arr.append(Omega)
            w_arr.append(w)
            M_arr.append(M)
            
            data.append({
                't': time[idx],
                'a': a,
                'ecc': ecc,
                'i': i * toDeg,
                'w': w * toDeg,
                'Omega': Omega * toDeg, 
                'M': M * toDeg,
                'MEGNO': megno[idx],
                'Mean MEGNO': mean_megno[idx]
            })

            F.append(resonance(*date[idx], M=M, Omega=Omega, w=w))
            dF.append(derivative_resonance(ecc=ecc, i=i, a=a))

        F = np.array(F)
        dF = np.array(dF)

        phi = []
        dot_phi = []
        time1 = []
        time2 = []
        for index in range(len(F[0])):
            phi.append(F[:, index])
            dot_phi.append(dF[:, index])

            pos1 = np.where(np.abs(np.diff(phi[index])) >= 240)[0] + 1
            time1.append(np.insert(time, pos1, np.nan))
            phi[index] = np.insert(phi[index], pos1, np.nan)
            
            pos2 = np.where(np.abs(np.diff(dot_phi[index])) >= 240)[0] + 1
            time2.append(np.insert(time, pos2, np.nan))
            dot_phi[index] = np.insert(dot_phi[index], pos2, np.nan)

        F = [[]] * 5
        dF = [[]] * 5
        for l in res:
            F[l-1] = phi[l-1]
            dF[l-1] = dot_phi[l-1]

        if write:
            WriteFile(self.path_out, self.outfile, data)

        if graph:
            if ang:
                params = {
                    'xlabel': 't, годы',
                    'y1label': 'Φ1, °',
                    'y2label': 'Φ2, °',
                    'y3label': 'Φ3, °',
                    'y4label': 'Φ4, °',
                    'y5label': 'Φ5, °',
                    'path': self.path_fig,
                    'graph_name': 'Орбитальные резонансы',
                    'show': show,
                    'save': autosave,
                    # 'plot_type': [1, 1, 1, 1, 1],
                    'plot_type': [0, 0, 0, 0, 0],
                    'title': 'Орбитальные резонансы',
                    'grid': grid,
                    'annotate': annotate,
                    'plot_type': plot_type['ang']
                }
                PrintCommonGraph(time1, *F, **params)
        
            if freq:
                params = {
                    'xlabel': 't, годы',
                    'y1label': "Φ'1, рад/с",
                    'y2label': "Φ'2, рад/с",
                    'y3label': "Φ'3, рад/с",
                    'y4label': "Φ'4, рад/с",
                    'y5label': "Φ'5, рад/с",
                    'path': self.path_fig,
                    'graph_name': 'Орбитальные резонансы, частоты',
                    'show': show,
                    'line': line,
                    'save': autosave,
                    'plot_type': [0, 0, 0, 0, 0],
                    'title': 'Орбитальные резонансы, частоты',
                    'grid': grid,
                    'annotate': annotate,
                    'plot_type': plot_type['freq']
                }
                PrintCommonGraph(time2, *dF, **params)
   
            if pair:
                for idx in res:
                    args = (dF[idx-1], F[idx-1])
                    time = (time2[idx-1], time1[idx-1])

                    path = self.path_fig + f'\Ф{idx+1}'
                    title = self.path_data.split('_')[1].split('.')[0]
                    
                    params = {
                        'xlabel': 't, годы',
                        'y1label': f"Ф'{idx}, рад/с",
                        'y2label': f"Φ{idx}, °",
                        'path': path,
                        'graph_name': title + f"_{idx}",
                        'show': show,
                        'save': autosave,
                        'plot_type': [0, 1],
                        'title': f'Ф{idx}',
                        'grid': grid,
                        'annotate': annotate,
                        'plot_type': plot_type['pair']
                    }
                    
                    PrintCommonGraph(time, *args, **params)
        return

    # async def second(self, *args, **kwargs) -> None:
    def second(self, *args, **kwargs) -> None:
        '''
        Вторичные резонансы
        ```
        ang: int - графики углов (default=1)
        freq: int - графики частот (default=0)
        pair: int - построение парных графиков (default=0)
        graph: int - построение графиков (default=1)
        show: int - отрисовка графиков (default=1)
        line: int - отрисовка линии у=0 (default=0)
        res: list = [1, 2, 3, 4, 5] - набор резонансов для построения
        grid: построение сетки
        '''
        ang = kwargs.get('ang', 1)
        freq = kwargs.get('freq', 0)
        pair = kwargs.get('pair', 0)
        graph = kwargs.get('graph', 1)
        show = kwargs.get('show', 1)
        line = kwargs.get('line', 0)
        res = kwargs.get('res', [1, 2, 3, 4, 5])
        grid = kwargs.get('grid', None)
        plot_type = kwargs.get('plot_type', {
            'ang': [0, 0, 0, 0, 0],
            'freq': [1, 1, 1, 1, 1],
            'pair': [0, 1]
        })
        annotate = kwargs.get('annotate', False)
        

        time, F, dF = ReadResonance(self.path_resonance)
        
        F = np.array(F)
        dF = np.array(dF)

        phi = []
        dot_phi = []
        time1 = []
        time2 = []
        for index in range(len(F)):
            phi.append(F[index, :])
            dot_phi.append(dF[index, :])

            pos1 = np.where(np.abs(np.diff(phi[index])) >= 240)[0] + 1
            time1.append(np.insert(time, pos1, None))
            phi[index] = np.insert(phi[index], pos1, None)
            
            pos2 = np.where(np.abs(np.diff(dot_phi[index])) >= 240)[0] + 1
            time2.append(np.insert(time, pos2, None))
            dot_phi[index] = np.insert(dot_phi[index], pos2, None)

        F = [[]] * 5
        dF = [[]] * 5
        for l in res:
            F[l-1] = phi[l-1]
            dF[l-1] = dot_phi[l-1]

        if graph:
            if ang:
                params = {
                    'xlabel': 't, годы',
                    'y1label': 'Φ1, °',
                    'y2label': 'Φ2, °',
                    'y3label': 'Φ3, °',
                    'y4label': 'Φ4, °',
                    'y5label': 'Φ5, °',
                    'path': self.path_fig,
                    'graph_name': 'Вторичные резонансы',
                    'show': show,
                    'save': autosave,
                    # 'plot_type': [0, 0, 0, 0, 0],
                    'plot_type': plot_type['ang'],
                    'title': 'Вторичные резонансы',
                    'grid': grid,
                    'annotate': annotate,
                }
                PrintCommonGraph(time1, *F, **params)
            if freq:
                params = {
                    'xlabel': 't, годы',
                    'y1label': "Φ'1, рад/с",
                    'y2label': "Φ'2, рад/с",
                    'y3label': "Φ'3, рад/с",
                    'y4label': "Φ'4, рад/с",
                    'y5label': "Φ'5, рад/с",
                    'path': self.path_fig,
                    'graph_name': 'Вторичные резонансы, частоты',
                    'show': show,
                    'line': line,
                    'save': autosave,
                    'plot_type': plot_type['freq'],
                    'title': 'Вторичные резонансы, частоты',
                    'grid': grid,
                    'annotate': annotate,
                }
                PrintCommonGraph(time2, *dF, **params)
            
            if pair:
                for idx in res:
                    args = (dF[idx-1], F[idx-1])
                    time = (time2[idx-1], time1[idx-1])
                    path = self.path_fig + f'\Ф{idx}'
                    title = self.path_data.split('_')[1].split('.')[0]

                    params = {
                        'xlabel': 't, годы',
                        'y1label': f"Ф'{idx}, рад/с",
                        'y2label': f"Φ{idx}, °",
                        'path': path,
                        'graph_name': title + f'_{idx}',
                        'show': show,
                        'path': path,
                        'line': line,
                        'save': autosave,
                        # 'plot_type': [0, 1],
                        'plot_type': plot_type['pair'],
                        'title': f'Ф{idx}',
                        'grid': grid,
                        'annotate': annotate,
                    }

                    PrintCommonGraph(time, *args, **params)


async def gather_data():
    list_file = os.listdir(path_data)
    
    tasks = []
    for num, dat in enumerate(list_file[:2]):
        res = Resonance(dat, f'elements_{num}.csv', type_='9000')
        task = asyncio.create_task(res.orbital(write=0, graph=1))
        tasks.append(task)

    await asyncio.gather(*tasks)

@timer
def main():
    # asyncio.run(gather_data())
    res = Resonance('EPH_0010.DAT', 'elements.csv', type_='9000')
    res.orbital(
        ang=0, 
        freq=0, 
        pair=1, 
        plot_type={
            'ang': [1] * 5,
            'freq': [0] * 5,
            'pair': [0, 1]
        }, 
        annotate=1,
        res=[1, 5],
        show=0)
    
    res.second(
        ang=0, 
        freq=0, 
        pair=1, 
        plot_type={
            'ang': [1] * 5,
            'freq': [0] * 5,
            'pair': [0, 1]
        }, 
        annotate=0,
        res=[1, 5],
        show=0)

if __name__=="__main__":
    main()
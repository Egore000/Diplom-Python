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

start_time = time.time()

autosave = 0
plt.rcParams.update(custom_rcParams)

class Resonance:
    def __init__(self, infile: str, outfile: str,  type_: str):
        self.infile = infile
        self.outfile = outfile
        
        self.path_data = path_data + '\\' + infile
        self.path_fig = path_fig
        self.path_out = path_out
        self.path_resonance = path_resonance
        self.type = type_ 

    # def orbital(self, ang=0, freq=0, pair=1, write=0, graph=1) -> None:
    async def orbital(self, ang=0, freq=0, pair=1, write=0, graph=1) -> None:
        # await asyncio.sleep(0.1)
        print(f'[INFO] file: {self.path_data}')
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

        F1 = F[:, 0]
        F2 = F[:, 1]
        F3 = F[:, 2]
        F4 = F[:, 3]
        F5 = F[:, 4]
        
        # self.checker(time, F1)

        dF1 = dF[:, 0]
        dF2 = dF[:, 1]
        dF3 = dF[:, 2]
        dF4 = dF[:, 3]
        dF5 = dF[:, 4]

        i_arr = list(map(Degree, i_arr))
        Omega_arr = list(map(Degree, Omega_arr))
        w_arr = list(map(Degree, w_arr))
        M_arr = list(map(Degree, M_arr))

        F = (F1, F2, F3, F4, F5)
        dF = (dF1, dF2, dF3, dF4, dF5)
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
                }
                PrintCommonGraph(time, self.path_fig, *F, save=autosave, plot_type=[1, 1, 1, 1, 1], title='Орбитальные резонансы', **params)
        
            if freq:
                params = {
                    'xlabel': 't, годы',
                    'y1label': "Φ'1, рад/с",
                    'y2label': "Φ'2, рад/с",
                    'y3label': "Φ'3, рад/с",
                    'y4label': "Φ'4, рад/с",
                    'y5label': "Φ'5, рад/с",
                    'path': self.path_fig,
                    'graph_name': 'Орбитальные резонансы, частоты'
                }
                PrintCommonGraph(time, *dF, save=autosave, plot_type=[0, 0, 0, 0, 0], title='Орбитальные резонансы, частоты', line=1, **params)
   
            if pair:
                for idx in range(len(F)):
                    args = (dF[idx], F[idx])

                    path = self.path_fig + f'\Ф{idx+1}'
                    title = self.path_data.split('_')[1].split('.')[0]
                    
                    params = {
                        'xlabel': 't, годы',
                        'y1label': f"Ф'{idx+1}, рад/с",
                        'y2label': f"Φ{idx+1}, °",
                        'path': path,
                        'graph_name': title + f"_{idx+1}"
                    }

                    PrintCommonGraph(time, *args, save=autosave, plot_type=[0, 1], title=f'Ф{idx+1}', line=0, **params)
        return

    def second(self, ang=1, freq=0, graph=1, pair=0) -> None:
    # async def second(self, ang=1, freq=0, graph=1, pair=0) -> None:
        time, F, dF = ReadResonance(self.path_resonance)
        # PrintGraph(time, dF[0], title='Вторичный резонанс', legend='Ф1', save=autosave)
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
                    'graph_name': 'Вторичные резонансы'
                }
                PrintCommonGraph(time, *F, save=autosave, plot_type=[1, 1, 1, 1, 1], title='Вторичные резонансы', **params)
            if freq:
                params = {
                    'xlabel': 't, годы',
                    'y1label': "Φ'1, рад/с",
                    'y2label': "Φ'2, рад/с",
                    'y3label': "Φ'3, рад/с",
                    'y4label': "Φ'4, рад/с",
                    'y5label': "Φ'5, рад/с",
                    'path': self.path_fig,
                    'graph_name': 'Вторичные резонансы, частоты'
                }
                PrintCommonGraph(time, *dF, save=autosave, plot_type=[0, 0, 0, 0, 0], title='Вторичные резонансы, частоты', line=0, **params)
            
            if pair:
                for idx in range(len(F)):
                    args = (dF[idx], F[idx])
                    path = self.path_fig + f'\Ф{idx+1}'
                    title = self.path_data.split('_')[1].split('.')[0]

                    params = {
                        'xlabel': 't, годы',
                        'y1label': f"Ф'{idx+1}, рад/с",
                        'y2label': f"Φ{idx+1}, °",
                        'path': path,
                        'graph_name': title + f'_{idx}'
                    }

                    PrintCommonGraph(time, path, *args, save=autosave, plot_type=[0, 1, 1], title=f'Ф{idx+1}', line=0, **params)


    def checker(self, x: list, y: list) -> bool:
        list1 = [x for x in range(0, 26, 5)]
        list2 = [x for x in range(5, 31, 5)]

        list3 = [x for x in range(0, 351, 50)]
        list4 = [x for x in range(50, 401, 50)]

        rect_x = list(zip(list1, list2))
        rect_y = list(zip(list3, list4))

        lenght = len(rect_x)

        matrix = {}
        for elem in product(rect_x, rect_y):
            matrix[elem[0] + elem[1]] = 0
        
        
        for t, v in zip(x, y):
            for elem in product(rect_x, rect_y):
                x_min = elem[0][0]
                x_max = elem[0][1]
                y_min = elem[1][0]
                y_max = elem[1][1]

                if x_min <= t < x_max and y_min <= v < y_max:
                    try:
                        matrix[elem[0] + elem[1]] += 1
                    except KeyError:
                        matrix[elem[0] + elem[1]] = 1

        if 0 in matrix.values():
            print('non-circular')
        else:
            print('circular')

        print(matrix)

async def gather_data():
    list_file = os.listdir(path_data)
    
    tasks = []
    for num, dat in enumerate(list_file[:100]):
        res = Resonance(dat, f'elements_{num}.csv', type_='9000')
        task = asyncio.create_task(res.orbital(write=1, graph=0))
        tasks.append(task)

    await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())

    # list_file = os.listdir(path_data)
    # for num, dat in enumerate(list_file[:100]):
    #     res = Resonance(dat, f'elements_{num}.csv', type_='9000')
    #     res.orbital(write=1, graph=0)

    print(f'[TIME] {time.time() - start_time}')
    # count = 0
    # res = Resonance('EPH_7569.DAT', 'elements.csv', type_='9000')
    # res.orbital(write=0, graph=1)
    # res.checker([3, 4, 5, 6], [8.5, 9, 12, 44])
    # plt.show()

if __name__=="__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt
from service import *
from math import *
from mechanics import *
from AnglesPy import Angles
from params import *

autosave = 0
plt.rcParams.update(custom_rcParams)

class Resonance:
    def __init__(self, infile: str, outfile: str,  type_):
        self.infile = infile
        self.outfile = outfile
        
        self.path_data = path_data + '\\' + infile
        self.path_fig = path_fig
        self.path_out = path_out
        self.path_resonance = path_resonance
        self.type = type_ 

    def Orbital(self, write=0, graph=1) -> None:
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
        for idx in range(len(coords)):
            ecc, i, a, Omega, w, M = CoordsToElements(coords[idx], velocities[idx])
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
        
        dF1 = dF[:, 0]
        dF2 = dF[:, 1]
        dF3 = dF[:, 2]
        dF4 = dF[:, 3]
        dF5 = dF[:, 4]

        i_arr = list(map(Degree, i_arr))
        Omega_arr = list(map(Degree, Omega_arr))
        w_arr = list(map(Degree, w_arr))
        M_arr = list(map(Degree, M_arr))

        if write:
            WriteFile(self.path_out, self.outfile, data)

        if graph:
            params = {
            'xlabel': 't, годы',
            'y1label': 'Φ1, °',
            'y2label': 'Φ2, °',
            'y3label': 'Φ3, °',
            'y4label': 'Φ4, °',
            'y5label': 'Φ5, °'
            }
            args = (F1, F2, F3, F4, F5)
            PrintCommonGraph(time, self.path_fig, *args, save=autosave, plot_type=[1, 1, 1, 1, 1], title='Орбитальные резонансы', **params)
        
            params = {
                'xlabel': 't, годы',
                'y1label': "Φ'1, рад/с",
                'y2label': "Φ'2, рад/с",
                'y3label': "Φ'3, рад/с",
                'y4label': "Φ'4, рад/с",
                'y5label': "Φ'5, рад/с"
            }
            args = (dF1, dF2, dF3, dF4, dF5)
            PrintCommonGraph(time, self.path_fig, *args, save=autosave, plot_type=[0, 0, 0, 0, 0], title='Орбитальные резонансы, частоты', line=1, **params)
        return

    def Second(self, ang=1, freq=0, graph=1, pair=0) -> None:
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
                    'y5label': 'Φ5, °'
                }
                PrintCommonGraph(time, self.path_fig, *F, save=autosave, plot_type=[1, 1, 1, 1, 1], title='Вторичные резонансы', **params)
            if freq:
                params = {
                    'xlabel': 't, годы',
                    'y1label': "Φ'1, рад/с",
                    'y2label': "Φ'2, рад/с",
                    'y3label': "Φ'3, рад/с",
                    'y4label': "Φ'4, рад/с",
                    'y5label': "Φ'5, рад/с"
                }
                PrintCommonGraph(time, self.path_fig, *dF, save=autosave, plot_type=[0, 0, 0, 0, 0], title='Вторичные резонансы, частоты', line=0, **params)
            
            if pair:
                for idx in range(len(F)):
                    params = {
                        'xlabel': 't, годы',
                        'y1label': f"Ф'{idx+1}, рад/с",
                        'y2label': f"Φ{idx+1}, °",
                    }
                    args = (dF[idx], F[idx])
                    PrintCommonGraph(time, self.path_fig, *args, save=autosave, plot_type=[0, 1, 1], title=f'Ф{idx+1}', line=0, **params)



def main():
    # list_file = os.listdir(path_data)
    # count = 0
    # for dat in list_file[:3]:
    #     print(dat)
    #     count += 1
    #     Orbital_resonance(path_data=path_data + '\\' + dat, 
    #                     path_fig=path_fig + f'\{count}',
    #                     path_out=path_out + f'\{count}', 
    #                     write=0, 
    #                     graph=1)
        # args = ReadFile(path_data + '\\' + dat)

    # Second_resonance(path_resonance, ang=0, freq=0, pair=1)

    res = Resonance('EPH_0001.DAT', 'elements.csv', type_='9000')
    res.Orbital(write=1, graph=1)

    plt.show()
    return

if __name__=="__main__":
    main()
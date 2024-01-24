import os
import time
import matplotlib.pyplot as plt
import csv
import numpy as np

import params

class Filer:
    def __init__(self, path: str, path2: str, path_out):
        self.path = path
        self.path2 = path2
        self.path_out = path_out


    def ReadResonance(self) -> tuple[list[float], list[float], list[float]]:
        '''
        Считывание данных о вторичных резонансах из файла
        path - путь к файлу 

        Возращает (time, Ф, Ф'): tuple
        * time - время
        * Ф - критический аргумент
        * Ф' - частота вторичного резонанса
        '''
        time = []
        F = ([], [], [], [], [])
        dF = ([], [], [], [], [])
        with open(self.path2, 'r') as data:
            i = 0
            for line in data:
                if i == 0:
                    i += 1  
                    continue
                line = list(filter(bool, line.strip().split(' ')))

                if len(line) != 11:
                    break

                time.append(float(line[0]))
                for i in range(1, 6):
                    F[i-1].append(float(line[i]))
                    dF[i-1].append(float(line[i+5]))
        return time, F, dF


    def ReadFile(self, type_='NM') -> tuple[list[float] | float]:
        '''
        Чтение данных из path
        Возрвращает следующие данные:
        * time - время
        * coords - координаты
        * velocities - скорости
        * megno - параметр MEGNO
        * mean_megno - осреднённый MEGNO
        * data - даты наблюдений
        '''
        time = []
        date = []
        coords = []
        velocities = []
        lines = []
        megno = []
        mean_megno = []
        with open(self.path, 'r') as data:
            for line in data:
                line = line.strip().split(' ')
                line_clear = [x for x in line if x != '']
                lines.append(line_clear)
            
            for i in range(0, len(lines), 3):
                line1 = lines[i]
                line2 = lines[i+1]
                line3 = lines[i+2]
            
                time.append(float(line1[1])/(86400*365))
                if type_ == "NM":
                    date.append((int(line1[4]), int(line1[5]), int(line1[6])))
                else:
                    date.append((int(line1[3]), int(line1[4]), int(line1[5])))
                
                x = float(line2[1])
                y = float(line2[2])
                z = float(line2[3])
                megno.append(float(line2[4]))

                Vx = float(line3[0])
                Vy = float(line3[1])
                Vz = float(line3[2])
                mean_megno.append(float(line3[3]))

                coords.append((x, y ,z))
                velocities.append((Vx, Vy, Vz))
        return time, coords, velocities, megno, mean_megno, date


    def WriteFile(self, filename: str, data: dict) -> None:
        '''
        Запись данных из data в .csv файл по пути path 
        '''
        if not os.path.exists(self.path_out):
            os.makedirs(self.path_out)

        with open(self.path_out + '\\' + filename, 'w', newline='') as outfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()
            writer.writerows(data)


class Grapher:

    @staticmethod
    def PrintGraph(x: list, y: list, **kwargs) -> None:
        '''
        Отрисовка графика
        Параметры:
        * x - массив абсцисс
        * y - массив ординат
        * path - путь к директории для сохранения
        * title - название графика (и файла в случае сохранения)
        * legend - подпись к оси Oy
        * save - метка о сохранении файла
        '''
        path = kwargs.get('path')
        title = kwargs.get('title', 'График')
        legend = kwargs.get('legend', 'Легенда')
        save = kwargs.get('save', params.autosave)
        show = kwargs.get('show', 1)
        figsize = kwargs.get('figsize', params.FIGSIZE)
        plot_type = kwargs.get('plot_type', 1)
        marker = kwargs.get('marker', params.marker_style)

        if save and not os.path.exists(path):
            os.makedirs(path)
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)

        if plot_type:
            plt.scatter(x, y, **marker)
        else:
            ax.plot(x, y, color=plt.rcParams['lines.color'])
        plt.title(title)
        plt.xlabel('t, годы')
        plt.ylabel(legend)
        plt.grid()
        if save:
            plt.savefig(path + f'\{title}.png')
        if show:
            mngr = plt.get_current_fig_manager()
            mngr.window.geometry('+0+0')
            plt.show()


    @staticmethod
    def PrintCommonGraph(x: list, *args, **kwargs):
        '''
        Отрисовка группового графика
        * x - массив абсцисс
        * path - путь к директории для сохранения
        * *args - кортеж данных
        * plot_type - метка о типе графика (0 - plot, 1 - scatter)
        * **kwargs - словарь доп.параметров в формате:
            **params = {
                'xlabel': 'x',
                'y1label': 'y1',
                'y2label': 'y2',
                ...,
                'title': 'title',
                'line': int (default=0),
                'save': int (default=1),
                'plot': list (default=[1])
                'grid': tuple (default=None)
            } 
        '''
        path = kwargs.get('path')
        plot_type = kwargs.get('plot_type', [1] * len(args))
        line = kwargs.get('line', 0)
        save = kwargs.get('save', 1)
        grid = kwargs.get('grid', None)
        annotate = kwargs.get('annotate', False)
        figsize = kwargs.get('figsize', params.FIGSIZE)
        show = kwargs.get('show', None)
        marker = kwargs.get('marker', params.marker_style)

        if save and path and not os.path.exists(path):
            os.makedirs(path)

        fig = plt.figure(figsize=figsize)
        ax = fig.subplots(len(args), 1)
        
        if len(args) == 1:
            ax = [ax]

        idx = 0

        def enum(x):
            i = 0
            y = []
            for item in x:
                if np.isnan(item):
                    y.append(('', np.nan))
                else:
                    y.append((i, item)) 
                    i += 1
            return y               

        for axes in ax:
            text = list(zip(*enum(x[idx])))[0]

            if plot_type[idx] == 0:
                axes.plot(x[idx], args[idx], color=plt.rcParams['lines.color'])
            else:
                axes.scatter(x[idx], args[idx], **marker)

            if annotate:
                for i in range(len(text)):
                    axes.annotate(text[i], (x[idx][i], args[idx][i] + 0.2), size=4)

            if line:
                axes.plot([min(x[idx]), max(x[idx])], [0, 0], color=plt.rcParams['lines.color'])
        
            if grid:
                x_points = np.linspace(-2, int(max(x[idx])) + 2, grid[0])
                y_points = np.linspace(-2, int(max(args[idx])) + 2, grid[1])
                axes.set_xticks(x_points, minor=True)
                axes.set_yticks(y_points, minor=True)
                axes.grid(which='both')

            axes.set_ylabel(kwargs.get(f'y{idx+1}label', f'y{idx+1}'))
            
            if idx % 2 == 1:
                axes.yaxis.tick_right()
            idx += 1
            axes.grid()

        ax[idx-1].set_xlabel(kwargs.get('xlabel', 'x'))
                
        title = kwargs.get('title', 'Общий график')
        fig.suptitle(title)

        graph_name = kwargs.get('graph_name', 'Общий график')
        if save:
            plt.savefig(path + f'\{graph_name}.png')

        if show:
            mngr = plt.get_current_fig_manager()
            mngr.window.geometry('+0+0')
            plt.show()
        # plt.close(fig)
        # plt.clf()
        # plt.cla()
        return


    @staticmethod
    def PrintMap(data, *args, **kwargs) -> None:
        '''
        Отрисовка зон действия резонансов
        * res - Зоны резонансов 1 порядка
        * sec_plus - Зоны вторичных резонансов со знаком +
        * sec_minus - Зоны вторичных резонансов со знаком -
        '''
        res = kwargs.get('res', True)
        sec_plus = kwargs.get('sec_plus', True)
        sec_minus = kwargs.get('sec_minus', True)
        marker = kwargs.get('marker', 's')
        size = kwargs.get('s', 10)
        color = kwargs.get('colors', ['#FFFFFF', '#F0F0F0', '#A0A0A0'])
        save = kwargs.get('save', params.autosave)
        show = kwargs.get('show', 1)
        path = kwargs.get('path', params.PATH_MAP)
        figsize = kwargs.get('figsize', (13, 7))
        
        if save and path and not os.path.exists(path):
            os.makedirs(path)

        arguments = {
            'Орбитальные резонансы': ['Ф1', 'Ф2', 'Ф3', 'Ф4', 'Ф5'],
            'Вторичные резонансы (+)': ['Ф1s+', 'Ф2s+', 'Ф3s+', 'Ф4s+', 'Ф5s+'],
            'Вторичные резонансы (-)': ['Ф1s-', 'Ф2s-', 'Ф3s-', 'Ф4s-', 'Ф5s-']
        }

        resonance_types = []

        if res:
            resonance_types.append("Орбитальные резонансы")
        if sec_plus:
            resonance_types.append("Вторичные резонансы (+)")
        if sec_minus:
            resonance_types.append("Вторичные резонансы (-)")


        for resonance_type in resonance_types:
            fig = plt.figure(figsize=figsize)
            ax = fig.subplots(3, 2)
            fig.delaxes(ax[2, 1])
            
            if save and path and not os.path.exists(path):
                os.makedirs(path)

            row = 0
            col = 0
            for arg in arguments[resonance_type]:
                df = data[['Номер папки', 'номер файла', 'а, км', 'i, град', arg]]

                circular = df[df[arg] == 0.]
                libration = df[df[arg] == 1.]
                mixed = df[df[arg] == 2.]

                ax[row, col].scatter(circular['i, град'], circular['а, км'], marker=marker, color=color[0], s=size)
                ax[row, col].scatter(libration['i, град'], libration['а, км'], marker=marker, color=color[1], s=size)
                ax[row, col].scatter(mixed['i, град'], mixed['а, км'], marker=marker, color=color[2], s=size)
                ax[row, col].set_ylabel('a, км')
                ax[row, col].set_xlabel('i, град')
                ax[row, col].set_title(arg)

                row += 1

                if row % 3 == 0:
                    row = 0
                    col += 1

            plt.tight_layout()
            
            if save:
                plt.savefig(path + f'\\{resonance_type}.png')
            if show:
                mngr = plt.get_current_fig_manager()
                mngr.window.geometry('+0+0')
                plt.show()
            else:
                plt.close(fig)
        return


def timer(func):
    '''
    Декоратор для измерения времени работы функции
    '''
    def wrap():
        start_time = time.time()
        func()
        finish_time = time.time()
        runtime = finish_time - start_time
        print(f'[TIME] runtime: {runtime:.2f} c')
    return wrap

if __name__=="__main__":
    import pandas as pd

    data = pd.read_excel(params.PATH_CLASSIFICATION)

    plt.rcParams.update(params.custom_rcParams)
    # Grapher.PrintCommonGraph(([1, 2, 3], [1, 2, 3], [1, 3, 5]), *([1, 2, 0], [1, 0, 1], [1, 3, 5]), plot_type=[0] * 5, show=1, save=0)
    # Grapher.PrintGraph([1, 2, 3], [0, 10, 20], plot_type=1)
    Grapher.PrintMap(data, res=True, sec_plus=True, sec_minus=True, save=0)
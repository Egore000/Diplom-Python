import matplotlib.pyplot as plt
import csv
import params
import os


def ReadResonance(path: str) -> tuple[float]:
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
    with open(path, 'r') as data:
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

def ReadFile(path: str, type_='NM') -> tuple[list[float] | float]:
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
    with open(path, 'r') as data:
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

def WriteFile(path: str, filename: str, data: dict) -> None:
    '''
    Запись данных из data в .csv файл по пути path 
    '''
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + '\\' + filename, 'w', newline='') as outfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        writer.writerows(data)


def PrintGraph(x: list, y: list, path: str, title: str, legend: str, save=1) -> None:
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
    if not os.path.exists(path):
        os.makedirs(path)
    
    fig = plt.figure()
    mngr = plt.get_current_fig_manager()
    mngr.window.geometry('+0+0')

    # plt.scatter(x, y, s=0.3, alpha=0.5)
    plt.plot(x, y, color=plt.rcParams['lines.color'])
    plt.title(title)
    plt.xlabel('t, годы')
    plt.ylabel(legend)
    plt.grid()
    if save:
        plt.savefig(path + f'\{title}.png')


def PrintCommonGraph(x: list, *args, save=1, plot_type=[1], line=1, **kwargs):
    '''
    Отрисовка группового графика
    * x - массив абсцисс
    * path - путь к директории для сохранения
    * *args - кортеж данных
    * save - метка о сохранении файла
    * plot_type - метка о типе графика (0 - plot, 1 - scatter)
    * line - метка о линии нуля (0 - нет, 1 - да)
    * **kwargs - словарь доп.параметров в формате:
        **params = {
            'xlabel': 'x',
            'y1label': 'y1',
            'y2label': 'y2',
            ...,
            'title': 'title',
        } 
    '''
    path = kwargs.get('path')
    if not os.path.exists(path):
        os.makedirs(path)

    fig = plt.figure(figsize=(7, 6))
    ax = fig.subplots(len(args), 1)
    idx = 0
    for axes in ax:
        if plot_type[idx] == 0:
            plot = axes.plot(x, args[idx], color=plt.rcParams['lines.color'])
        else:
            plot = axes.scatter(x, args[idx], s=0.3, c='black')

        if line:
            l = axes.plot([min(x), max(x)], [0, 0], color=plt.rcParams['lines.color'])
    
        axes.set_ylabel(kwargs.get(f'y{idx+1}label', f'y{idx+1}'))
        
        if idx % 2 == 1:
            axes.yaxis.tick_right()
        idx += 1
        axes.grid()

    ax[idx-1].set_xlabel(kwargs.get('xlabel', 'x'))
            
    title = kwargs.get('title', 'Общий график')
    fig.suptitle(title)


    graph_name = kwargs.get('graph_name')
    if save:
        plt.savefig(path + f'\{graph_name}.png')

    mngr = plt.get_current_fig_manager()
    mngr.window.geometry('+0+0')

    # plt.close(fig)
    # plt.clf()
    # plt.cla()


if __name__=="__main__":
    # PrintCommonGraph([1, 2, 3], [2, 3, 4], [1, 4, 2], [0,1,10])
    # t, F, dF = ReadResonance(r'C:\Users\egorp\Desktop\диплом\файлы\Pascal\Вторичные резонансы.dat')
    list_file = os.listdir(params.path_data)

    for dat in list_file[:1]:
        args = ReadFile(params.path_data + "\\" + dat)
        print(args[0])
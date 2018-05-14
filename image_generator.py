# coding=utf-8
from PIL import Image, ImageEnhance
import os
import sys
from multiprocessing.spawn import set_executable
import multiprocessing
from tqdm import tqdm
import re

top_offset = 5
left_offset = 5

img_re = re.compile('([^/]*)\.([^.]*)')
path_re = re.compile('(.*)/([^/]*)')
executable = sys.executable
application_path = path_re.match(executable)[1]

mask = Image.open(application_path + '/mask.png')
empty = Image.open(application_path + '/empty.png')
alpha_gradient = Image.open(application_path + '/alfa.png')

COLORS = {"Кармин": "960018", "Кардинал": "c41e3a", "Тициановый": "d53e07", "Красный": "ff0000", "Алый": "ff2400",
          "Карминово-красный": "ff0033", "Киноварь": "ff4d00", "Международный оранжевый": "ff4f00",
          "Ализариновый": "e32636", "Малиновый": "dc143c", "Каштановый": "cd5c5c", "Темно-коралловый": "cd5b45",
          "Морковный": "f36223", "Сиена жженая": "e97451", "Коралловый": "ff7f50", "Лососевый": "ff8c69",
          "Темно-лососевый": "e9967a", "Оранжево-розовый": "ff9966", "Сомон": "efaf8c", "Розовый": "ffc0cb",
          "Бледно-розовый": "fadadd", "Розовато-лавандовый": "fff0f5", "Бледно-песочный": "fdeaa8",
          "Циннвальдитовый": "ebc2af", "Бледно-коричневый": "987654", "Темно-каштановый": "986960",
          "Красновато-коричневый": "755a57", "Кофейный": "442d25", "Бистр": "3d2b1f", "Темно-коричневый": "654321",
          "Коричный": "7b3f00", "Медвежьего ушка": "834d18", "Сепия": "704214", "Умбра": "734a12",
          "Кирпичный": "884535", "Терракотовый": "904d30", "Коричневый": "964b00", "Камелопардовый": "a25f2a",
          "Краснобуро-оранжевый": "cd5700", "Выгоревший оранжевый": "cc5500", "Шоколадный": "d2691e", "Охра": "cc7722",
          "Медный": "b87333", "Светло-коричневый": "cd853f", "Ванильный": "d5713f", "Рыжий": "d77d31",
          "Бронзовый": "cd7f32", "Темно-золотой": "b8860b", "Золотисто-березовый": "daa520", "Гуммигут": "e49b0f",
          "Сиена": "e28b00", "Темно-мандариновый": "ea7500", "Тыквенный": "ff7518", "Последний вздох Жако": "ff9218",
          "Мандариновый": "ff8800", "Сигнальный оранжевый": "ff9900", "Оранжевый": "ffa500",
          "Отборный желтый": "ffba00", "Янтарный": "ffbf00", "Яндекса": "ffcc00",
          "Желтого школьного автобуса": "ffd800", "Золотистый": "ffd700", "Горчичный": "ffdb58", "Песочный": "fcdd76",
          "Кожи буйвола": "f0dc82", "Старого льна": "eedc82", "Оранжево-персиковый": "ffcc99", "Белый навахо": "ffdead",
          "Темно-персиковый": "ffdab9", "Желто-персиковый": "fadfad", "Пшеничный": "f5deb3", "Персиковый": "ffe5b4",
          "Желто-розовый": "ffe4b2", "Побега папайи": "ffefd5", "Морской пены": "fff5ee", "Белый": "ffffff",
          "Бежевый": "f5f5dc", "Льняной": "faf0e6", "Бедра испуганной нимфы": "faeedd", "Сливочный": "f2e8c9",
          "Пергидрольной блондинки": "eee6a3", "Желто-коричневый": "d2b48c", "Шамуа": "a08040",
          "Темный желто-коричневый": "918151", "Хаки": "806b2a", "Темный хаки": "4c3c18", "Оливковый": "808000",
          "Нежно-оливковый": "6b8e23", "Латунный": "b5a642", "Темно-грушевый": "d8a903", "Старого золота": "cfb53b",
          "Шафрановый": "f4c430", "Грушевый": "efd334", "Желтый": "ffff00", "Лимонный": "fde910",
          "Детской неожиданности": "f7f21a", "Кукурузный": "fbec5d", "Вердепешевый": "dad871",
          "Лимонно-кремовый": "fffacd", "Слоновой кости": "fffddf", "Кремовый": "f2ddc6",
          "Серого зеленого чая": "cadaba", "Болотный": "acb78e", "Cпаржи": "7ba05b", "Защитный": "78866b",
          "Темно-оливковый": "556832", "Зеленого папоротника": "4f7942", "Травяной": "5da130",
          "Влюбленной жабы": "3caa3c", "Вердепомовый": "34c924", "Зеленый": "00ff00", "Ярко-зеленый": "66ff00",
          "Ядовито-зеленый": "7fff00", "Лаймовый": "ccff00", "Фисташковый": "bef574", "Желто-зеленый": "adff2f",
          "Салатовый": "99ff99", "Зеленой мяты": "98ff98", "Зеленого чая": "d0f0c0", "Темного зеленого чая": "badbad",
          "Зеленого мха": "addfad", "Серо-зеленый": "ace1af", "Бледно-зеленый": "77dd77", "Зелено-морской": "2e8b57",
          "Темно-зеленый": "013220", "Красного моря": "1f4037", "Темный весенне-зеленый": "177245",
          "Нефритовый": "00a86b", "Изумрудный": "50c878", "Темный пастельно-зеленый": "03c03c", "Малахитовый": "0bda51",
          "Весенне-зеленый": "00ff7f", "Аквамариновый": "7fffd4", "Панг": "c7fcec", "Лягушки в обмороке": "7b917b",
          "Маренго": "4c5866", "Серой спаржи": "465945", "Аспидно-серый": "2f4f4f", "Темно-бирюзовый": "116062",
          "Мурена": "1c6b72", "Зеленой сосны": "01796f", "Cине-зеленый": "008080", "Яйца дрозда": "00cccc",
          "Бирюзовый": "30d5c8", "Ярко-бирюзовый": "08e8de", "Циан": "00ffff", "Электрик": "7df9ff",
          "Бледно-синий": "afeeee", "Серебристый": "c0c0c0", "Светло-серый": "bbbbbb", "Кварцевый": "99958c",
          "Серого шифера": "708090", "Серый": "808080", "Мокрого асфальта": "505050", "Антрацитовый": "464451",
          "Черный": "000000", "Берлинской лазури": "003153", "Сапфировый": "082567", "Полуночно-синий": "003366",
          "Темно-синий": "000080", "Ультрамариновый": "120a8f", "Синей пыли": "003399", "Темно-лазурный": "08457e",
          "Черного моря": "1a4780", "Синий": "0000ff", "Кобальтовый": "0047ab", "Лазурно-синий": "2a52be",
          "Джинсовый": "1560bd", "Королевский синий": "4169e1", "Лазурно-серый": "007ba7", "Синий Клейна": "3a75c4",
          "Синей стали": "4682b4", "Воды пляжа Бонди": "0095b6", "Лазурный": "007fff", "Морской волны": "008cf0",
          "Защитно-синий": "1e90ff", "Голубой": "42aaff", "Васильковый": "6495ed", "Сизый": "79a0c1",
          "Ниагара": "9db1cc", "Небесный": "7fc7ff", "Бледно-васильковый": "abcdef", "Барвинковый": "ccccff",
          "Гридеперлевый": "c7d0cc", "Бороды Абдель-Керима": "d5d5d5", "Лавандовый": "e6e6fa",
          "Чертополоховый": "d8bfd8", "Сиреневый": "c8a2c8", "Глициниевый": "c9a0dc", "Аметистовый": "9966cc",
          "Серобуромалиновый": "735184", "Фиолетовый": "8b00ff", "Персидский синий": "6600ff",
          "Темно-фиолетовый": "423189", "Темный индиго": "310062", "Индиго": "4b0082", "Темно-пурпурный": "660099",
          "Сливовый": "660066", "Фиолетово-баклажанный": "991199", "Орхидеевый": "da70d6", "Гелиотроповый": "df73ff",
          "Фиалковый": "ea8df7", "Бледно-пурпурный": "f984e5", "Фуксии": "f754e1", "Звезды в шоке": "ff47ca",
          "Пурпурный": "ff00ff", "Ярко-розовый": "fc0fc0", "Ярко-фиолетовый": "cd00cd", "Баклажановый": "990066",
          "Вишневый": "911e42", "Розовато-лиловый": "993366", "Фиолетово-красный": "c71585",
          "Светло-вишневый": "de3163", "Темно-розовый": "e75480", "Лиловый": "db7093", "Бледно-каштановый": "ddadaf",
          "Пюсовый": "cc8899", "Розовый Маунтбэттена": "997a8d", "Бледный розовато-лиловый": "996666",
          "Умбра жженая": "8a3324", "Блошиного брюшка": "4e1609", "Бурый": "45161c", "Темно-алый": "560319",
          "Бургундский": "900020", "Коричнево-малиновый": "800000", "Сангиновый": "92000a", "Бисмарк-фуриозо": "a5260a",
          "Бордовый": "9b2d30", "Бледно-карминный": "af4035", "Ржаво-коричневый": "b7410e"}
_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x + y for x in _NUMERALS for y in _NUMERALS)}
LOWERCASE, UPPERCASE = 'x', 'X'


def rgb(triplet):
    return [_HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]]


def generate_colors(step=5):
    for red in range(0, 256, step):
        for green in range(0, 256, step):
            for blue in range(0, 256, step):
                yield [red, green, blue, f'{red}-{green}-{blue}']


def get_colors(step=5):
    colors_list = []
    try:
        listdir = os.listdir(application_path + '/imgs')
        for _filename in listdir:
            filename = img_re.match(_filename)
            if not _filename.startswith("."):
                try:
                    os.mkdir(application_path + f'/result/{filename[1]}')
                except FileExistsError:
                    pass
                bg = Image.open(application_path + '/imgs/' + filename[0])
                for color in generate_colors(step):
                    color_set = color.append(bg)
                    colors_list.append(color_set)
    except FileNotFoundError:
        ok = input('There is no files in imgs folder geterate just colored labels? [Y/n] ') or 'Y'
        if ok == 'Y':
            bg = ''
            for color in generate_colors(step):
                color_set = color.append(bg)
                colors_list.append(color_set)
        else:
            raise Exception('Bye!')
    return colors_list


def get_rus_colors():
    colors_list = []
    try:
        listdir = os.listdir(application_path + '/imgs')
    except FileNotFoundError:
        ok = input('There is no files in imgs folder geterate just colored labels? [Y/n] ') or 'Y'
        if ok == 'Y':
            for color in COLORS:
                color_set = rgb(COLORS[color]) + [f'{color}', None]
                colors_list.append(color_set)
            return colors_list
        else:
            raise Exception('Bye!')
    for _filename in listdir:
        filename = img_re.match(_filename)
        if not _filename.startswith("."):
            try:
                os.mkdir(application_path + f'/result/{filename[1]}')
            except FileExistsError:
                pass
            bg = Image.open(application_path + '/imgs/' + filename[0])
            for color in COLORS:
                color_set = rgb(COLORS[color]) + [f'{filename[1]}/{color}', bg]
                colors_list.append(color_set)
    return colors_list


def make_img(color):
    bg = color.pop()
    name = color.pop()
    color = tuple(color)
    img = Image.new('RGBA', (mask.width, mask.height), color=color)
    gradient_color = ImageEnhance.Brightness(img).enhance(0.8)
    img = Image.composite(gradient_color, img, alpha_gradient)
    img = Image.composite(img, empty, mask)
    if bg:
        bg.convert('RGBA')
        offset = (
            ((bg.width - img.width + left_offset) if left_offset < 0 else left_offset),
            ((bg.height - img.height + top_offset) if top_offset < 0 else top_offset)
        )
        bg.paste(img, offset, img)
        bg.save(application_path + f'/result/{name}.png')
    else:
        img.save(application_path + f'/result/{name}.png')


def get_top_offset():
    _top_offset = input('Set top offset or skip (int): ')
    if not _top_offset:
        return get_bottom_offset()
    elif _top_offset.isdigit():
        __top_offset = int(_top_offset) if _top_offset else None
        return __top_offset
    else:
        print('Must be integer!')
        return get_top_offset()


def get_bottom_offset():
    bottom_offset = input('Set bottom offset (int) [5]: ')
    if not bottom_offset:
        print('Stayed default bottom offset - 5')
        return -5
    elif bottom_offset.isdigit():
        __bottom_offset = (0 - int(bottom_offset)) if bottom_offset else None
        return __bottom_offset
    else:
        print('Must be integer!')
        return get_bottom_offset()


def get_left_offset():
    _left_offset = input('Set left offset or skip (int): ')
    if not _left_offset:
        return get_right_offset()
    elif _left_offset.isdigit():
        __left_offset = int(_left_offset) if _left_offset else None
        return __left_offset
    else:
        print('Must be integer!')
        return get_left_offset()


def get_right_offset():
    right_offset = input('Set right offset (int) [5]: ')
    if not right_offset:
        print('Stayed default left offset - 5')
        return -5
    elif right_offset.isdigit():
        __right_offset = (0 - int(right_offset)) if right_offset else None
        return __right_offset
    else:
        print('Must be integer!')
        return get_right_offset()


def get_step():
    __step = input('Set color step (1-255) [5]: ')
    if __step.isdigit() and 1 <= int(__step) <= 255:
        return __step
    elif not __step:
        return 5
    else:
        print('Must be integer 1 - 255!')
        return get_step()


def what_colors():
    try:
        os.mkdir(application_path + '/result')
    except FileExistsError:
        pass
    ok = input('Get named (1) colors or RGB (2) [1/2]? ')
    if ok.isprintable() and str(ok) == '1':
        print('Making named!\n')
        __colors = get_rus_colors()
    elif not ok:
        print('Making named as default!\n')
        __colors = get_rus_colors()
    elif ok.isprintable() and str(ok) == '2':
        step = get_step()
        print(f'Making RGB with step = {step}!\n')
        __colors = get_colors(step)
    else:
        print('Must be integer 1 or 2!')
        return what_colors()
    return __colors


if __name__ == '__main__':
    set_executable(sys.executable)
    if not (mask.size == empty.size == alpha_gradient.size):
        raise Exception('mask.png, empty.png and alfa.png must be same size!')
    else:
        pass
    top_offset = get_top_offset()
    left_offset = get_left_offset()
    colors = what_colors()
    multiprocessing.freeze_support()
    with multiprocessing.Pool(processes=os.cpu_count() * 4) as pool:
        max_ = len(colors)
        tqdm.monitor_interval = 0
        with tqdm(total=max_) as progress_bar:
            for i, _ in tqdm(enumerate(pool.imap_unordered(make_img, colors))):
                progress_bar.update()

def colour_parser_eng():#Функция, превращающая файл с цветами на английском языке в множество 
    f = open('colours_wiki.txt', 'r')
    set_of_colours = set()
    for lines in f: 
        hash_s = lines.find('#') #разделитель в файле
        lines = lines[:hash_s - 1]
        curr_colour = lines.lower().split()
        for i in range(len(curr_colour)):
            curr_colour[i] = curr_colour[i].strip('(,\«»"\"'')')
            if curr_colour[i].isalpha():
                set_of_colours.add(curr_colour[i])
    return set_of_colours

def colour_parser_rus(): #Функция, превращающая файл с цветами на русском языке в множество 
    f = open('colours_rus.txt', 'r')
    set_of_colours = set()
    for lines in f: 
        hash_s = lines.find('#') #разделитель в файле
        lines = lines[:hash_s - 1]
        curr_colour = lines.lower().split()
        for i in range(len(curr_colour)):
            curr_colour[i] = curr_colour[i].strip('(,\«»"\"'')')
            if curr_colour[i].isalpha():
                set_of_colours.add(curr_colour[i])
    return set_of_colours

def bigrams(string_to_compare, model): #функция, берущая на вход 2 строки, состоящие из нескольких токенов, создающая в каждой строке список всевозможных сочетаний по 2
#и считающая количество совпавших пар - биграмм - между строками
    import nltk
    from nltk.util import ngrams
    string_to_compare = string_to_compare.lower().split()
    for i in range(len(string_to_compare)):
        string_to_compare[i] = string_to_compare[i].strip('(,\«»"\"'')')
    bigrams_s = list(ngrams(string_to_compare, 2))
    model = model.lower().split()
    probability = 0
    for i in range(len(model)):
        model[i] = model[i].strip('(,\«»"\"'')')
    bigrams_m = list(ngrams(model, 2))
    all_to_comp = len(bigrams_m)
    for i in range(all_to_comp):
        if bigrams_m[i] in bigrams_s:
            probability += 1
    return probability

def jaccard(string_to_compare, model): #функция, считающая меру Жаккара между строками - пересечение слов в 2х строках, деленное на их объединение
    string_to_compare = string_to_compare.lower().split()
    a = len(string_to_compare)
    for i in range(a):
        string_to_compare[i] = string_to_compare[i].strip('(,\«»"\"'')')
    model = model.lower().split()
    b = len(model)
    for i in range(b):
        model[i] = model[i].strip('(,\«»"\"'')')
    model = set(model)
    string_to_compare = set(string_to_compare)
    return len(model & string_to_compare) / len(string_to_compare | model)

def colour(string_to_compare, model): #функция, находящая в строках цвет и проверяющая, совпадает ли он
    set_of_colours_eng = colour_parser_eng() #множество всех цветов по-английски
    set_of_colours_rus = colour_parser_rus() #множество всех цветов по-русски
    dct_colours_rus = {'золотой': 'gold', 'черный': 'black', 'чёрный': 'black', 'белый': 'white', 'синий': 'blue', 'серебряный': 'silver', 'серебристый': 'silver', 'красный':'red', 'желтый':'yellow', 'жёлтый': 'yellow', 'космос': 'space', 'розовый':'pink', 'розовое':'rose', 'золото':'gold', 'зеленый':'green', 'светлый':'light', 'темный':'dark', 'жемчужный': 'pearl', 'рубиновый':'ruby', 'теплый':'warm', 'коричневый':'brown', 'топаз': 'topaz', 'космический':'cosmic', 'глубокий':'deep', 'металлик':'metallic', 'красное дерево':'mahogany', 'кремовый':'cream', 'лаймовый':'lime', 'сиреневый': 'lilac', 'стальной':'steel', 'бронзовый':'bronze', 'оникс':'onyx', 'циан':'cyan', 'пурпурный': 'magenta', 'коралловый':'coral', 'фуксия':'fuchsia','оранжевый':'orange', 'песочный':'sand', 'янтарный':'amber', 'винный':'wine', 'ультра':'ultra', 'фиолетовый':'purple', 'титан':'titanium', 'небесный':'sky','арктик':'arctic', 'индиан':'indian','шоколадный':'chocolate', 'мечта':'dream', 'яркий':'blaze', 'морской':'navy', 'неоновый':'neon', 'бриллиантовый':'diamond', 'мятный':'mint', 'медный':'copper', 'либерти':'liberty', 'фэйшн':'fashion', 'платиновый':'platinum', 'аква':'aqua', 'индиго':'indigo', 'сапфировый':'sapphire', 'ледяной':'ice', 'орхидея':'orchid', 'пастельный':'pastel', 'ваниль':'vanilla', 'нефрит':'jade', 'каштан':'chestnut', 'опал':'opal'}
    dct_colours_eng = {'white':'белый', 'blue': 'синий', 'red':'красный', 'space': 'космос', 'pink':'розовый', 'rose':'розовое', 'cosmic':'космический', 'topaz':'топаз', 'brown':'коричневый', 'ruby':'рубиновый', 'pearl':'жемчужный', 'deep':'глубокий', 'warm':'теплый', 'apple':'яблочный', 'dark':'темный', 'green':'зеленый', 'light':'светлый', 'wave':'морской', 'metallic':'металлик', 'charcoal':'древесный уголь', 'mahogany':'красное дерево', 'cream':'кремовый', 'lime':'лаймовый', 'blackberry':'ежевичный', 'lilac':'сиреневый', 'steel':'стальной', 'midnight':'полночь', 'misty':'туманный', 'bronze': 'бронзовый', 'onyx':'оникс', 'cyan':'циан', 'magenta':'пурпурный', 'coral':'коралловый', 'cool':'свежий', 'fuchsia':'фуксия', 'orange':'оранжевый', 'sand':'песочный', 'golden':'золотой', 'amber':'янтарный', 'wine':'винный', 'star':'звездный', 'ultra':'ультра', 'purple':'фиолетовый', 'titanium':'титан', 'magic':'магический', 'vista':'виста', 'sky':'небесный', 'surf':'сёрф', 'slate':'грифельный', 'arctic':'арктик', 'indian':'индиан', 'chocolate':'шоколадный', 'dream':'мечта', 'navy':'морской', 'neon':'неоновый', 'diamond':'бриллиантовый', 'mint':'мятный', 'copper':'медный', 'liberty':'либерти', 'platinum':'платиновый', 'aqua':'аква', 'indigo':'индиго', 'sapphire':'сапфировый', 'ice':'ледяной', 'orchid':'орхидея', 'pastel':'пастельный', 'vanilla':'ваниль', 'jade':'нефрит', 'chestnut':'каштан', 'opal':'опал'}
    #два словаря, использующиеся, если в одной строке название цвета по-русски, в другой - по-английски
    string_to_compare = string_to_compare.lower().split()
    for i in range(len(string_to_compare)):
        string_to_compare[i] = string_to_compare[i].strip('(,""«»'')')
    model = model.lower().split()
    probability = 0
    for i in range(len(model)):
        model[i] = model[i].strip('(,""«»'')')
        if model[i].isalpha(): #цвета не содержат цифр
            if model[i] in set_of_colours_eng and model[i] != "apple" and model[i] != "blackberry": #если токен - цвет по-английски, но не является моделью телефона, то
                if model[i] == 'gray' or model[i] == 'grey':  #обрабатываем серый цвет, а также далее другие 4 цвета - исключения из-за разности написания
                    if 'gray' in string_to_compare or 'grey' in string_to_compare or 'серый' in string_to_compare:
                        probability += 1
                elif model[i] == 'black':
                    if 'черный' in string_to_compare or 'чёрный' in string_to_compare or 'black' in string_to_compare:
                        probability += 1
                elif model[i] == 'yellow':
                    if 'желтый' in string_to_compare or 'жёлтый' in string_to_compare or 'yellow' in string_to_compare:
                        probability += 1  
                elif model[i] == 'gold':
                    if 'золото' in string_to_compare or 'золотой' in string_to_compare or 'gold' in string_to_compare:
                        probability += 1
                elif model[i] == 'silver':
                    if 'серебряный' in string_to_compare or 'серебристый' in string_to_compare or 'silver' in string_to_compare:
                        probability += 1 
                elif model[i] in string_to_compare: #если в другой строке есть совпадающий токен-цвет
                    probability += 1
                elif model[i] in dct_colours_eng: #если мы знаем перевод этого слова на русский
                    if dct_colours_eng[model[i]] in string_to_compare: #и перевод этого слова присутствует в другой строке
                        probability += 1
            elif model[i] in dct_colours_eng: #если в английском файле не оказалось данного цвета, но мы ранее видели, что данный цвет используется в описании телефонов и мы записали его перевод,
                if dct_colours_eng[model[i]] in string_to_compare: #и его перевод оказался во второй строке
                    probability += 1            
            elif model[i] in set_of_colours_rus: #если токен - цвет по-русски
                if model[i] in dct_colours_rus: #если мы знаем перевод этого слова на английский
                    if dct_colours_rus[model[i]] in string_to_compare: #и перевод этого слова присутствует в другой строке
                        probability += 1
                elif model[i] in string_to_compare: #если в другой строке есть совпадающий токен-цвет
                    probability += 1  
                elif model[i] == 'серый': #проверяем цвет-исключение
                    if 'gray' in string_to_compare or 'grey' in string_to_compare or 'серый' in string_to_compare:
                        probability += 1
            elif model[i] in dct_colours_rus: #если в русском файле не оказалось данного цвета, но мы ранее видели, что данный цвет используется в описании телефонов и мы записали его перевод,
                if dct_colours_rus[model[i]] in string_to_compare: #и его перевод оказался во второй строке
                    probability += 1            
    return probability

def levenstain(string_to_compare, model): #функция, считающая расстояние Левенштейна между сплошными строками без пробелов
    from nltk.metrics import edit_distance
    string_to_compare = string_to_compare.lower().split()
    for i in range(len(string_to_compare)):
        string_to_compare[i] = string_to_compare[i].strip('(,\«»"\"'')')
    string_to_compare = ''.join(string_to_compare)
    model = model.lower().split()
    for i in range(len(model)):
        model[i] = model[i].strip('(,\«»"\"'')')
    model = ''.join(model)
    try:
        dist = edit_distance(model, string_to_compare) / len(model)
    except:
        dist = -1
    return dist

#четыре правила ниже отвечают за проверку совпадения памяти устройствв паре
def mem_normalize(mem): #функция, которая переводит часть, отвечающую за единицу объема памяти, в 2 английские буквы
    fir = mem.find('gb')
    if fir > 0:
        mem = mem[:fir] + 'gb'
    sec = mem.find('гб')
    if sec > 0:
        mem = mem[:sec] + 'gb'
    thir = mem.find('mb') 
    if thir > 0:
        mem = mem[:thir] + 'mb'
    four = mem.find('мб')
    if four > 0:
        mem = mem[:four] + 'mb'
    return mem
        
def changing(memory): #превращает в шаблон представление памяти устройства (считаем, что число в строке всегда идет перед размером памяти)
    #память записывается в формате число слитно с 2мя английскими буквами, означающими объем памяти
    result = []
    for i in range(len(memory)):
        memory[i] = memory[i].strip('(,\«»"\"'')')
        if memory[i].find('gb') == 0 or memory[i].find('гб') == 0 or memory[i].find('мб') == 0 or memory[i].find('mb') == 0:
            if i != 0 and memory[i-1].isdigit():
                curr = memory[i - 1] + memory[i]
                curr = mem_normalize(curr)
                result.append(curr)
        elif memory[i].find('gb') > 0 or memory[i].find('гб') > 0 or memory[i].find('мб') > 0 or memory[i].find('mb') > 0:
            result.append(mem_normalize(memory[i]))
    return result
    
def mem_storage(string_to_compare, model): #сравнивает шаблонизированную память в 2х строках
    string_to_compare = string_to_compare.lower().split()
    model = model.lower().split()    
    mem_str = changing(string_to_compare)
    mem_mod = changing(model)
    prob = 0
    for i in range(len(mem_mod)):
        if mem_mod[i] in mem_str:
            prob += 1
    return prob      

def is_it_mem_st(mem_str): #проверяет, имеет ли токен отношение к памяти устройства
    if mem_str.find('gb') >= 0 or mem_str.find('гб') >= 0 or mem_str.find('мб') >= 0 or mem_str.find('mb') >= 0:
        return True
    else:
        return False

def name_model(string_to_compare, model): #функция, сравнивающая токены, которые являются названиями модели
    set_of_colours_eng = colour_parser_eng() #множество всех цветов по-английски
    set_of_colours_rus = colour_parser_rus() #множество всех цветов по-русски
    string_to_compare = string_to_compare.lower().split()
    for i in range(len(string_to_compare)):
        string_to_compare[i] = string_to_compare[i].strip('(,""'')')
    model = model.lower().split()
    probability = 0
    for i in range(len(model)):
        model[i] = model[i].strip('(,\«»"\"'')')
        if model[i] == 'apple' or model[i] == 'blackberry': #модели-исключения, так как одновременно являются и цветами
            if model[i] in string_to_compare:
                probability += 1
        if model[i].isalpha() and not is_it_mem_st(model[i]) and model[i] not in set_of_colours_eng and model[i] not in set_of_colours_rus: #проверяем, не является ли буквенный токен цветом или памятью устройства
            if model[i] in string_to_compare: #если нет, то это скорее всего название модели, поэтому мы ищем такое же во 2й строке
                probability += 1  
    if probability == 0: #усиливаем важность правила
        probability = -1
    return probability

def num_model(string_to_compare, model): #также в этом правиле может выполняться сравнение года выпуска модели,
    #функция, сравнивающая токены, состоящие из цифр (не являющиеся объемом памяти модели), то есть номера модели
    string_to_compare = string_to_compare.lower().split()
    for i in range(len(string_to_compare)):
        string_to_compare[i] = string_to_compare[i].strip('(,\«»"\"'')')
    model = model.lower().split()
    param_kol = len(model)
    probability = 0
    for i in range(len(model)):
        model[i] = model[i].strip('(,\«»"\"'')')
        if model[i].isdigit():
            if i < len(model) - 1: #здесь мы проверяем,что число не является размером памяти устройства (с учетом стандартного построения словосочетания - объем, единица объема)
                if model[i + 1] != 'mb' and model[i + 1] != 'gb' and model[i + 1] != 'мб' and model[i + 1] != 'гб':
                    if model[i] in string_to_compare:
                        probability += 1
            else:
                if model[i] in string_to_compare:
                    probability += 1  
    if probability == 0: #усиливаем важность правила
        probability = -1
    return probability

def check_series(str_ch): #правило, проверяющее, что токен является серией, то есть состоит не только из букв/цифр, не является нормализованной строкой объема памяти устройства
    if not str_ch.isalpha() and not str_ch.isdigit() and str_ch.find('gb') < 0 and str_ch.find('mb') < 0 and str_ch.find('гб') < 0 and str_ch.find('мб') < 0:
        return True    
    else:
        return False
    
def series(string_to_compare, model): #правило, сравнивающее токены-серии телефонов
    string_to_compare = string_to_compare.lower().split()
    for i in range(len(string_to_compare)):
        string_to_compare[i] = string_to_compare[i].strip('(,""'')')
    model = model.lower().split()
    for i in range(len(model)):
        model[i] = model[i].strip('(,\«»"\"'')')
    sum_prob = 0
    size = len(model)
    length = len(string_to_compare)
    for i in range(size):
        if check_series(model[i]): #если очередной токен - серия
            for j in range(length): #рассматриваем все токены второй строки
                if check_series(string_to_compare[j]): #если токен во 2 строке тоже серия
                    flag = 0
                    if model[i].find(string_to_compare[j]) >= 0: #проверяем, не является токен 1й строки, который мы рассматриваем, подсловом токена 2й строки, и наоборот
                        flag = 1
                    elif string_to_compare[j].find(model[i]) >= 0:
                        flag = 1
                    sum_prob += flag  #если является, учитываем это
    if sum_prob == 0: #необходимо проверить, нет ли во 2й строке серии, расклеенной по 2м или 3м токенам (больше обычно не бывает), разделенной на буквы и цыфрв (PRO6 -> pro 6)
    #тогда найденная такая же серия в первой строке, но в привычнолм виде, не смэтчится с расклеенной (если расклейка произошла в 1й строке, то токены просто не воспримутся, как серия)
        adglutinate = [] 
        for i in range(length - 1): #склеиваем 2ую строку по 2 токена в прямом порядке
            adglutinate.append(string_to_compare[i] + string_to_compare[i + 1])
        for i in range(length - 2): #по 3 токена в прямом
            adglutinate.append(string_to_compare[i] + string_to_compare[i + 1] + string_to_compare[i + 2])
        for i in range(1, length): #по 2 обратном порядке
            adglutinate.append(string_to_compare[i] + string_to_compare[i - 1])
        for i in range(2, length): #по 3 в обратном (с конца в начало)
            adglutinate.append(string_to_compare[i] + string_to_compare[i - 1] + string_to_compare[i - 2])    
        for i in range(size): 
            if check_series(model[i]): #если очередной токен - серия
            for j in range(len(adglutinate)): #рассматриваем все токены из списка склеек из 2й строки
                if check_series(adglutinate[j]): #если токен в списке склеек из 2й строки тоже серия
                    flag = 0
                    if model[i].find(adglutinate[j]) >= 0: #проверяем, не является токен 1й строки, который мы рассматриваем, подсловом токена склеек из 2й строки, и наоборот
                        flag = 1
                    elif adglutinate[j].find(model[i]) >= 0:
                        flag = 1
                    sum_prob += flag  #если является, учитываем это        
    if sum_prob == 0: #стараемся сделать правило с серией самым главным
        sum_prob = -1.5
    return sum_prob

def price_abs(price_to_compare, price): #правило, возвращающее модуль разницы цены телефонов из пары
    if price_to_compare == "NaN" or price_to_compare == "NaN":
        return -999
    return abs(price_to_compare - price)

def price_comp(price_to_compare, price): #правило, возвращающее процент модуля разницы цены телефонов от цены телефона из стороннего интернет-магазина
    if price_to_compare == "NaN" or price_to_compare == "NaN":
        return -999
    return abs(price_to_compare - price) / price
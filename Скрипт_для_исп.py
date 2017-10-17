import pandas as pd
#Здесь пока идет кусок с объяснением, как пользоваться результатом прошлой работы алгоритма, если изменение в числе телефонов происходит в сторонних интернет-магазинах;
#так как требуется выполнение противоположной задачи, а именно, учитывать изменения в нашем - мтс - интернет-магазине, код будет изменен.
info_checked = pd.read_excel("Top_match.xlsx") #записываем в df результаты (найденные пары) работы прошлого запуска алгоритма (необходимо для упрощения поиска новых пар, так как
#новые телефоны добавляются в небольшом количестве, а старые пары, найденные правильно, остаются актуальными)
info_other_shops = pd.read_excel("pattern_file.xlsx") #записываем в df информацию о телефонах из интернет-магазинов (не мтс, сторонних)
info_other_shops = info_other_shops.rename(columns={"price": "Price", "title":"Real"}) #переименовываем колонки с ценой телефонов из других интернет-магазинов и их кратким описанием
#(серия, номер, модель, цвет, память устройства) для того, чтобы можно было соединить информацию из 2х таблиц
top_pair_known = info_checked.merge(info_other_shops, on="Real").dropna().drop_duplicates(subset="Real") #соединяем информацию из 2х таблиц с помощью колонки, содержащей краткую информацию о телефонах,
#чтобы получить df, содержащий пары телефонов, которые не придется уже мэтчить с помощью алгоритма (отличается от таблицы info_checked тем, что там встречаются телефоныв, проверенные алгоритмом, на которым
#не удалось найти пару)
top_pair_known = top_pair_known[["Real","Top_match"]].reset_index() #оставляем в таблице 2 колонки - найденную пару, индексируем с 0
del top_pair_known["index"]#удаляем ненужную колонку со старыми индексами
info_other_shops['Model_exists'] = ~info_other_shops["Real"].isin(top_pair_known["Real"]) #создаем в df сторонних телефонов колонку, показывающую, была ли найдена ранее пара телефону
#из другого интернет-магазина в базе телефонов мтс. Была - false, не была - true
info_other_shops = info_other_shops.loc[info_other_shops['Model_exists']] #оставляем только те телефоны, которым пары в базе телефонов мтс найдены не были
info_other_shops = info_other_shops.rename(columns={"Real":"title"}) #переименовываем обратно колонку с краткой информаицей о телефонах для алгоритма
info_mts = pd.read_excel("shop_mts_with_prices.xlsx") #записываем в df информацию о телефонах из интрнет-магазина мтс
info_other_shops['ones'] = 1
info_mts['ones'] = 1 #для того, чтобы сделать декартово произведение 2х таблиц - телефонов из других интрнет-магазинов и магазина мтс, то есть рассмотреть всевозможные пары телефоны,
#которые получаются при соединении каждого телефона из 1ой таблицы со всеми телефонами другой, создаем 2 одинаковые колонки в обеих таблицах
all_pairs = info_other_shops.merge(info_mts, how='outer', on='ones').fillna(-999) #создаем таблицу декартовых произведений. Так как не у всех телефонов записаны цены, то
#недостающие цены заполняем -999, что не меняет выбор random forest, но упрощает его использование

del all_pairs["store"]
del all_pairs["datetime"]
del all_pairs["region"]
del all_pairs["Model_exists"] #удаляем лишние колонки
from all_rules import jaccard as rule_jaccard, bigrams as rule_bigrams, name_model as rule_model, series as rule_series, num_model as rule_num_model, mem_storage as rule_mem_storage, colour as rule_colour, levenstain as rule_levenstain
from all_rules import price_comp as rule_price_comp, price_abs as rule_price_abs #импортируем 8 правил на краткую информаицю о телефоне (правило на совпадение серии, номера,
#названия модели, совпадения цвета и памяти устройства, а также 3 правила на проверку сходства 2х предложений: расстояние Левенштейна, мера Жаккара и количество совпавших биграмм)
#импортируем 2 правила, возвращающих абсолютную и относительную разницу между ценами телефонов. Импортируем из файла all_rules.py с написанными мной правилами.
price_rules = [('Prob_abs_price', rule_price_abs), ('Prob_comp_price', rule_price_comp)]
rules = [('Prob_jaccard', rule_jaccard), ('Prob_bigrams', rule_bigrams), ('Prob_model', rule_model), ('Prob_series', rule_series),
('Prob_num_model', rule_num_model), ('Prob_mem_storage', rule_mem_storage), ('Prob_colour', rule_colour), ('Prob_levenstain', rule_levenstain)]
# создаем списки кортежей ("название колонки, в которой будет содержаться вероятность сходства пар, возвращенная конкретным правилом", названием, под которым импортировано правило),
# отдельно для правил с ценами, отдельно для правил с информацией о телефонах (нужно для того, чтобы применение правил можно было описать в простом цикле)

def model_match(string_to_compare, model):
    token1 = string_to_compare.split()[0].lower().strip('(,\"\"'')')
    token2 = model.split()[0].lower().strip('(,\"\"'')')
    return token1 == token2 #правило, отмечающее пары, которые почти точно не являются описанием одного и того же телефона. Оно основано на том, что
    #несовпадение первого токена почти точно, по тому, как представлена информация о телефонах, означает, что телефоны разных моделей, то есть нужная пара не была найдена, потому
    #что в базе мтс такой модели нет

def calc_rules(info_top, col1, col2):
    for i in range(len(rules)):
        colname, foo = rules[i]
        info_top[colname] = info_top.apply(lambda row: foo(row[col1], row[col2]), axis=1)
    return info_top #функция, которая применяет к паре телефонов 8 правил, проверяющих совпадение информации о телефонах, и записывает результат в колонку правила в df

def calc_price(info_top, col1, col2):
    for i in range(len(price_rules)):
        colname, foo = price_rules[i]
        info_top[colname] = info_top.apply(lambda row: foo(row[col1], row[col2]), axis=1)
    return info_top #функция, которая применяет к ценами пары телефонов правила, связанные со стоимостью моделей, и записывает результат в колонку правила в df

import seaborn as sns
import numpy as np
from multiprocessing import Pool

num_partitions = 50 #number of partitions to split dataframe
num_cores = 50 


def parallelize_dataframe(df, func):
    df_split = np.array_split(df, num_partitions)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df #разделение df на num_of_partitions, чтобы распараллелить и увеличить скорость выполнения алгоритма, и применение алгоритма ко всем парам all_pairs (func - параметр parallelize_dataframe)

def probability(prob, name):
    if prob >= 0.7: #порог отсечения (примерно такой найден был после построения pr-curve по полученным результатам)
        return name #фунция, отсекающая по порогу вероятности пары, которые можно считать верными и те, оторые алгоритм нашел неправильно, например, потому, что такого телефона в базе мтс нет

def in_base(matched, name):
    if matched == True:
        return name #функция, проверяющая, был ли найден в базе мтс такой телефон (основывается на результатах правила model_match)

def multiply_all_pairs(all_pairs):
    all_pairs['Model_match'] = all_pairs.apply(lambda row: model_match(row['title'], row['Name']), axis=1) #создание колонки, где каждой паре соответствует true, если первые токены совпадают,
    #false - иначе
    all_pairs = calc_rules(all_pairs, col2='Name', col1='title') #Name - колонка телефонов из базы мтс, title - из сторонних интернет-магазинов
    all_pairs = calc_price(all_pairs, col1='Price_mts', col2='Price')
    return all_pairs #основная функция, отвечающая за рассчет всех правил совпадения/не совпадения моделей в паре, записывающая в df по колонкам полученныке вероятности

all_pairs = parallelize_dataframe(all_pairs, multiply_all_pairs) #применяем алгорим ко всем получившимся парам, чтобы узнать вероятность того, что они описывают один и тот же телефон.
#Распараллеливаем работу алгоритма.

from sklearn.externals import joblib
rf = joblib.load('random_forest.pkl') #загружаем обученный ранее на имеющихся правилах random forest
feature_names = [x[0] for x in rules] + [x[0] for x in price_rules] #список строковых названий фич (правил), использующихся для отбора пар
X = all_pairs[feature_names] #X - df, состоящая из вероятностей совпадения каждой из проверяемых пар по числу правил, найденных алгоритмом, т.е. на пару телефон - телефон
#возвращается строка из 8 вероятностей совпадения телефонов, возвращенных правилами. Эти вероятности мы отбираем в Х.
all_pairs['Probability'] = rf.predict_proba(X)[:,1] #В общем dataframe, содержащем пары и информацию о их совпадении, создается столбец итоговых вероятностей совпадения телефонов внутри пар,
#предсказанных на основе вероятностей, посчитанных каждым правилом. Итоговые вероятности определяет random forest.
all_pairs = all_pairs.sort_values('Probability', ascending=False) #сортируем пары по убыванию вероятности их совпадения
top_pair = all_pairs.groupby('title', as_index=False).first() #first - выбор лучшей пары (с самой большой вероятностью совпадения), top_pair - табличка с лучшими совпадениями
top_pair["Name"] = top_pair.apply(lambda row: in_base(row['Model_match'], row['Name']), axis=1) #убираем пару, найденную телефону в базе мтс, так как пара почти точно неправильная, 
#в силу отсутствия телефона данной модели в базе мтс
top_pair["Name"] = top_pair.apply(lambda row: probability(row['Probability'], row['Name']), axis=1)  #убираем пару, найденную телефону в базе мтс, так как вероятность
#совпадения телефонов оказалась ниже порога, который показывает точность результата работы алгоритма
top_pair = top_pair.rename(columns={"title": "Real", "Name": "Top_match"}) #переименовываем колонки таким образом, чтобы "real" отвечала за телефоны из других магазинов,
#top_match за пары, найденные этим телефонам в базе мтс
cols = top_pair.columns.tolist()
cols = cols[0:1] + cols[3:4] 
top_pair = top_pair[cols] #оставляем только 2 колонки - пары телефонов, найденные алгоритмом

top_pair = pd.concat([top_pair, top_pair_known]) #присоединям к результату старые пары, найденные алгоритмом еще при ранних запусках

top_pair.to_excel("Top_match.xlsx") #Это итоговая табличка, в которой записаны результаты
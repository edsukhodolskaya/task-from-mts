import pandas as pd
info_true_arts_1c = pd.read_excel("shop_mts_with_prices.xlsx") #записываем в df информацию о телефонах интернет-магазина мтс с ценами 
external_phones = pd.read_excel("pattern_file.xlsx") #записываем в df информаицю о телефонах из других интернет-магазинов с ценами
external_phones = external_phones[['title', 'price']].drop_duplicates() #оставляем только нужные нам колонки с краткой информацией о телефоне и его цене без дубликатов
known_pairs = pd.read_csv('Пары_найденные_в_базе.txt', '>', header=None, names=['phone{}'.format(i) for i in range(1,3)]) #записываем в df пары, вручную размеченные и найденные ранее в базе(аболютно точно правильные),
#и собранные в определенном формате в файл. 
known_pairs = pd.concat([known_pairs, known_pairs.rename(columns={'phone1':'phone2', 'phone2':'phone1'})]).drop_duplicates() #записываем в эту же df пары, написанные в обратном порядке,
#чтобы не пропустить уже найденные пары
external_phones['ones'] = 1
info_true_arts_1c['ones'] = 1 # как и в основном скрипте для запуска, создаем две одинаковые колонки для того, чтобы сделать декартово произведение телефонов в 2х таблицах
info_true_labeled = external_phones.loc[external_phones['title'].isin(known_pairs.phone2)] #записываем в df только те строки из таблицы сторонних телефонов, в которых присутствуют телефоны,
#у которых найдены и записаны в файле, отмеченном выше, пары в базе мтс, чтобы в декартовом произведении присутствовали лишь те телефоны из сторонних магазинов, у которых мы знаем
#верную пару из базы мтс 
all_pairs = pd.merge(info_true_labeled.reset_index(), info_true_arts_1c, on='ones').drop('ones', axis=1) #декартово произведение пар, удалена лишняя колонка 1
all_pairs = all_pairs.set_index(['Name', 'title']) #делаем индексом df пару телефонов для удобства подготовки данных для обучения
known_pairs['ones'] = 1
all_pairs['Match'] = known_pairs.set_index(['phone1','phone2'])['ones'] #сделав так же индексом пару телефонов в таблице верных пар, проставляем в общей таблице пар единицы напротив пар,
#которые являются верными
all_pairs['Match'] = all_pairs['Match'].fillna(0) #все остальные пары являются по построению неправильными, поэтому их размечаем 0
all_pairs = all_pairs.reset_index() #сбрасываем индекс и индексируем с 0
all_pairs = pd.concat([all_pairs[all_pairs['Match']==1],
                       all_pairs[all_pairs['Match']==0]\
                           .sample(int(all_pairs['Match'].sum()*10), random_state=0) # disbalance remains
                      ]).sample(frac=1, random_state=0) # shuffle #для того, чтобы данные не вызвали неправильного обучения, перемешиваем 
                      #пары, размеченные 0 и 1, и пар с 0 (которых, очевидно, во много раз больше, чем правильных) берем в 10 раз больше, чем пар с 1, балансируя выборку 
all_pairs = all_pairs.rename(columns={"price": "Price", "title": "Real", "Name": "Top_guess"}).drop('index', axis=1).reset_index().fillna(-999)
#приводим таблицу в удобный для обучения вид - переименовываем и удаляем лишние колонки, заполняем пропущенные цены -999, переиндексируем

from all_rules import jaccard as rule_jaccard, bigrams as rule_bigrams, name_model as rule_model, series as rule_series, num_model as rule_num_model, mem_storage as rule_mem_storage, colour as rule_colour, levenstain as rule_levenstain
from all_rules import price_comp as rule_price_comp, price_abs as rule_price_abs

price_rules = [('Prob_abs_price', rule_price_abs), ('Prob_comp_price', rule_price_comp)]
rules = [('Prob_jaccard', rule_jaccard), ('Prob_bigrams', rule_bigrams), ('Prob_model', rule_model), ('Prob_series', rule_series),
('Prob_num_model', rule_num_model), ('Prob_mem_storage', rule_mem_storage), ('Prob_colour', rule_colour), ('Prob_levenstain', rule_levenstain)]

def calc_rules(info_top, col1, col2):
    for i in range(len(rules)):
        colname, foo = rules[i]
        info_top[colname] = info_top.apply(lambda row: foo(row[col1], row[col2]), axis=1)
    return info_top

def calc_price(info_top, col1, col2):
    for i in range(len(price_rules)):
        colname, foo = price_rules[i]
        info_top[colname] = info_top.apply(lambda row: foo(row[col1], row[col2]), axis=1)
    return info_top  
#часть с 29 по 46 строку такая же в файле основного скрипта, где приведены комментарии    

all_pairs = calc_rules(all_pairs, col1='Real', col2='Top_guess') #рассчитываем для подготовленных данных вероятность совпадения пар по 8 правилам на информацию о телефонах
all_pairs = calc_price(all_pairs, col1='Price', col2="Price_mts") #-||- по правилам на цены
all_pairs = all_pairs.drop_duplicates(subset=["Real", "Top_guess", "Price"]) #убираем дубликаты 

feature_names = [x[0] for x in rules] + [x[0] for x in price_rules] #список строковых названий фич (правил), использующихся для отбора пар
X = all_pairs[feature_names]
#X - df, состоящая из вероятностей совпадения каждой из проверяемых пар по числу правил, найденных алгоритмом, т.е. на пару телефон - телефон
#возвращается строка из 8 вероятностей совпадения телефонов, возвращенных правилами. Эти вероятности мы отбираем в Х.
y = all_pairs[:]['Match'] #y - разметка пар 0 и 1 в зависимости от их совпадения
from sklearn import ensemble
rf = ensemble.RandomForestClassifier(n_estimators=15, max_depth=7)
rf = rf.fit(X, y) #обучаем модель на выборке
from sklearn.externals import joblib
joblib.dump(rf, 'random_forest.pkl') #сохраняем обученную модель

from sklearn.model_selection import cross_val_predict
from sklearn.metrics import f1_score
y_pred = cross_val_predict(rf, X, y, cv=10) #оцениваем работу модели
print("f1_score:",  f1_score(y, y_pred, average='binary'), "\n")


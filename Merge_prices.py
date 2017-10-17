import pandas as pd
info_true_arts_1c = pd.read_excel("shop_mts_startphones_table.xlsx", sheetname='data') #здесь должен быть файл (самый актуальный,т его название), из которого в df записывается информация о телефонах мтс с их артикулами
info_true_arts_1c = info_true_arts_1c[['artikul','name']].dropna().set_index('artikul')
info_prices = pd.read_csv('iv_recdev_art_tac_price.tsv', '\t', encoding='ISO-8859-1', low_memory=False) #в df записывается файл с артикулами, таками и ценами телефонов из базы мтс
info_prices = info_prices.rename(columns={"iv_recdev_art_tac_price.art_1c": "Art_1c", #мнеяются названия колонок
                                          "iv_recdev_art_tac_price.tac": "Tac", 
                                          "iv_recdev_art_tac_price.price_med":"Price_mts"})
info_prices = info_prices.groupby('Art_1c').Price_mts.median() #в df записывается медианная цена телефонов с одним артикулом
info_true_arts_1c['Price_MTS'] = info_prices #по артикулам мы собираем воедину информацию (краткую) о телефонах и их среднюю цену
info_true_arts_1c.to_excel("shop_mts_with_prices.xlsx") #сохраняем в файл с удобным нам названием


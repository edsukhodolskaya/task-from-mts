**Внутри каждого скрипта подробные комментарии, объясняющие его работу** 

В файле "Отчет" - отчет по пройденной практике, содержащий полное объяснение и раскрытие поставленной задачи
Некоторые файлы, необходимые для работы алгоритма, содержат информацию, которую запрещено выкладывать в публичный доступ, поэтому тут присутствует их описание, но их самих нет.

**файлы, нужные для работы алгоритма**:
* Merge\_prices - собирает из базы телефонов мтс с артикулами и кратким описанием телефонов - на данный момент shop\_mts\_startphones\_table.xlsx - и файла с ценами телефонов мтс
  и их артикулами - iv\_recdev\_art\_tac\_price.tsv - один целый файл: краткая информаиця о телефоне, необходимая алгоритма, и его цена
* PR\_curve - строит pr_curve на размеченных (1 - пара совпала, 0 - пара найдена неправильно) вручную парах, выданных алгоритмом и вероятностях их совпадения, выданных random forest
* random\_forest - обученная скриптом обучение\_и\_оценка модель, готовая к использованию
* Обучение\_и\_оценка - файл, учащий random\_forest на основе файлa Пары\_найденные\_в\_базе.txt пар, найденных в базе и вручную размеченных + f1_score.
* Скрипт\_для\_исп - непосредственно скрипт, применяющий алгоритм к данным
* Все правила в одном файле all\_rules, который используется файлом скрипт\_для\_исп
* Два файла с списком цветов на русском - colours\_rus.txt и на английском - colours\_wiki.txt 
* Пары\_найденные\_в\_базе - файл с списком пар, размеченных и найденных вручную - пары вида "телефон из стороннего интернет-магазина - телефон из базы мтс"
* Нет\_в\_базе\_МТС.txt - файл с списком телефонов из сторонних интернет-магазинов, которых точно нет  базе МТС, может использоваться для разметки
* shop\_mts\_with\_prices.xlsx - файл, в котором собраны воедино скриптом Merge\_prices цены и краткие описния телефонов из интернет-магазина мтс
* iv\_recdev\_art\_tac\_price.tsv - файл, в котором собраны артикулы и цены телефонов из базы мтс
* Top_match.xlsx - файл, хранящий в себе результаты последнего запсука алгоритма, использующийся в том числе в новых запусках для уменьшения времени работы 

**Для запуска алгоритма необходимо пользоваться скрипт\_для\_исп, подставляя, при необходимости, нужные файлы в скрипт для обработки,**
**для переобучения модели скриптом обучение\_и\_оценка, для правки правил - all\_rules**  


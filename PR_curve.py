import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
prob_in_shops = pd.read_excel('file.xlsx') #здесь должен быть файл, в котором стоит отдельной колонкой разметка 0 и 1 пар, абсолютно верная, пары и вероятности, возвращенные random forest
prob_in_shops = prob_in_shops.dropna() #не должно быть пустых ячеек, иначе график не построится
reals_list = prob_in_shops["Match"].tolist() #match пока проставляется руками
match_prob_list = prob_in_shops["Probability"].tolist()
y_true = np.array(reals_list)
y_scores = np.array(match_prob_list)
precision, recall, threshold = precision_recall_curve(y_true, y_scores) #рассчитываем на основе данных
plt.clf()
plt.plot(recall, precision, lw=2, color='navy',
         label='Precision-Recall curve for matches')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.legend(loc="lower left")
plt.show()
plt.savefig('Precision-Recall curve for matches.pdf') #строим pr-curve


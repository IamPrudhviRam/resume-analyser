from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
import numpy as np
import matplotlib.pyplot as plt

def plot_confusion_matrix(df_confusion, title='Confusion matrix', cmap=plt.cm.gray_r):
    plt.matshow(df_confusion, cmap=cmap) # imshow
    #plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(df_confusion.columns))
    plt.xticks(tick_marks, df_confusion.columns, rotation=45)
    plt.yticks(tick_marks, df_confusion.index)
    #plt.tight_layout()
    plt.ylabel(df_confusion.index.name)
    plt.xlabel(df_confusion.columns.name)

y_true = [5, 5, 5, 6, 11, 8 ,13,13,13,6,11,6,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,7,7,12,10,15,15,15,10,15,15,15,
          10,5,5,5,5,5,5,5,5,10,15,5,5,5]
print("lenth of ytrue",len(y_true))
y_pred = [16,5, 5, 16, 16, 8,13,13,13,6,11,6,12,12,11,11,11,11,11,11,12,11,11,11,12,11,14,11,11,11,7,12,12,12,16,5,16,16,5,16,12,
          16,5,5,5,5,5,5,5,5,16,5,16,16,16]
print("lenth of ypred",len(y_pred))
confusion_matrix(y_true, y_pred)



print("confusion matrix value : \n ",confusion_matrix(y_true, y_pred))

#plot_confusion_matrix(confusion_matrix(y_true, y_pred))

print("accuracy score value : \n ",accuracy_score(y_true, y_pred))
print("recall score value : \n ",recall_score(y_true, y_pred, average=None, labels=np.unique(y_pred)))
print("precision score value : \n ",precision_score(y_true, y_pred, average=None,labels=np.unique(y_pred)))


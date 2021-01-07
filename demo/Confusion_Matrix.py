import sys
import os
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score


def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    compare_resume()

def compare_resume():
    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    labelled_data_dir_path = current_dir + '/data/Confusion_Matrix_Text_Data/labelled'
    predicted_data_dir_path = current_dir + '/data/Confusion_Matrix_Text_Data/predicted'
    labelled_file_Names = os.listdir(labelled_data_dir_path)
    predicted_file_Names = os.listdir(predicted_data_dir_path)
    print("labelled file names", labelled_file_Names)
    labels=[
        'meta\tknowledge', 'meta\tproject', 'meta\teducation', 'meta\texperience', 'meta\tothers',
        'header\tknowledge','header\tproject','header\teducation','header\texperience','header\tothers',
        'content\tknowledge', 'content\tproject', 'content\teducation', 'content\texperience', 'content\tothers'
    ]
    labelled_dict = {}
    predicted_dict = {}
    for file in labelled_file_Names:
        with open(labelled_data_dir_path +"/"+file,encoding='utf-8') as f:
            lines = f.read().split('\n')
            for line in lines:
                word=line.rsplit('\t',1)
                if(word[0] != ''):
                    word[0] = word[0].replace(word[0], str(labels.index(word[0])))
                    labelled_dict[word[1]] = word[0]
    print("labelled Dict is: ", labelled_dict)
    for file in predicted_file_Names:
        with open(predicted_data_dir_path + "/" + file, encoding='utf-8') as f:
            lines = f.read().split('\n')
            for line in lines:
                word = line.rsplit('\t', 1)
                if (word[0] != ''):
                    word[0] = word[0].replace(word[0], str(labels.index(word[0])))
                    predicted_dict[word[1]] = word[0]
    print("Predicted Dict is: ", predicted_dict)

    common_items = {k: predicted_dict[k] for k in predicted_dict if k in labelled_dict}
    #diff_items = {k: predicted_dict[k] for k in predicted_dict if k in labelled_dict and predicted_dict[k] != labelled_dict[k]}
    print ("length mathched",len(common_items))
    y_true=[]
    y_predict=[]
    for key in common_items:
        y_true.append(labelled_dict[key])
        y_predict.append(predicted_dict[key])
    print("ytrue values",y_true)
    print("ypred values",y_predict)
    confusion_matrix(y_true, y_predict)
    print("confusion matrix value : \n ", confusion_matrix(y_true, y_predict))
    print("accuracy score value : \n ", accuracy_score(y_true, y_predict))
    print("recall score value : \n ", recall_score(y_true, y_predict, average=None, labels=np.unique(y_predict)))
    print("precision score value : \n ", precision_score(y_true, y_predict, average=None, labels=np.unique(y_predict)))

if __name__ == '__main__':
    main()


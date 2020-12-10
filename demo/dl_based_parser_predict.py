import sys
import os
from collections import Counter
from io import StringIO
import pandas as pd
from spacy.matcher import PhraseMatcher
import en_core_web_sm
import matplotlib.pyplot as plt

final_database = pd.DataFrame()
def getresults(dataf):
    
    global final_database
    final_database = final_database.append(dataf)
    final_database = final_database.drop_duplicates()

    final_database2 = final_database['Keyword'].groupby(
        [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace=True)
    final_database2.fillna(0, inplace=True)
    print("database20 \n",final_database2)
    global new_data
    new_data = final_database2.iloc[:, 1:]
    new_data.index = final_database2['Candidate Name']
    # execute the below line if you want to see the candidate profile in a csv format

    sample2 = new_data.to_csv('sample.csv')




def main():

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    from keras_en_parser_and_analyzer.library.dl_based_parser import ResumeParser
    from keras_en_parser_and_analyzer.library.utility.io_utils import read_pdf_and_docx

    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    data_dir_path = current_dir + '/data/test_data'  # directory to scan for any pdf and docx files
    nlp = en_core_web_sm.load()
    template= current_dir + '/data/resumeTemplate_Keys.xlsx'
    keyword_dict= pd.read_excel(template)

    ML_words = [nlp(text) for text in keyword_dict['Machine Learning'].dropna(axis=0)]
    DL_words = [nlp(text) for text in keyword_dict['Deep Learning'].dropna(axis=0)]
    R_words = [nlp(text) for text in keyword_dict['R Language'].dropna(axis=0)]
    python_words = [nlp(text) for text in keyword_dict['Python Language'].dropna(axis=0)]
    Data_Engineering_words = [nlp(text) for text in keyword_dict['Data Engineering'].dropna(axis=0)]
    Java_Developer_words = [nlp(text) for text in keyword_dict['Java Developer'].dropna(axis=0)]
    Web_Developer_words = [nlp(text) for text in keyword_dict['Web Developer'].dropna(axis=0)]
    Quality_Assurance_words = [nlp(text) for text in keyword_dict['Quality Assurance'].dropna(axis=0)]
    UI_UX_developer_words = [nlp(text) for text in keyword_dict['UI UX developer'].dropna(axis=0)]

    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('ML', None, *ML_words)
    matcher.add('DL', None, *DL_words)
    matcher.add('R', None, *R_words)
    matcher.add('Python', None, *python_words)
    matcher.add('DE', None, *Data_Engineering_words)
    matcher.add('Java', None, *Java_Developer_words)
    matcher.add('Web', None, *Web_Developer_words)
    matcher.add('QA', None, *Quality_Assurance_words)
    matcher.add('UI-UX', None, *UI_UX_developer_words)

    #job_desc = input("enter the Job Description: ")
    job_desc=" Familiarity with a variety of designs, languages, and methodologies (e.g. SQL, ORM, J2EE, RabbitMQ, Microservices, Agile and Scrum)Competence and comfort using multiple frameworks (e.g. Spark, Storm, Hadoop, java,angular 2/4/5, Spring Boot)"
    print(job_desc)
    job_desc_doc = nlp(job_desc)
    matches1 = matcher(job_desc_doc)
    matchlist= []
    for match_id, start, end in matches1:
        span = str(job_desc_doc[start: end])
        print("span",type(job_desc_doc[start: end]),span)
        print("Web_Developer_words", type(Web_Developer_words),Web_Developer_words)
        for words in ML_words:
          if span == str(words):
            matchlist.append("ML")
        for words in DL_words:
          if span == str(words):
            matchlist.append("DL")
        for words in R_words:
          if span == str(words):
            matchlist.append("R")
        for words in python_words:
          if span == str(words):
            matchlist.append("Python")
        for words in Data_Engineering_words:
          if span == str(words):
            matchlist.append("DE")
        for words in Java_Developer_words:
          if span == str(words):
            matchlist.append("Java")
        for words in Web_Developer_words:
          if span == str(words):
            matchlist.append("Web")
        for words in Quality_Assurance_words:
          if span == str(words):
            matchlist.append("QA")
        for words in UI_UX_developer_words:
          if span == str(words):
            matchlist.append("UI-UX")

    print("matched values",matchlist)

    def parse_resume(file_path, file_content):
        parser = ResumeParser()
        parser.load_model(current_dir + '/models')
        parser.parse(file_content)
     #   print("rac onent",parser.raw)  # print out the raw contents extracted from pdf or docx files

        if parser.unknown is False:
            print("summary",parser.summary())
            doc = nlp(parser.summary())
            matches = matcher(doc)
            d = []
            for match_id, start, end in matches:
                #         print(match_id, start, end)
                rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'LANGUAGE Name'
                span = doc[start: end]
                d.append((rule_id, span))
        keywords = "\n".join(f'{i[0]} {i[1]} ({j})' for i, j in Counter(d).items())
        df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
        df1 = pd.DataFrame(df.Keywords_List.str.split(' ', 1).tolist(), columns=['Subject', 'Keyword'])
        df2 = pd.DataFrame(df1.Keyword.str.split('(', 1).tolist(), columns=['Keyword', 'Count'])
        df3 = pd.concat([df1['Subject'], df2['Keyword'], df2['Count']], axis=1)



        base = os.path.basename(file_path)
        filename = os.path.splitext(base)[0]

        name = filename.split('_')
        name2 = name[0]
        name2 = name2.lower()
        ## converting str to dataframe
        name3 = pd.read_csv(StringIO(name2), names=['Candidate Name'])


        dataf = pd.concat([name3['Candidate Name'], df3['Subject'], df3['Keyword'], df3['Count']], axis=1)
        dataf['Candidate Name'].fillna(dataf['Candidate Name'].iloc[0], inplace=True)
        
        print('++++++++++++++++++++++++++++++++++++++++++')
        getresults(dataf)


    collected = read_pdf_and_docx(data_dir_path, command_logging=True, callback=lambda index, file_path, file_content: {
      parse_resume(file_path, file_content)
    })
    #print(" final database ", final_database)

    categorised_dict = pd.read_csv('sampletest.csv')
    print(" before sort categorised_dict \n", categorised_dict)
    fileds =  matchlist.copy()
    fileds.insert(0,"Candidate Name")
    categorised_dict=categorised_dict[fileds].sort_values(by=matchlist, ascending=False,ignore_index=True)

    print("after categorised \n", categorised_dict)
    print("after categorised new_dict\n", new_data)
# code to count words under each category and visulaize it through Matplotlib

    plt.rcParams.update({'font.size': 10})
    ax = new_data.plot.barh(title="Resume keywords by category", legend=False, figsize=(25, 7), stacked=True)
    labels = []
    for j in new_data.columns:
        for i in new_data.index:
            label = str(j) + ": " + str(new_data.loc[i][j])
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
    plt.show()


if __name__ == '__main__':
    main()

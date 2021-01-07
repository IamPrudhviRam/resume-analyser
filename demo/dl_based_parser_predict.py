import sys
import os
from collections import Counter
from io import StringIO
import pandas as pd
from pandas.tests.io.excel.test_openpyxl import openpyxl
from spacy.matcher import PhraseMatcher
import en_core_web_sm
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob

final_database = pd.DataFrame()
y = 2


def getresults(dataf):
    global final_database
    final_database = final_database.append(dataf)
    final_database = final_database.drop_duplicates()
    final_database2 = final_database['Keyword'].groupby(
        [final_database['Candidate Name'], final_database['Subject']]).count().unstack()
    final_database2.reset_index(inplace=True)
    final_database2.fillna(0, inplace=True)
    print("final_database \n", final_database2)
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
    data_dir_path = current_dir + '/data/Dataset'  # directory to scan for any pdf and docx files
    nlp = en_core_web_sm.load()

    workbook = openpyxl.load_workbook(current_dir + '/data/ResumeTemplate_Keys.xlsx')
    worksheet = workbook.worksheets[0]
    column_list = []
    for cell in worksheet[1]:
        column_list.append(cell.value)
    if "New Words" in column_list:
        worksheet.delete_cols(9)
    worksheet.insert_cols(9)
    cell_title = worksheet.cell(row=1, column=9)
    cell_title.value = 'New Words'

    def parse_resume(file_path, file_content):
        # predicted_data_dir_path = current_dir + '/data/predicted'
        parser = ResumeParser()
        parser.load_model(current_dir + '/models')
        parser.parse(file_content)
        template = current_dir + '/data/ResumeTemplate_Keys.xlsx'
        keyword_dict = pd.read_excel(template)
        ML_words = [nlp(text.casefold()) for text in keyword_dict['ML Engineer'].dropna(axis=0)]
        HR_words = [nlp(text.casefold()) for text in keyword_dict['Human Resource'].dropna(axis=0)]
        Data_Engineering_words = [nlp(text.casefold()) for text in keyword_dict['Data Engineering'].dropna(axis=0)]
        Java_Developer_words = [nlp(text.casefold()) for text in keyword_dict['Java Developer'].dropna(axis=0)]
        Web_Developer_words = [nlp(text.casefold()) for text in keyword_dict['Web Developer'].dropna(axis=0)]
        Quality_Assurance_words = [nlp(text.casefold()) for text in keyword_dict['Quality Assurance'].dropna(axis=0)]
        UI_UX_developer_words = [nlp(text.casefold()) for text in keyword_dict['UI UX developer'].dropna(axis=0)]
        matcher = PhraseMatcher(nlp.vocab)
        matcher.add('ML', None, *ML_words)
        matcher.add('DE', None, *Data_Engineering_words)
        matcher.add('Java', None, *Java_Developer_words)
        matcher.add('Web', None, *Web_Developer_words)
        matcher.add('QA', None, *Quality_Assurance_words)
        matcher.add('UI-UX', None, *UI_UX_developer_words)
        matcher.add('HR', None, *HR_words)

        if parser.unknown is False:
            print("summary", parser.summary())
            # # TD
            # base = os.path.basename(file_path)
            # filename = os.path.splitext(base)[0]
            # print(filename)
            # output_file_path = os.path.join(data_dir_path, filename + '.txt')
            # print("op file path",output_file_path)
            # if os.path.exists(output_file_path):
            #     return
            # with open(output_file_path, 'wt', encoding='utf8') as f:
            #   f.write(parser.summary())
            doc = nlp(parser.skill_summary().casefold())
            # for removing special charactes code
            # bad_chars = ["", ""]
            # for i in bad_chars:
            #      skill_summary_string=parser.skill_summary().replace(i, " ")
            blob = TextBlob(parser.skill_summary())
            nounwords = list(blob.noun_phrases)
            # eliminating all column from nouns
            matches = matcher(doc)
            d = []
            for match_id, start, end in matches:
                #         print(match_id, start, end)
                rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'LANGUAGE Name'
                span = doc[start: end]
                spanstr = str(span).casefold()
                if spanstr in nounwords:
                    nounwords.remove(spanstr)
                d.append((rule_id, span))
        unique_nouns = list(dict.fromkeys(nounwords))
        # eliminating unw colum form nouns words
        UNW_Words = []
        for text in keyword_dict['UNW'].dropna(axis=0):
            UNW_Words.append(text.strip())
        for UNW in UNW_Words:
            if UNW in unique_nouns:
                unique_nouns.remove(str(UNW))
        global y
        for x in range(len(unique_nouns)):
            cell_to_write = worksheet.cell(row=y, column=9)
            cell_to_write.value = unique_nouns[x]
            y += 1
        # unique values to be loaded in new words column
        workbook.save(current_dir + '/data/ResumeTemplate_Keys.xlsx')
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

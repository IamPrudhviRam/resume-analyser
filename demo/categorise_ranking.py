import sys
import os
import pandas as pd
from spacy.matcher import PhraseMatcher
import en_core_web_sm
nlp = en_core_web_sm.load()






def main():
    print ("***************** Ranking candidates based on job description **************")

    #job_desc = input("enter the Job Description: ")
    job_desc="java"
    job_description = nlp(job_desc)

    current_dir = os.path.dirname(__file__)
    current_dir = current_dir if current_dir is not '' else '.'
    template = current_dir + '/data/resumeTemplate_Keys.xlsx'
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

    print("matcher", matcher)
    matchesWithJD = matcher(job_description)
    matchlistWithJD = []

    for match_id, start, end in matchesWithJD:
        span = str(job_description[start: end])
        print("span",span)
        #can we do this in list comparision instead of loop
        for words in ML_words:
          if span == str(words):
            matchlistWithJD.append("ML")
        for words in Data_Engineering_words:
          if span == str(words):
            matchlistWithJD.append("DE")
        for words in Java_Developer_words:
          if span == str(words):
            matchlistWithJD.append("Java")
        for words in Web_Developer_words:
          if span == str(words):
            matchlistWithJD.append("Web")
        for words in Quality_Assurance_words:
          if span == str(words):
            matchlistWithJD.append("QA")
        for words in UI_UX_developer_words:
          if span == str(words):
            matchlistWithJD.append("UI-UX")
        for words in HR_words:
          if span == str(words):
            matchlistWithJD.append("HR")
    matchlistWithJD = list(set(matchlistWithJD))
    print("Match List With Job Desc:\n", matchlistWithJD)

    categorised_dict = pd.read_csv('sample.csv')
    print(" Candidates Table: \n", categorised_dict)
    categorised_columns = list(categorised_dict.columns)
    matchlistWithJD=list(set(matchlistWithJD).intersection(set(categorised_columns)))
    fileds = matchlistWithJD.copy()
    fileds.insert(0, "Candidate Name")
    categorised_dict['Points'] = categorised_dict.loc[:, matchlistWithJD].sum(axis=1)
    fileds.insert(1, "Points")
    categorised_dict = categorised_dict[fileds].sort_values(by=matchlistWithJD, ascending=False, ignore_index=True)
    categorised_dict = categorised_dict.loc[categorised_dict['Points'] >= 1]
    print(" Categorised Canditates Table: \n", categorised_dict)
    #print(" job description matched values are {} ,resume canditate matched values are {} ".format(matchlistWithJD,))
    # we r having resumes
if __name__ == '__main__':
    main()
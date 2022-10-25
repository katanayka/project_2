import io
import os

import numpy as np
import pandas as pd
import sklearn as sk
# nltk.download("stopwords")
# nltk.download('punkt')
from nltk.corpus import stopwords
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

russian_stopwords = stopwords.words("russian")


def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()


def remove_punctuation(text):
    return ''.join(ch for ch in text if ch.isalnum() or ch == ' ')


def extract_text(pdf_path):

    sub_name = ""
    for page in extract_text_by_page(pdf_path):
        sub_name = page.split('             ')[1].split('Рабочая программа дисциплины')[0]
        break
    PAGE_DEF = []
    i = 0
    cur = 0
    page_list = []
    pdf_lists = extract_text_by_page(pdf_path)
    for page in pdf_lists:

        if page.startswith('МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ') or page.startswith(
                ' МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ') or page.startswith('  МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ'):
            if i > 0:
                cur = i + 1
                PAGE_DEF.append([sub_name, page_list[1:len(page_list)]])
                try:
                    sub_name = page.split('          ')
                    # get string from subname which containts "Рабочая программа"
                    sub_name = [x for x in sub_name if "Рабочая программа" in x][0]
                    try:
                        sub_name = sub_name.split('Рабочая программа')[0].split("       ")[1]
                    except:
                        sub_name = sub_name.split('Рабочая программа')[0].split("      ")[0]
                    print(sub_name)
                except IndexError:
                    print("+++++"+page)
                page_list = []
        i += 1
        if i == 278:
            print(page)
        page_list.append(remove_punctuation(page))
    PAGE_DEF.append([sub_name, page_list[1:len(page_list)]])
    return PAGE_DEF


def remove_stop_words(x):
    return [word for word in x if word not in russian_stopwords]


if __name__ == '__main__':
    blacklist = []
    # create dir to file MOIAIS.pdf in PdfFiles folder
    os.chdir('PdfFiles')
    # pdf_listing = extract_text('MOIAIS.pdf')
    # themes = ['SQL', 'WEB', 'GUI', 'ALGORITHM', 'MATH']
    # for listing in pdf_listing:
    #     print(listing[0])
    #
    # i = 0
    # print(pdf_listing[0])
    # #Set themes for training
    # pdf_listing[0].append(themes[1])  # WEB
    # pdf_listing[1].append(themes[3])  # ALGORITHM
    # pdf_listing[2].append(themes[3])  # ALGORITHM
    # pdf_listing[3].append(themes[3])  # ALGORITHM
    # pdf_listing[4].append(themes[3])  # ALGORITHM
    # pdf_listing[5].append(themes[4])  # MATH
    # pdf_listing[6].append(themes[4])  # MATH
    # pdf_listing[7].append(themes[4])  # MATH
    # pdf_listing[8].append(themes[3])  # ALGORITHM
    # pdf_listing[9].append(themes[3])  # ALGORITHM
    # pdf_listing[10].append(themes[4])  # MATH
    # pdf_listing[11].append(themes[4])  # MATH
    # pdf_listing[12].append(themes[4])  # MATH
    # pdf_listing[13].append(themes[4])  # MATH
    # pdf_listing[14].append(themes[2])  # GUI
    # pdf_listing[15].append(themes[3])  # ALGORITHM
    # pdf_listing[16].append(themes[2])  # GUI
    # pdf_listing[17].append(themes[3])  # ALGORITHM
    # pdf_listing[18].append(themes[3])  # ALGORITHM
    # pdf_listing[19].append(themes[2])  # GUI
    # pdf_listing[20].append(themes[3])  # ALGORITHM
    # pdf_listing[21].append(themes[3])  # ALGORITHM
    # pdf_listing[22].append(themes[3])  # ALGORITHM
    # pdf_listing[23].append(themes[3])  # ALGORITHM
    # pdf_listing[24].append(themes[2])  # GUI
    #
    # Create training data by pandas
    #
    # df = pd.DataFrame(pdf_listing, columns=['Name', 'Text', 'Theme'])
    #Save training data to csv file
    # df.to_csv('training_data.csv', index=False)
    df = pd.read_csv('training_data.csv')

    # Get text from "Пояснительная записк" to "Система оценивания"
    df['Text'] = df['Text'].apply(lambda x: x.split('Пояснительная записка')[1].split('Система оценивания')[0])
    # Remove punctuation
    df['Text'] = df['Text'].apply(lambda x: remove_punctuation(x))
    # Split text to words
    df['Text'] = df['Text'].apply(lambda x: x.split())
    # Get only unique words
    df['Text'] = df['Text'].apply(lambda x: set(x))
    #Concat all words in one string
    df['Text'] = df['Text'].apply(lambda x: ' '.join(x))
    for row in df['Text']:
        print(row)
    # Create text classifier by sklearn to classify themes
    # Create pipeline for text classifier
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
    # Train classifier
    text_clf.fit(df['Text'], df['Theme'])
    # get accuracy of classifier
    print('Accuracy: ', np.mean(text_clf.predict(df['Text']) == df['Theme']))
    for row in df.iterrows():
        #Print row theme and predicted
        print(row[1]['Theme'], text_clf.predict([row[1]['Text']]))
    pdf_listing = extract_text('ISIT.pdf')
    # pdf_listing to dataframe
    df = pd.DataFrame(pdf_listing, columns=['Name', 'Text'])
    df['Text'] = df['Text'].apply(lambda x: x.split('Пояснительная записка')[1].split('Система оценивания')[0])
    # Remove punctuation
    df['Text'] = df['Text'].apply(lambda x: remove_punctuation(x))
    # Split text to words
    df['Text'] = df['Text'].apply(lambda x: x.split())
    # Get only unique words
    df['Text'] = df['Text'].apply(lambda x: set(x))
    # Concat all words in one string
    df['Text'] = df['Text'].apply(lambda x: ' '.join(x))





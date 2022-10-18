import io
import os
import nltk
import wordcloud
import numpy as np
import matplotlib.pyplot as plt
# nltk.download("stopwords")
# nltk.download('punkt')
from nltk.corpus import stopwords
from string import punctuation
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from nltk.probability import FreqDist

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
                ' МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ'):
            if i > 0:
                cur = i + 1
                PAGE_DEF.append([sub_name, page_list[1:len(page_list)]])
                sub_name = page.split('             ')[1].split('Рабочая программа дисциплины')[0]
                page_list = []
        i += 1
        page_list.append(remove_punctuation(page))
    PAGE_DEF.append([sub_name, page_list[1:len(page_list)]])
    return PAGE_DEF


def train(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]
    return tokens


if __name__ == '__main__':
    blacklist = []
    # create dir to file MOIAIS.pdf in PdfFiles folder
    os.chdir('PdfFiles')
    pdf_listing = extract_text('MOIAIS.pdf')
    themes = ['СУБД', 'WEB', 'GUI', 'ALGORITHM']
    # for listing in pdf_listing:
    #     print(listing[0])
    # #
    i = 0
    pdf_listing[0].append(themes[1])  # WEB
    pdf_listing[1].append(themes[3])  # ALGORITHM
    pdf_listing[3].append(themes[0])  # SUDB
    pdf_listing[-1].append(themes[2])  # GUI
    fdis = []
    for listing in pdf_listing:
        i += 1
        # Concat list of string to one string
        text = ' '.join(listing[1])
        text = text.split('Пояснительная записка')[1].split('Система оценивания')[0]
        tokens = train(text)
        fdist = FreqDist(tokens)
        # fdist.plot(30, cumulative=False)

        for fd in fdist:
            try:
                temp = [fd, fdist[fd], listing[2]]
                check = False
                for f in fdis:
                    if f[0] == temp[0] and f[2] == temp[2]:
                        f[1] += temp[1]
                        check = True
                if not check:
                    if temp[0] not in blacklist:
                        fdis.append(temp)
            except:
                pass
    for fd in fdis:
        if fd[1] > 100:
            print(fd)
    for listing in pdf_listing:
        if len(listing) < 3:
            x = 0
            y = 0
            z = 0
            d = 0
            text = ' '.join(listing[1])
            text = text.split('Пояснительная записка')[1].split('Система оценивания')[0].split(' ')
            for fd in fdis:
                if fd[0] in text:
                    if fd[2] == themes[0]:
                        x += fd[1]
                    elif fd[2] == themes[1]:
                        y += fd[1]
                    elif fd[2] == themes[2]:
                        z += fd[1]
                    elif fd[2] == themes[3]:
                        d += fd[1]
            print(x, y, z, d)
            # plt.bar(themes, [x, y*1.1, z*1.1, d])
            # plt.title(listing[0])
            # plt.show()
            listing.append(themes[np.argmax([x, y, z, d])])
    print("DONE FIRST ________________________________________________________________________________________")
    for listing in pdf_listing:
        i += 1
        # Concat list of string to one string
        text = ' '.join(listing[1])
        text = text.split('Пояснительная записка')[1].split('Система оценивания')[0]
        tokens = train(text)
        fdist = FreqDist(tokens)
        for fd in fdist:
            try:
                temp = [fd, fdist[fd], listing[2]]
                check = False
                for f in fdis:
                    if f[0] == temp[0] and f[2] == temp[2]:
                        f[1] += temp[1]
                        check = True
                        break
                if not check: fdis.append(temp)
            except:
                pass
    for fd in fdis:
        if fd[2] == 'ALGORITHM':
            fd[1] *= 0.2
    for listing in pdf_listing:
        x = 0
        y = 0
        z = 0
        d = 0
        text = ' '.join(listing[1])
        for fd in fdis:
            if fd[0] in text:
                tokenss = train(text)
                fdists = FreqDist(tokenss)
                if fd[2] == themes[0]:
                    x += fd[1] * fdists[fd[0]]
                elif fd[2] == themes[1]:
                    y += fd[1] * fdists[fd[0]]
                elif fd[2] == themes[2]:
                    z += fd[1] * fdists[fd[0]]
                elif fd[2] == themes[3]:
                    d += fd[1] * fdists[fd[0]]
        print(x, y, z, d)
        plt.title(listing[0])
        plt.show()
    print("DONE SECOND ________________________________________________________________________________________")

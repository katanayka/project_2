import sqlite3
import pandas as pd

def MOIAIS(url):
    arr = []
    # Read text from MOIAIS.txt
    with open(url, 'r', encoding='UTF-8') as f:
        text = f.read()
    lines = text.splitlines()
    for line in lines:
        arr.append(
            {line.split('-')[0]: line.split(' - ')[1].replace('[', '').replace(']', '').replace(' ', '').split(',')})
    return arr


def add_random():
    bipki = sqlite3.connect('bipki.db')
    c = bipki.cursor()
    # Read data from Test.xlsx
    df = pd.read_excel('Test.xlsx')
    # Append to bipki db (students table) data from df
    # id = 200000+1+i
    # name from df
    # course from df
    # faculty_id from df
    for i in range(100):
        print(type(df['name'][i]),type(int(df['course'][i])), type(int(df['faculty_id'][i])))
        c.execute("INSERT INTO students (id, name, course, faculty_id) VALUES (?, ?, ?, ?)",
                 (200000 + i, df['name'][i], int(df['course'][i]), int(df['faculty_id'][i])))
    # Save (commit) the changes
    bipki.commit()
    # Close connection
    bipki.close()


add_random()
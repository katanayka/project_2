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


def add_random(n):

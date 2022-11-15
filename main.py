import math

import numpy as np
import matplotlib.pyplot as plt
from SplitTeams import bruteForceTeams, getStudlist, Split_Teams, Split_Teams_
from scipy import stats


def bruteForceMethod(amount, needs, directorie, maxIter):
    studList = getStudlist(directorie)
    Teams, history = bruteForceTeams(studList, amount, needs, maxIter)
    if type(Teams) is str:
        print("Количество команд больше, чем количество студентов, либо == 1")
        return 0
    ratings = []
    # Zip teams with their rating
    teams = Teams['teams']
    rating = Teams['teams_rating']
    Teams = list(zip(teams, rating))
    Teams.sort(key=lambda i: i[1])
    for Team in Teams:
        ratings.append(Team[1])
    # printTeams(Teams)
    print(str(np.var(ratings)), " Дисперсия с помощью перебора")
    # plot history
    plt.plot(history)
    plt.show()
    # Check normal test
    print(stats.chisquare(ratings).statistic, " chi square")


def oldMethod(amount, needs, directorie):
    studList = getStudlist(directorie)
    Teams = Split_Teams_(studList, amount, needs)
    if type(Teams) is str:
        print("Количество команд больше, чем количество студентов, либо == 1")
        return 0
    ratings = []
    for Team in Teams:
        ratings.append(list(Team.values()))
    print(str(np.var(ratings)), " Дисперсия с помощью старого метода")
    # printTeams(Teams)
    # Calculate chi square
    print(stats.chisquare(ratings).statistic[0], " chi square")


def graphMethod(amount, needs, directorie):
    studList = getStudlist(directorie)
    Teams = Split_Teams(studList, amount, needs)
    if type(Teams) is str:
        print("Количество команд больше, чем количество студентов, либо == 1")
        return 0
    teams = Teams['teams']
    rating = Teams['teams_rating']
    # Zip teams with their rating
    Teams = list(zip(teams, rating))
    Teams.sort(key=lambda i: i[1])
    # Print teams with their rating
    # printTeams(Teams)
    # Print dispersion of rating
    print(np.var(rating), " Дисперсия с помощью графов")
    print(stats.chisquare(rating).statistic, " chi square")


def printTeams(Teams):
    for Team in Teams:
        print(Team)


if __name__ == '__main__':
    # Указание необходимых технологий
    needness = [{"MATH": 50, "NEURO": 80, "SQL": 100, "WEB": 50}]
    # Количество необходимых команд
    n_amount = 12
    # Путь к файлу с данными
    directory = 'bipki.db'
    # # Вызов функции для старого метода
    oldMethod(n_amount, needness, directory)  # Хорошо работает для большого количества команд, работает быстро
    # Вызов функции для нового метода
    graphMethod(n_amount, needness, directory)  # Хорошо работает для малого количества команд, работает быстро
    # Вызов функции для перебора
    print("Рекомендуемое количество итераций:", int(10**math.sqrt(n_amount*2)))
    bruteForceMethod(n_amount, needness, directory, 100000)  # Хорошо работает для любого количества команд (в зависимости от количества итераций), работает медленно

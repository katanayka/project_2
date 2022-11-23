import os
import random
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import sklearn as sk
# ignore FutureWarning
import warnings

from scipy import stats

warnings.simplefilter(action='ignore', category=FutureWarning)

# Preprocessing of data
def preProcessing(subjectss, needness_compet):
    new_subjectss = []
    for need in needness_compet:
        need = (list(need.keys())[0])
        for subject in subjectss:
            if need in subject[3]:
                new_subjectss.append(subject)
    # Sort new_subjectss by student_id
    new_subjectss.sort(key=lambda x: x[0])
    df = pd.DataFrame(new_subjectss, columns=['student_id', 'subject_id', 'mark', 'theme'])
    df_group = df.groupby('student_id')
    list_of_students = []
    for name, group in df_group:
        list_of_students.append({name: {}})
        for need in needness_compet:
            need = (list(need.keys())[0])
            list_of_students[-1][name][need] = 0
            for subject in new_subjectss:
                if subject[0] == name and need in subject[3]:
                    list_of_students[-1][name][need] += subject[2]
    # Create df from new_subjectss
    df_marks = pd.DataFrame(columns=['student_id', 'theme', 'mark'])
    df = pd.DataFrame(new_subjectss, columns=['student_id', 'subject_id', 'mark', 'theme'])
    df_group = df.groupby('student_id')
    needness_compet = needness_compet[0]
    for name, group in df_group:
        for compet, vv in needness_compet.items():
            comp = compet
            sum_comp = 0
            for row in group.iterrows():
                if comp in (row[1]['theme']):
                    sum_comp += row[1]['mark']
            df_marks = df_marks.append({'student_id': name, 'theme': comp, 'mark': sum_comp}, ignore_index=True)
    return df_marks


def getStudlist(directory):
    # Create connection to database
    bipki = sqlite3.connect(directory)
    cursor = bipki.cursor()
    cursor.execute("SELECT id FROM students WHERE faculty_id = 1")
    students = cursor.fetchall()
    cursor.execute("SELECT id FROM subjects WHERE faculty_id = 1")
    subjects = cursor.fetchall()
    stud_list = []
    for student in students:
        for subject in subjects:
            cursor.execute("Select mark FROM substu WHERE student_id = ? AND subject_id = ?", (student[0], subject[0]))
            mark = cursor.fetchall()
            cursor.execute("Select theme FROM subjects WHERE id = ?", (subject[0],))
            theme = cursor.fetchall()
            try:
                stud_list.append(
                    [student[0], subject[0], (mark[0][0] - 61) / 39 * 100, theme[0][0].split(' ')])
            except AttributeError:
                pass
    return stud_list


def Split_Teams(subjectss, n_amoun, needness_compet):
    df_marks = preProcessing(subjectss, needness_compet)
    result = Generate_balanced_teams(df_marks, n_amoun, needness_compet)
    return result


def Generate_balanced_teams(stud_theme_mark_df, amount_members, compet_needs):
    if amount_members < 2 or len(stud_theme_mark_df) / len(compet_needs) < amount_members:
        return 'Error: amount of members in team must be >= 2 and <= amount of students/amount of competences'
    # Get ratings of each student
    df_group = stud_theme_mark_df.groupby('student_id')
    list_of_students = []
    for name, group in df_group:
        list_of_students.append({name: {}})
        for row in group.iterrows():
            list_of_students[-1][name][row[1]['theme']] = row[1]['mark']
    All_arr_ratings = []
    val_need = []
    compet_needs = compet_needs[0]
    for compet, value in compet_needs.items():
        val_need.append(value)
    for student in list_of_students:
        arr_rating = []
        for i in range(len(val_need)):
            val_need_iter = (val_need[i])
            value = (list((list(student.values())[0]).values())[i])
            arr_rating.append(value / val_need_iter)
        All_arr_ratings.append(np.mean(arr_rating))
    list_of_students = []
    for name, group in df_group:
        list_of_students.append(name)
    stud_rating = dict(zip(list_of_students, All_arr_ratings))
    # Create graph of stud_rating
    G = nx.Graph()
    G.add_nodes_from(stud_rating.keys())
    for i in range(len(stud_rating)):
        for j in range(i + 1, len(stud_rating)):
            G.add_edge(list(stud_rating.keys())[i], list(stud_rating.keys())[j],
                       weight=abs(list(stud_rating.values())[i] - list(stud_rating.values())[j]))
    # plot graph
    nx.draw(G, with_labels=True)
    plt.show()
    # Create balanced teams using graph community detection
    communities_generator = nx.algorithms.community.greedy_modularity_communities(G)
    communities = list(communities_generator)
    communities = list(communities[0])
    # Create teams
    teams = []
    for i in range(amount_members):
        teams.append([])
    for i in range(len(communities)):
        teams[i % amount_members].append(communities[i])
    # That method named "Greedy Modularity Communities" is not always optimal
    # plot histogram of teams rating
    teams_rating = []
    for team in teams:
        sum_rating = 0
        for student in team:
            sum_rating += stud_rating[student]
        teams_rating.append(sum_rating / len(team))
    plt.hist(teams_rating)
    plt.show()
    return {'teams': teams, 'teams_rating': teams_rating}


def Split_Teams_(subjectss, n_amoun, needness_compet):
    df_marks = preProcessing(subjectss, needness_compet)
    result = SplitTeams_First_method_(df_marks, n_amoun, needness_compet)
    return result


def SplitTeams_First_method_(stud_theme_mark_df, amount_members, compet_needs):
    if amount_members < 2 or len(stud_theme_mark_df) / len(compet_needs) < amount_members:
        return 'Error: amount of members in team must be >= 2 and <= amount of students/amount of competences'
        # Get ratings of each student
    df_group = stud_theme_mark_df.groupby('student_id')
    list_of_students = []
    for name, group in df_group:
        list_of_students.append({name: {}})
        for row in group.iterrows():
            list_of_students[-1][name][row[1]['theme']] = row[1]['mark']
    All_arr_ratings = []
    val_need = []
    compet_needs = compet_needs[0]
    for compet, value in compet_needs.items():
        val_need.append(value)
    for student in list_of_students:
        arr_rating = []
        for i in range(len(val_need)):
            val_need_iter = (val_need[i])
            value = (list((list(student.values())[0]).values())[i])
            arr_rating.append(value / val_need_iter)
        All_arr_ratings.append(np.mean(arr_rating))
    list_of_students = []
    for name, group in df_group:
        list_of_students.append(name)
    stud_rating = dict(zip(list_of_students, All_arr_ratings))
    # Create graph of stud_rating
    G = nx.Graph()
    G.add_nodes_from(stud_rating.keys())
    for i in range(len(stud_rating)):
        for j in range(i + 1, len(stud_rating)):
            G.add_edge(list(stud_rating.keys())[i], list(stud_rating.keys())[j],
                       weight=abs(list(stud_rating.values())[i] - list(stud_rating.values())[j]))
    # plot graph
    nx.draw(G, with_labels=True)
    plt.show()
    # Create balanced teams
    teams = []
    for i in range(amount_members):
        teams.append([])
    # Get list of students sorted by rating
    sorted_stud_rating = sorted(stud_rating.items(), key=lambda x: x[1])
    # Add students to teams
    # We will use greedy algorithm
    for i in range(len(sorted_stud_rating)):
        teams[i % amount_members].append(sorted_stud_rating[i][0])
    teams_with_mean = []
    for team in teams:
        sum = 0
        for student in team:
            sum += stud_rating[student]
        teams_with_mean.append({str(team): sum / len(team)})
    # make plot of teams
    for team in teams_with_mean:
        plt.bar(list(team.keys())[0], list(team.values())[0])
    plt.show()
    return teams_with_mean


class SplitTeams_BruteForce_:
    best_team = []
    best_team_rating = 0
    iter = 0
    best_diff = 99999
    history = []

    def __init__(self, stud_theme_mark_df, amount_members, compet_needs, iters):
        self.stud_theme_mark_df = stud_theme_mark_df
        self.amount_members = amount_members
        self.compet_needs = compet_needs
        self.iter = iters
        self.stud_rating = self.get_stud_rating()
        self.history = []

    def SplitTeams_BruteForce(self):
        for i in range(self.iter):
            teams = self.splitTeams(i)
            teams_rating = self.get_teams_rating(teams)
            if stats.chisquare(teams_rating).statistic < self.best_diff or self.best_diff == 99999:
                self.best_diff = stats.chisquare(teams_rating).statistic
                self.best_team = teams
                self.best_team_rating = teams_rating
                # append to history variance of teams rating
                self.history.append(stats.chisquare(teams_rating).statistic)
            if i% (self.iter/100) == 0:
                print(i/(self.iter/100), '%')
        # plot teams rating
        plt.hist(self.best_team_rating)
        plt.show()
        return {'teams': self.best_team, 'teams_rating': self.best_team_rating}, self.history

    def splitTeams(self,i):
        seed = i
        random.seed(seed)
        # Randomly split students into teams and calculate rating of each team
        Teams = []
        listofStudents = list(self.stud_rating.keys())
        listofRatings = list(self.stud_rating.values())
        Studs = list(zip(listofStudents, listofRatings))
        random.shuffle(Studs)
        for i in range(self.amount_members):
            Teams.append([])
        for i in range(len(Studs)):
            Teams[i % self.amount_members].append(Studs[i][0])
        return Teams

    def get_stud_rating(self):
        # Get ratings of each student
        df_group = self.stud_theme_mark_df.groupby('student_id')
        list_of_students = []
        for name, group in df_group:
            list_of_students.append({name: {}})
            for row in group.iterrows():
                list_of_students[-1][name][row[1]['theme']] = row[1]['mark']
        All_arr_ratings = []
        val_need = []
        compet_needs = self.compet_needs[0]
        for compet, value in compet_needs.items():
            val_need.append(value)
        for student in list_of_students:
            arr_rating = []
            for i in range(len(val_need)):
                val_need_iter = (val_need[i])
                value = (list((list(student.values())[0]).values())[i])
                arr_rating.append(value / val_need_iter)
            All_arr_ratings.append(np.mean(arr_rating))
        list_of_students = []
        for name, group in df_group:
            list_of_students.append(name)
        stud_rating = dict(zip(list_of_students, All_arr_ratings))
        return stud_rating

    def get_teams_rating(self, teams):
        # Calculate rating of each team
        teams_rating = []
        for team in teams:
            sum = 0
            for student in team:
                sum += self.stud_rating[student]
            teams_rating.append(sum / len(team))
        return teams_rating


def bruteForceTeams(subjectss, n_amoun, needness_compet, iters):
    df_marks = preProcessing(subjectss, needness_compet)
    result, history = SplitTeams_BruteForce_(df_marks, n_amoun, needness_compet, iters).SplitTeams_BruteForce()
    return result, history




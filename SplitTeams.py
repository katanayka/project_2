import os
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
import sklearn as sk
# ignore FutureWarning
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def Split_Teams(subjectss, n_amoun, needness_compet):
    # subjectss = list of subjects:
    #   subjectss[:][0] - id of student
    #   subjectss[:][1] - id of subject
    #   subjectss[:][2] - mark of subject (float, from 0 to 100)
    #   subjectss[:][3] - theme of subject (List of strings)
    # n_amoun = amount of teams
    # needness_compet = list of needness competences with their weights
    new_subjectss = []
    for need in needness_compet:
        need = (list(need.keys())[0])
        for subject in subjectss:
            if need in subject[3]:
                new_subjectss.append(subject)
    new_list = []
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
    for name, group in df_group:
        for compet in needness_compet:
            comp = list(compet.keys())[0]
            sum_comp = 0
            for row in group.iterrows():
                if comp in (row[1]['theme']):
                    sum_comp += row[1]['mark']
            df_marks = df_marks.append({'student_id': name, 'theme': comp, 'mark': sum_comp}, ignore_index=True)
    result = Generate_balanced_teams(df_marks, n_amoun, needness_compet)
    return result







def Generate_balanced_teams(stud_theme_mark_df, amount_members, compet_needs):
    if amount_members < 2 or len(stud_theme_mark_df) / len(compet_needs) < amount_members:
        return ('Error: amount of members in team must be >= 2 and <= amount of students/amount of competences')
    # Get ratings of each student
    df_group = stud_theme_mark_df.groupby('student_id')
    list_of_students = []
    for name, group in df_group:
        list_of_students.append({name: {}})
        for row in group.iterrows():
            list_of_students[-1][name][row[1]['theme']] = row[1]['mark']
    All_arr_ratings = []
    for student in list_of_students:
        arr_rating = []
        for i in range(len(compet_needs)):
            val_need = (list(compet_needs[i].values())[0])
            value = (list((list(student.values())[0]).values())[i])
            arr_rating.append(value / val_need)
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
    #plot histogram of teams rating
    teams_rating = []
    for team in teams:
        sum_rating = 0
        for student in team:
            sum_rating += stud_rating[student]
        teams_rating.append(sum_rating / len(team))
    for i in range(len(teams_rating)):
        print('Team ' + str(i) + ' rating: ' + str(teams_rating[i]), teams[i])
    plt.hist(teams_rating)
    plt.show()
    return {'teams': teams, 'teams_rating': teams_rating}




def SplitTeams(n_amount, needness, directory):
    # Create connection to database
    bipki = sqlite3.connect(directory)
    cursor = bipki.cursor()
    cursor.execute("SELECT id FROM students WHERE faculty_id = 1")
    students = cursor.fetchall()
    cursor.execute("SELECT id FROM subjects WHERE faculty_id = 1")
    subjects = cursor.fetchall()
    needness = needness
    n_amount = n_amount  # -- Amount of teams
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
            except(AttributeError):
                pass
    teams = Split_Teams(stud_list, n_amount, needness)
    return teams





def Split_Teams_(subjectss, n_amoun, needness_compet):
    # subjectss = list of subjects:
    #   subjectss[:][0] - id of student
    #   subjectss[:][1] - id of subject
    #   subjectss[:][2] - mark of subject (float, from 0 to 100)
    #   subjectss[:][3] - theme of subject (List of strings)
    # n_amoun = amount of teams
    # needness_compet = list of needness competences with their weights
    new_subjectss = []
    for need in needness_compet:
        need = (list(need.keys())[0])
        for subject in subjectss:
            if need in subject[3]:
                new_subjectss.append(subject)
    new_list = []
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
    for name, group in df_group:
        for compet in needness_compet:
            comp = list(compet.keys())[0]
            sum_comp = 0
            for row in group.iterrows():
                if comp in (row[1]['theme']):
                    sum_comp += row[1]['mark']
            df_marks = df_marks.append({'student_id': name, 'theme': comp, 'mark': sum_comp}, ignore_index=True)
    result = SplitTeams_First_method_(df_marks, n_amoun, needness_compet)
    return result

def SplitTeams_First_method_(stud_theme_mark_df, amount_members, compet_needs):
    if amount_members < 2 or len(stud_theme_mark_df) / len(compet_needs) < amount_members:
        return ('Error: amount of members in team must be >= 2 and <= amount of students/amount of competences')
        # Get ratings of each student
    df_group = stud_theme_mark_df.groupby('student_id')
    list_of_students = []
    for name, group in df_group:
        list_of_students.append({name: {}})
        for row in group.iterrows():
            list_of_students[-1][name][row[1]['theme']] = row[1]['mark']
    All_arr_ratings = []
    for student in list_of_students:
        arr_rating = []
        for i in range(len(compet_needs)):
            val_need = (list(compet_needs[i].values())[0])
            value = (list((list(student.values())[0]).values())[i])
            arr_rating.append(value / val_need)
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

def SplitTeams_(n_amount, needness, directory):
    # Create connection to database
    bipki = sqlite3.connect(directory)
    cursor = bipki.cursor()
    cursor.execute("SELECT id FROM students WHERE faculty_id = 1")
    students = cursor.fetchall()
    cursor.execute("SELECT id FROM subjects WHERE faculty_id = 1")
    subjects = cursor.fetchall()
    needness = needness
    n_amount = n_amount  # -- Amount of teams
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
            except(AttributeError):
                pass
    teams = Split_Teams_(stud_list, n_amount, needness)
    return teams
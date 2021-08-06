from os import stat
import numpy as np
import pandas as pd
import plotly.express as px
from collections import Counter

file = pd.ExcelFile(r'grades.xlsx')
quarter_sheets = dict()
statistics = []

def get_quarters():
    return file.sheet_names

def populate_quarter_sheets():
    if len(quarter_sheets) == 0:
        for q in get_quarters():
            d = file.parse(q)
            d['Instructor'] = d['Instructor'] + ' (' + q + ')'
            d.Course = d.Course.replace('\s+', ' ', regex=True)
            quarter_sheets[q] = d

def get_classes_based_off_quarter(quarters):
    data = pd.concat([quarter_sheets[q] for q in quarters])
    return data['Course'].unique()

def get_professor_based_off_class_and_quarter(course, quarters):
    data = pd.concat([quarter_sheets[q] for q in quarters])
    only_course = data[data['Course'] == course]
    professors = only_course['Instructor'].unique()

    unique_professors_dict = Counter([p.split(' (')[0] for p in professors])
    unique_professors = []
    for p in professors:
        if unique_professors_dict[p.split(' (')[0]] > 1:
            unique_professors.append(p)
        else:
            unique_professors.append(p.split(' (')[0])
            only_course = only_course.replace(p, p.split(' (')[0])
    professors = unique_professors

    return [professors, only_course]

def avg(counts, gpas):
    return np.sum(np.dot(counts, gpas)) / np.sum(counts)

def median(counts, gpas):
    n = 0
    half_students = np.sum(counts)/2
    for i in range(len(gpas)):
        n += counts[i]
        if (n > half_students):
            return gpas[i]

def std_dev(counts, gpas):
    mean = avg(counts, gpas)
    result = 0
    for i in range(len(gpas)):
        result += ((gpas[i] - mean)**2) * counts[i]
    return (result/np.sum(counts))**(0.5)


def getStatistics():
    return statistics

#——————————————————————————————————————————————————————————#

def plot(course, quarters, professors, percentage, dataframe):
    labels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
    gpas = [4.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
    cols = pd.DataFrame({'Grade': labels})

    # if not professors or len(professors) == 0:
    #     do something
    statistics.clear()

    for professor in professors:
        other = dataframe[dataframe['Instructor'] == professor][['Grade Given', 'Sum of Student Count']]
        other.columns = ['Grade', professor]

        counts = pd.DataFrame({'Grade': labels}).set_index('Grade').join(other.set_index('Grade'))[professor].fillna(0)
        statistics.append({'Professor': professor, 'Median': str(median(counts, gpas)), 'Average': str(round(avg(counts, gpas), 2)), 'Standard Deviation': str(round(std_dev(counts, gpas), 2))})

        if percentage:
            other[professor] = other[professor].div(np.sum(other[professor]), axis=0)

        cols = cols.set_index('Grade').join(other.set_index('Grade')).reset_index()

    cols = cols.set_index('Grade')
    cols = cols.fillna(0)

    #——————————————————————————————————————————————————————————#

    fig = px.bar(cols, labels={
            'Grade': 'Grade',
            'value': 'Percentage of Students' if percentage else 'Number of Students',
            'variable': 'Professor'
        },
        title=course,
        barmode='group'
    )
    if percentage:
        fig.update_layout(yaxis_tickformat = '%')
    return fig
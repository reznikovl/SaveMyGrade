import numpy as np
import pandas as pd
import re
import json
import pickle
from os.path import exists
import plotly.express as px
from collections import Counter

labels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
labels_non_letter = ['P', 'NP', 'S']
gpas = [4.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
na = '---'

file = pd.ExcelFile(r'grades.xlsx')
professor_data = dict()
quarter_sheets = dict()
quarter_sheets_no_quarter = dict()
statistics = []

def get_quarters():
    return file.sheet_names

def populate_quarter_sheets():
    if not professor_data:
        with open('data/profs.txt', 'r') as j:
            professor_data.update(json.loads(j.read()))

    if len(quarter_sheets) == 0:
        for q in get_quarters():
            path = 'data/' + q + '.txt'
            if exists(path):
                d = pd.read_json(path)
                quarter_sheets_no_quarter[q] = d.copy()
            else:
                d = file.parse(q)
                d.Course = d.Course.replace('\s+', ' ', regex=True)
                d.Course = d.Course.str.replace('ES 1-', 'ES', regex=False)
                d.Course = d.Course.str.replace('ED HSS', 'ED HSS ', regex=False)
                d.Course = d.Course.str.replace('ED SPS', 'ED SPS ', regex=False)
                # d.Course = d.Course.str.replace('(?<=ED .) ', '', regex=True)
                # d.Course = d.Course.str.replace('(?<=ED .{2}) ', '', regex=True)
                quarter_sheets_no_quarter[q] = d.copy()
                f = open(path, 'w+')
                f.write(json.dumps(json.loads(d.to_json())))
                f.close()

            abbrev = ('M' if q.startswith('Summer') else q[0]) + q.split(' ')[1][2:]
            d['Instructor'] = d['Instructor'] + ' (' + abbrev + ') '
            quarter_sheets[q] = d

def get_departments_based_off_quarter(quarters):
    data = pd.concat([quarter_sheets[q] for q in quarters])
    departments = [d[:d.rfind(' ')] for d in data['Course'].unique()]
    return sorted(list(set(departments)))

def get_numbers_based_off_quarters_and_department(quarters, department):
    union_course_numbers = None
    for q in quarters:
        courses = [c for c in quarter_sheets[q]['Course'].unique() if c[:c.rfind(' ')] == department]
        course_numbers = [c.split(' ')[-1] for c in courses]
        union_course_numbers = course_numbers if not union_course_numbers else union(union_course_numbers, course_numbers)
    return union_course_numbers

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
    professors = unique_professors

    return professors

def avg(counts):
    total = np.sum(counts)
    return np.sum(np.dot(counts, gpas)) / total

def median(counts):
    n = 0
    half_students = np.sum(counts)/2
    for i in range(len(gpas)):
        n += counts[i]
        if (n > half_students):
            return str(gpas[i]) + ' (' + str(labels[i]) + ')'

def std_dev(counts):
    mean = avg(counts)
    result = 0
    for i in range(len(gpas)):
        result += ((gpas[i] - mean)**2) * counts[i]
    return (result/np.sum(counts))**(0.5)

def points_to_grade(points):
    if points == na:
        return ''
    return ' (' + labels[len(labels) - np.searchsorted(gpas[::-1], points, side='right')] + ')'

def splitter(x):
    match = re.compile("[^\W\d]").search(x)
    if match:
        return (int(x[:match.start()]), x[match.start():])
    return (int(x), '')

def union(lst1, lst2):
    return sorted(set(lst1).union(set(lst2)), key=lambda x:splitter(x))

def get_data(professor):
    if professor in professor_data:
        return professor_data[professor]
    elif professor.rsplit(' ', 1)[0] in professor_data:
        return professor_data[professor.rsplit(' ', 1)[0]]
    else:
        parts = professor.split(' ')
        if len(parts) == 2:
            arrange = ' '.join([parts[0], parts[1][0]])
            if arrange in professor_data:
                return professor_data[arrange]

        for k, v in professor_data.items():
            if str(k).startswith(professor) \
                or (str(k).startswith(professor.split(' ', 1)[0]) and True):
                return v
        return 'N/A'

def get_rating(professor):
    data = get_data(professor)
    if data == 'N/A' or data[1] == 'N/A':
        return '---'
    return data[1] + ('*' if data[2] <= 5 else '')

def get_professor_based_off_department(department):
    data = pd.concat([quarter_sheets_no_quarter[q] for q in get_quarters()])[['Course', 'Instructor']]
    data = data[data['Course'].str.startswith(department)]

    professors = data['Instructor'].unique().tolist()
    professors = [str(s) for s in professors]
    return sorted(professors)

def get_statistics_of_professor(professor, show_na):
    statistics = []
    total_counts = pd.DataFrame()
    for q in get_quarters():
        data = quarter_sheets_no_quarter[q]
        data = data[data['Instructor'] == professor]

        for course in data['Course'].unique().tolist():
            df = data[data['Course'] == course][['Grade Given', 'Sum of Student Count']]

            df.columns = ['Grade', professor]
            counts = pd.DataFrame({'Grade': labels}).set_index('Grade').join(df.set_index('Grade'))[professor].fillna(0)
            if total_counts.empty:
                total_counts = counts
            else:
                total_counts = total_counts + counts

            med = median(counts) or na
            mean = round(avg(counts), 2)
            if np.isnan(mean):
                mean = na
            dev = round(std_dev(counts), 2)
            if np.isnan(dev):
                dev = na

            if (show_na or not (med is na or mean is na or dev is na)):
                statistics.append({'quarter': q, 'course': course, 'median': str(med), 'average': str(mean) + points_to_grade(mean), 'deviation': str(dev), 'count': sum(df[professor])})

    med = median(total_counts) or na
    mean = round(avg(total_counts), 2)
    if np.isnan(mean):
        mean = na
    dev = round(std_dev(total_counts), 2)
    if np.isnan(dev):
        dev = na
    return statistics, [{'median': str(med), 'average': str(mean) + points_to_grade(mean), 'deviation': str(dev)}]

#——————————————————————————————————————————————————————————#

def plot(course, quarters, professors, percentage):
    data = pd.concat([quarter_sheets[q] for q in quarters])
    only_course = data[data['Course'] == course]
    
    new_professors = only_course['Instructor'].tolist()
    for i in range(len(new_professors)):
        if new_professors[i].split(' (')[0] in professors:
            new_professors[i] = new_professors[i].split(' (')[0]
    only_course = only_course.assign(Instructor=new_professors)

    cols = pd.DataFrame({'Grade': labels})

    statistics.clear()

    for professor in professors:
        other = only_course[only_course['Instructor'] == professor][['Grade Given', 'Sum of Student Count']]
        other.columns = ['Grade', professor]

        counts = pd.DataFrame({'Grade': labels}).set_index('Grade').join(other.set_index('Grade'))[professor].fillna(0)
        med = median(counts) or na
        
        mean = round(avg(counts), 2)
        if np.isnan(mean):
            mean = na
        dev = round(std_dev(counts), 2)
        if np.isnan(dev):
            dev = na
        statistics.append({'professor': professor, 'median': str(med), 'average': str(mean) + points_to_grade(mean), 'deviation': str(dev), 'count': sum(other[professor]), 'rating': str(get_rating(professor.split(' (')[0]))})

        if percentage:
            other[professor] = other[professor].div(np.sum(other[professor]), axis=0)

        cols = cols.set_index('Grade').join(other.set_index('Grade')).reset_index()

    cols = cols.set_index('Grade')
    cols = cols.fillna(0)

    #——————————————————————————————————————————————————————————#

    fig = px.bar(cols, labels={
            'Grade': 'Grade',
            'value': 'Percent of Students' if percentage else 'Number of Students',
            'variable': 'Professor'
        },
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99,
        
    ), margin=dict(l=20, r=0, t=0, b=0))
    fig.update_xaxes(title=None, fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    if percentage:
        fig.update_layout(yaxis_tickformat = '%')
    if np.all((fig['data'][0]['y'] == 0)):
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "No letter-grade data found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    return fig, statistics
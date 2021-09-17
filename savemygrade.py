import numpy as np
import pandas as pd
import plotly.express as px
from collections import Counter

labels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
gpas = [4.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]

file = pd.ExcelFile(r'grades.xlsx')
quarter_sheets = dict()
quarter_sheets_no_quarter = dict()
statistics = []

def get_quarters():
    # return ['Winter 2021']
    return file.sheet_names

def populate_quarter_sheets():
    if len(quarter_sheets) == 0:
        for q in get_quarters():
            d = file.parse(q)
            d.Course = d.Course.replace('\s+', ' ', regex=True)
            d.Course = d.Course.str.replace('ES 1-', 'ES', regex=False)
            d.Course = d.Course.str.replace('(?<=ED .) ', '', regex=True)
            d.Course = d.Course.str.replace('(?<=ED .{2}) ', '', regex=True)
            quarter_sheets_no_quarter[q] = d.copy()
            d['Instructor'] = d['Instructor'] + ' (' + q + ')'
            quarter_sheets[q] = d

def get_classes_based_off_quarter(quarters):
    data = pd.concat([quarter_sheets[q] for q in quarters])
    return data['Course'].unique()

def get_departments_based_off_quarter(quarters):
    data = pd.concat([quarter_sheets[q] for q in quarters])
    departments = [d[:d.rfind(' ')] for d in data['Course'].unique()]
    return sorted(list(set(departments)))

def get_numbers_based_off_quarters_and_department(quarters, department):
    common_course_numbers = None
    for q in quarters:
        courses = [c for c in quarter_sheets[q]['Course'].unique() if c[:c.rfind(' ')] == department]
        course_numbers = [c.split(' ')[-1] for c in courses]
        common_course_numbers = course_numbers if not common_course_numbers else intersection(common_course_numbers, course_numbers)
    return common_course_numbers

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

def avg(counts, gpas):
    total = np.sum(counts)
    return np.sum(np.dot(counts, gpas)) / total

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

def intersection(lst1, lst2):
    temp = set(lst2)
    return [value for value in lst1 if value in temp]

def get_professor_based_off_department(department):
    data = pd.concat([quarter_sheets_no_quarter[q] for q in get_quarters()])[['Course', 'Instructor']]
    data = data[data['Course'].str.startswith(department)]

    professors = data['Instructor'].unique().tolist()
    professors = [str(s) for s in professors]
    return sorted(professors)

def get_statistics_of_professor(professor):
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

            med = median(counts, gpas) or 'N/A'
            mean = round(avg(counts, gpas), 2)
            if np.isnan(mean):
                mean = 'N/A'
            dev = round(std_dev(counts, gpas), 2)
            if np.isnan(dev):
                dev = 'N/A'
            statistics.append({'Quarter': q, 'Course': course, 'Median': str(med), 'Average': str(mean), 'Standard Deviation': str(dev)})

    med = median(total_counts, gpas) or 'N/A'
    mean = round(avg(counts, gpas), 2)
    if np.isnan(mean):
        mean = 'N/A'
    dev = round(std_dev(counts, gpas), 2)
    if np.isnan(dev):
        dev = 'N/A'
    return statistics, [{'Overall Median': str(med), 'Overall Average': str(mean), 'Overall Standard Deviation': str(dev)}]

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
        med = median(counts, gpas) or 'N/A'
        mean = round(avg(counts, gpas), 2)
        if not np.isnan(mean):
            mean = 'N/A'
        dev = round(std_dev(counts, gpas), 2)
        if not np.isnan(dev):
            dev = 'N/A'
        statistics.append({'Professor': professor, 'Median': str(med), 'Average': str(mean), 'Standard Deviation': str(dev)})

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
                    "text": "No data found",
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
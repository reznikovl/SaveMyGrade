import numpy as np
import pandas as pd
import plotly.express as px

file = pd.ExcelFile(r'grades.xlsx')
def get_quarters():
    return file.sheet_names

def get_classes_based_off_quarter(quarter):
    data = pd.read_excel(file, quarter)
    data.Course = data.Course.replace('\s+', ' ', regex=True)
    return data['Course'].unique()

def get_professor_based_off_class_and_quarter(course, quarter):
    data = pd.read_excel(file, quarter)
    data.Course = data.Course.replace('\s+', ' ', regex=True)
    courses =  data[data['Course'] == course]
    return courses['Instructor'].unique()

def median(column, gpas):
    n = 0
    half_students = np.sum(column)/2
    for i in range(len(gpas)):
        n += column[i]
        if (n > half_students):
            return gpas[i]

#——————————————————————————————————————————————————————————#


#——————————————————————————————————————————————————————————#
def plot(course, quarter, professors, percentage):
    data = pd.read_excel(file, quarter)
    data.Course = data.Course.replace('\s+', ' ', regex=True)

    df = data[data['Course'] == course]

    labels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
    gpas = [4.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
    cols = pd.DataFrame({'Grade': labels})

    statistics = []

    if not professors or len(professors) == 0:
        professors = df['Instructor'].unique()
    for professor in professors:
        other = df[df['Instructor'] == professor][['Grade Given', 'Sum of Student Count']]
        other.columns = ['Grade', professor]

        counts = pd.DataFrame({'Grade': labels}).set_index('Grade').join(other.set_index('Grade'))[professor].fillna(0)
        statistics.append([ professor, np.sum(np.dot(counts, gpas)) / np.sum(counts), median(counts, gpas) ])

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
        title=course + ' – ' + quarter,
        barmode='group'
    )
    if percentage:
        fig.update_layout(yaxis_tickformat = '%')
    # fig.show()
    return fig

# course = 'MATH 8'
# quarter = 'Winter 2020'
# professors = []
# percentage = True

# plot(course, quarter, professors, percentage)
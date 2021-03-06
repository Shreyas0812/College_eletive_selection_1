# -*- coding: utf-8 -*-
"""Collaborative_Filtering_1_sem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gL8GbTey-txcq7qpy44wKE8ho6Rz0nxD

"""

"""Importing Libraries:"""

import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

"""Preparing the Data"""

df = pd.read_excel('Student_Performance_Data.xlsx', sheet_name='Sheet1')

df_dict_sem = {}
for name in df['Semster_Name'].unique():
    df_dict_sem[name] = df[df['Semster_Name'] == name].reset_index(drop=True)

key = input('Please Enter Your Semester (sem_1, Sem_2, Sem_3, Sem_4, Sem_5, Sem_6, Sem_7, Sem_8) : ')
known_ip = input('Please enter the already selected Papers with a "," (Paper 1, Paper 2, Paper 3, Paper 4, Paper 5, Paper 6, Paper7) : ')

known_solution = known_ip.split(',')

marks_thresh = 75

df_sem = df_dict_sem[key]
df_sem.head()

#Applying Marks Threshold
df_sem_marks_thresh = df_sem[df_sem['Marks'] > marks_thresh].reset_index(drop=True)
df_sem_marks_thresh.head()

#getting only the sudent ID and the paper name
df_sem_marks_thresh_ID_Paper = df_sem_marks_thresh[['Student_ID', 'Paper_Name']]
df_sem_marks_thresh_ID_Paper

df_sem_dummies = pd.get_dummies(df_sem_marks_thresh_ID_Paper, prefix=[None], columns=['Paper_Name'])
df_sem_encoded = df_sem_dummies.groupby(['Student_ID'], axis=0).sum().reset_index()
df_sem_encoded.head()

ser = pd.Series(0, index = df_sem_encoded.columns)
ser[known_solution] = 1
ser['Student_ID'] = 'NEW_VALUE'
ser

df_sem_encoded = df_sem_encoded.append(ser, ignore_index=True)
df_sem_encoded.head()

"""#### Item-Item Calculations:"""

#dropping student ID column for calculation purposes
data_sem_calc = df_sem_encoded.drop(columns="Student_ID")
data_sem_calc.head()

#normalizing
magnitude = np.sqrt(np.square(data_sem_calc).sum(axis=1))
data_sem_calc = data_sem_calc.divide(magnitude, axis='index')

#Taking Age into account (To be done later)

#Calculating Similartiy of items and store it in a sparse matrix
def calculate_similarity(data_sem_calc):
    data_sparse = sparse.csr_matrix(data_sem_calc)
    similarities =  cosine_similarity(data_sparse.transpose())
    df_sim = pd.DataFrame(data=similarities, index=data_sem_calc.columns, columns=data_sem_calc.columns)
    return df_sim

data_sem_matrix = calculate_similarity(data_sem_calc)
data_sem_matrix

"""#### User-Item Calculations:"""

#Storing top 4 papers 
n_similarity_values = 4
data_sem_neighbours = pd.DataFrame(index=data_sem_matrix.columns, columns = range(1, n_similarity_values+1))
for i in range(len(data_sem_matrix.columns)):
    data_sem_neighbours.iloc[i, :n_similarity_values] = data_sem_matrix.iloc[0:, i].sort_values(ascending=False)[:n_similarity_values].index
data_sem_neighbours

most_similar_to_solution_sem = data_sem_neighbours.loc[known_solution]
similar_list_sem = most_similar_to_solution_sem.values.tolist()
similar_list_sem = list(set([item for sublist in similar_list_sem for item in sublist]))
similar_list_sem

#similarity b/w above mentioned similar elements
neighbourhood_sem = data_sem_matrix[similar_list_sem].loc[similar_list_sem]
neighbourhood_sem

#possible solutions that exist based on similarity List
Solution_index_sem = df_sem_encoded[df_sem_encoded.Student_ID == 'NEW_VALUE'].index.tolist()[0]
Solution_vector_sem = data_sem_calc.iloc[Solution_index_sem].loc[similar_list_sem]
Solution_vector_sem

#calculating score for final result (Cosine similarity)
score_sem = neighbourhood_sem.dot(Solution_vector_sem).div(neighbourhood_sem.sum(axis=1))
score = score_sem.drop(known_solution)
score_sem

#known or selected already
print('Known Solution: ', known_solution)

n_recommendation_sem = 2
top_n_recommendation = score.nlargest(n_recommendation_sem).index.tolist()
print('Top Recommendations:', top_n_recommendation)


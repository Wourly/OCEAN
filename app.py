# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
# LAYOUT --------------------------------------
app.layout = html.Div([
    html.Div([
	html.Label('Parameter'),
    dcc.Dropdown(
		id = 'parameter',
        options=[
            {'label': 'Age', 'value': 'age'},
            {'label': 'Education', 'value': 'education'},
            {'label': 'Gender', 'value': 'gender'}
        ],
        value='age'
    ),

    html.Label('Dimension'),
    dcc.Dropdown(
		id = 'dimension',
        options=[
            {'label': 'Agreeableness', 'value': 'agreeableness'},
            {'label': 'Conscientiousness', 'value': 'conscientiosness'},
            {'label': 'Extraversion', 'value': 'extraversion'},
			{'label': 'Neuroticism', 'value': 'neuroticism'},
            {'label': 'Openness', 'value': 'openness'}
        ],
        value='agreeableness'
    ),],
	
	style = {}
	
	
	),
	
	html.Div([
    dcc.Graph(id="graph")
	])

], style = {})
# CALLBACK -----------------------------
@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='parameter', component_property='value'),
    Input(component_id='dimension', component_property='value')]
)

def update_figure(parameter, dimension):

	if parameter == 'age':
		lake = lake_age
	elif parameter == 'education':
		lake = lake_edu
	else:
		lake = lake_gen

		
	if dimension == 'agreeableness':
		column = "A"
	elif dimension == 'conscientiosness':
		column = "C"
	elif dimension == 'extraversion':
		column = "E"
	elif dimension == 'neuroticism':
		column = "N"
	else:
		column = "O"
		
	data = [
            {'x': ocean[parameter], 'y': ocean[column], 'type': 'box', 'name': 'respondents'},
            {'x': lake[parameter], 'y': lake[column], 'type': 'scatter', 'name': 'mean'},
        ]

	figure = {
        'data': data,
        'layout': {
            'title': 'Relationship of {} and {}:'.format(parameter, dimension),

			'xaxis': {'title': parameter.title()},
            'yaxis': {'title': dimension.title()}
        }
    }
	return figure
# DATA ----------------------------------------


#variable "ocean" is a Dataframe used in this code

#loading ocean
ocean = pd.read_csv("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/psych/bfi.csv")
#general simplifying of ocean
ocean.drop(["Unnamed: 0"], axis = 1, inplace = True)
#low occurence of data for age lower than 16 and higher than 55, there are 10 or more participants for each age
ocean.drop(ocean.index[ocean['age'] <= 15].tolist(), inplace = True)
ocean.drop(ocean.index[ocean['age'] >= 56].tolist(), inplace = True)
ocean.dropna(axis = 0, how='any', thresh=None, subset=None, inplace = True)
#creating mean of individual questions
ocean['A'] = ocean[['A1', 'A2', 'A3', 'A4', 'A5']].mean(axis = 1)
ocean['C'] = ocean[['C1', 'C2', 'C3', 'C4', 'C5']].mean(axis = 1)
ocean['E'] = ocean[['E1', 'E2', 'E3', 'E4', 'E5']].mean(axis = 1)
ocean['N'] = ocean[['N1', 'N2', 'N3', 'N4', 'N5']].mean(axis = 1)
ocean['O'] = ocean[['O1', 'O2', 'O3', 'O4', 'O5']].mean(axis = 1)
#reorganization - cutting of unmeaned questions and resorting meaned ones
ocean.drop(['A1', 'A2', 'A3', 'A4', 'A5', 'C1', 'C2', 'C3', 'C4', 'C5', 'E1', 'E2', 'E3', 'E4', 'E5', 'N1', 'N2', 'N3', 'N4', 'N5', 'O1', 'O2', 'O3', 'O4', 'O5'], axis = 1, inplace = True)
ocean = ocean[['A', 'C', 'E', 'N', 'O', "age", "education", "gender"]].sort_values('age')
#removing values below scale
ocean = ocean[ocean['A'] > 1]
ocean = ocean[ocean['C'] > 1]
ocean = ocean[ocean['E'] > 1]
ocean = ocean[ocean['N'] > 1]
ocean = ocean[ocean['O'] > 1]
#removing decimals from 'education' column
ocean['education'] = ocean['education'].astype(int)
#final cut
ocean = ocean.reset_index(drop=True)




#meaner() creates means in dimensions according 
def meaner(dimension, parameter):

    start = 0
    iteration = 0
    mean = []
    
    if parameter == "a":
        end = ocean['age'].value_counts().sort_index().values.tolist()[0]
        step = ocean['age'].value_counts().sort_index().values.tolist()
    elif parameter == "e":
        end = ocean.sort_values("education")["education"].value_counts().sort_index().values.tolist()[0]
        step = ocean.sort_values("education")["education"].value_counts().sort_index().values.tolist()
    elif parameter == "g":
        end = ocean.sort_values("gender")["gender"].value_counts().sort_index().values.tolist()[0]
        step = ocean.sort_values("gender")["gender"].value_counts().sort_index().values.tolist()
    
    if dimension == "A":
        column = 0
    elif dimension == "C":
        column = 1
    elif dimension == "E":
        column = 2
    elif dimension == "N":
        column = 3
    else:
        column = 4

    for distance in step:    
    
        if iteration == 0:
            mean.append(ocean.iloc[start:end, column].mean())
            iteration += 1
            start += distance
    
        else:
            end += distance
            mean.append(ocean.iloc[start:end, column].mean())
            iteration += 1
            start += distance
            
    return [round(number, 2) for number in mean]

#end of meaner
	
	
lake_age = pd.DataFrame()
lake_age['age'] = ocean['age'].value_counts().sort_index().index.values.tolist()
lake_age['respondents'] = ocean['age'].value_counts().sort_index().values.tolist()
lake_age['A'] = meaner("A", "a")
lake_age['C'] = meaner("C", "a")
lake_age['E'] = meaner("E", "a")
lake_age['N'] = meaner("N", "a")
lake_age['O'] = meaner("O", "a")

lake_edu = pd.DataFrame()
lake_edu['education'] = ocean.sort_values("education")["education"].value_counts().sort_index().index.values.tolist()
lake_edu['respondents'] = ocean.sort_values("education")["education"].value_counts().sort_index().values.tolist()
lake_edu['A'] = meaner("A", "e")
lake_edu['C'] = meaner("C", "e")
lake_edu['E'] = meaner("E", "e")
lake_edu['N'] = meaner("N", "e")
lake_edu['O'] = meaner("O", "e")

lake_gen = pd.DataFrame()
lake_gen['gender'] = ocean.sort_values("gender")["gender"].value_counts().sort_index().index.values.tolist()
lake_gen['respondents'] = ocean.sort_values("gender")["gender"].value_counts().sort_index().values.tolist()
lake_gen['A'] = meaner("A", "g")
lake_gen['C'] = meaner("C", "g")
lake_gen['E'] = meaner("g", "g")
lake_gen['N'] = meaner("N", "g")
lake_gen['O'] = meaner("O", "g")




# ----------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.graph_objs import *


data = pd.read_csv('Data Vizualisation/chocolate.csv')
continent = pd.read_csv('Data Vizualisation/countryContinent.csv',encoding = "ISO-8859-1")
imp_exp=pd.read_csv('Data Vizualisation/UNdata_Export_20220301_151116452.csv')
coord=pd.read_csv('Data Vizualisation/country_points.csv',encoding = "ISO-8859-1")

data["company_location"] = data["company_location"].str.title()
data["country_of_bean_origin"] = data["country_of_bean_origin"].str.title()
data["company_location"].replace({'U.S.A': 'United States of America','U.K.':'United Kingdom of Great Britain and Northern Ireland','Dominican republic':'Dominican Republic','El salvador':'El Salvador','Vietnam':'Viet Nam','Venezuela':'Venezuela (Bolivarian Republic of)','South Korea':'Korea (Republic of)','New Zealand':'New Zealand','Russia':'Russian Federation','Taiwan':'Taiwan, Province of China','Sao Tome':'Sao Tome and Principe','Sao Tome & Principe':'Sao Tome and Principe','St. Lucia':'Saint Lucia','U.A.E.':'United Arab Emirates','St.Vincent-Grenadines':'Saint Vincent and the Grenadines','Bolivia':'Bolivia (Plurinational State of)'}, inplace=True)
data["country_of_bean_origin"].replace({'U.S.A': 'United States of America','U.K.':'United Kingdom of Great Britain and Northern Ireland','Dominican republic':'Dominican Republic','El salvador':'El Salvador','Vietnam':'Viet Nam','Venezuela':'Venezuela (Bolivarian Republic of)','South Korea':'Korea (Republic of)','New Zealand':'New Zealand','Russia':'Russian Federation','Taiwan':'Taiwan, Province of China','Sao Tome':'Sao Tome and Principe','Sao Tome & Principe':'Sao Tome and Principe','St. Lucia':'Saint Lucia','U.A.E.':'United Arab Emirates','St.Vincent-Grenadines':'Saint Vincent and the Grenadines','Bolivia':'Bolivia (Plurinational State of)','Burma':'Myanmar','Tanzania':'Tanzania, United Republic of','Trinidad':'Trinidad and Tobago','Dr Congo':'Congo (Democratic Republic of the)'}, inplace=True)

# removing Unnamed:0
data=data.iloc[:,1:]
teste=data.merge(continent[['country','continent','sub_region','code_2']].rename(columns={'continent':'company_continent','sub_region':'company_region','code_2':'company_code_2'}), left_on='company_location', right_on='country', how='left')
teste[teste['company_continent'].isna()]['company_location'].value_counts
teste=teste[teste['company_location']!= 'Scotland']
teste=teste.merge(continent[['country','continent','sub_region','code_2']].rename(columns={'continent':'bean_continent','sub_region':'bean_region','code_2':'bean_code_2'}), left_on='country_of_bean_origin', right_on='country', how='left')
teste[teste['bean_continent'].isna()]['country_of_bean_origin'].value_counts
teste=teste[teste['country_of_bean_origin']!= 'Blend']
data=teste


test_taste = data
test_taste.head()
test_taste['first_taste'].fillna(value = 0, inplace = True)
test_taste['second_taste'].fillna(value = 0, inplace = True)
test_taste['third_taste'].fillna(value = 0, inplace = True)
test_taste['fourth_taste'].fillna(value = 0, inplace = True)
#taste = lambda x: 1 if x.isna() == False else 0
taste = lambda x: 1 if x != 0 else x
test_taste['binFirst_taste'] = test_taste['first_taste'].apply(taste)
test_taste['binSecond_taste'] = test_taste['second_taste'].apply(taste)
test_taste['binThird_taste'] = test_taste['third_taste'].apply(taste)
test_taste['binFourth_taste'] = test_taste['fourth_taste'].apply(taste)
test_taste[test_taste['binThird_taste'] == 0].head()
test_taste['count_tastes'] = test_taste['binFirst_taste'] + test_taste['binSecond_taste'] + test_taste['binThird_taste'] + test_taste['binFourth_taste']

companies = list(data['company'].unique())


# The app itself

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.H4('Choose the companies you want to compare'),
        
        html.Div([
                      
            html.Div([
                html.Label('Company 1'),
                    dcc.Dropdown(
                                    id='drop_comp1_id',
                                    options=companies,
                                    value='5150',
                                    multi=False
                                ),
            ], className='box', style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'}),
            
            html.Div([
                html.Label('Company 2'),
                    dcc.Dropdown(
                                    id='drop_comp2_id',
                                    options=companies,
                                    value='A. Morin',
                                    multi=False
                                ),
            ], className='box', style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'})]),
                                
            
            
            html.Div([
                html.Div([
                    html.Label('Results', style={'font-size': 'medium'}),
                    html.Br(),
                    html.Br(),
 
                html.Div([ 
                    html.Div([
                        
                        html.Div([
                            html.Br(),
                            html.Label(id='title_map', style={'font-size':'medium'}), 
                            html.Br(),
                        ], style={'width': '70%'}),
                        html.Div([

                        ], style={'width': '5%'}),
                       
                    
                    dcc.Graph(id='radar'),

                ], className='box', style={'padding-bottom': '0px'}), 
                    ]),
                ], style={'width': '60%'}),           
            ], className='row')
])




@app.callback(
   
   Output('radar', 'figure'),
   
    [Input('drop_comp1_id', 'value'),
     Input('drop_comp2_id','value')] )

def update_radar(company1,company2):

    feat_radar = ['cocoa_percent', 'rating', 'counts_of_ingredients', 'count_tastes']

    radar = pd.DataFrame(round(test_taste.groupby(by = 'company')[feat_radar].mean(),2))
    radar['company_name'] = radar.index
    radar.insert(0, 'cocoa_level', round((5 * radar['cocoa_percent']) / 100, 2))
    radar.drop(columns = {'cocoa_percent'}, inplace = True)
    
    feat_radar = ['cocoa_level', 'rating', 'counts_of_ingredients', 'count_tastes']

    company1_list = []

    company1_df = pd.DataFrame(radar[radar['company_name'] == company1])
    for i in range(len(radar.columns)-1):
        company1_list.append(radar[radar['company_name'] == company1].iloc[0,i])

    company2_list = []

    company2_df = pd.DataFrame(radar[radar['company_name'] == company2])
    for i in range(len(radar.columns)-1):
        company2_list.append(radar[radar['company_name'] == company2].iloc[0,i])


    fig = go.Figure(data=go.Scatterpolar(
            r=company1_list,
            theta=['Level of Cocoa', 'Rating', 'Number of Ingredients', 'Number of Tastes'],
            fill='toself', 
            marker_color = 'rgb(205,102,29)',   
            opacity =1, 
            hoverinfo = "text" ,
            name = company1,
            text  = [company1_df.columns[i] + ' = ' + str(company1_df.iloc[0,i]) for i in range(len(company1_list))]
        ), layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'))
    fig.add_trace(go.Scatterpolar(
            r=company2_list,
            theta=['Level of Cocoa', 'Rating', 'Number of Ingredients', 'Number of Tastes'],
            fill='toself',
            marker_color = 'rgb(193,255,193)',
            hoverinfo = "text" ,
            name= company2,
            text  = [company2_df.columns[i] + ' = ' + str(company2_df.iloc[0,i]) for i in range(len(company2_list))]
            ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 5]
        )),
    showlegend=True
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
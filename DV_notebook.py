#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly 
import numpy as np
import plotly.figure_factory as ff
import scipy
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib.cm as cmx
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.offline import plot
import random
import dash_bootstrap_components as dbc
import urllib.request, json 
import dash_daq as daq

#pip install scipy
#!pip install Dash


# In[2]:


# Import data

data = pd.read_csv('chocolate.csv')
continent = pd.read_csv('countryContinent.csv',encoding = "ISO-8859-1")
imp_exp=pd.read_csv('UNdata_Export_20220301_151116452.csv')
coord = pd.read_csv('country_points.csv', encoding = "ISO-8859-1")


# In[3]:


imp_exp=imp_exp[imp_exp['Commodity']=='Cocoa beans, whole or broken, raw or roasted'][['Country or Area','Year','Commodity','Flow','Quantity','Trade (USD)']]


# In[4]:


# Prepare the data for the merge
data["company_location"] = data["company_location"].str.title()
data["country_of_bean_origin"] = data["country_of_bean_origin"].str.title()
data["company_location"].replace({'U.S.A': 'United States of America','U.K.':'United Kingdom of Great Britain and Northern Ireland','Dominican republic':'Dominican Republic','El salvador':'El Salvador','Vietnam':'Viet Nam','Venezuela':'Venezuela (Bolivarian Republic of)','South Korea':'Korea (Republic of)','New Zealand':'New Zealand','Russia':'Russian Federation','Taiwan':'Taiwan, Province of China','Sao Tome':'Sao Tome and Principe','Sao Tome & Principe':'Sao Tome and Principe','St. Lucia':'Saint Lucia','U.A.E.':'United Arab Emirates','St.Vincent-Grenadines':'Saint Vincent and the Grenadines','Bolivia':'Bolivia (Plurinational State of)'}, inplace=True)
data["country_of_bean_origin"].replace({'U.S.A': 'United States of America','U.K.':'United Kingdom of Great Britain and Northern Ireland','Dominican republic':'Dominican Republic','El salvador':'El Salvador','Vietnam':'Viet Nam','Venezuela':'Venezuela (Bolivarian Republic of)','South Korea':'Korea (Republic of)','New Zealand':'New Zealand','Russia':'Russian Federation','Taiwan':'Taiwan, Province of China','Sao Tome':'Sao Tome and Principe','Sao Tome & Principe':'Sao Tome and Principe','St. Lucia':'Saint Lucia','U.A.E.':'United Arab Emirates','St.Vincent-Grenadines':'Saint Vincent and the Grenadines','Bolivia':'Bolivia (Plurinational State of)','Burma':'Myanmar','Tanzania':'Tanzania, United Republic of','Trinidad':'Trinidad and Tobago','Dr Congo':'Congo (Democratic Republic of the)'}, inplace=True)


# In[5]:


# removing Unnamed:0
data=data.iloc[:,1:]


# In[6]:


teste=data.merge(continent[['country','continent','sub_region','code_2']].rename(columns={'continent':'company_continent','sub_region':'company_region','code_2':'company_code_2'}), left_on='company_location', right_on='country', how='left')


# In[7]:


teste[teste['company_continent'].isna()]['company_location'].value_counts


# In[8]:


teste=teste[teste['company_location']!= 'Scotland']


# In[9]:


teste=teste.merge(continent[['country','continent','sub_region','code_2']].rename(columns={'continent':'bean_continent','sub_region':'bean_region','code_2':'bean_code_2'}), left_on='country_of_bean_origin', right_on='country', how='left')


# In[10]:


teste[teste['bean_continent'].isna()]['country_of_bean_origin'].value_counts


# In[11]:


teste=teste[teste['country_of_bean_origin']!= 'Blend']


# In[12]:


data=teste


# In[13]:


data1=data.groupby(by=['company']).mean()


# In[14]:


imp_exp_regions = imp_exp.merge(continent[['country','continent','sub_region','code_2']].rename(columns={'sub_region':'region'}), left_on = 'Country or Area', right_on= 'country', how= 'left')


# ### TREEMAP
# 

# In[15]:


imp_exp_regions.loc[(imp_exp_regions['continent']=='nan') & (imp_exp_regions['Country or Area']!='nan')]


# In[16]:


imp_exp_regions['country'].isna().sum()


# In[17]:


imp_exp_regions['continent'].isna().sum()
#imp_exp_regions[imp_exp_regions['Quantity'].isna()==True]


# In[18]:


imp_exp_regions= imp_exp_regions[~(imp_exp_regions['Flow'] == 'Re-Export')]
imp_exp_regions= imp_exp_regions[~(imp_exp_regions['Flow'] == 'Re-Import')]


# In[19]:


imp_exp_regions["Quantity"]= imp_exp_regions["Quantity"].fillna(imp_exp_regions.groupby('Country or Area')['Quantity'].transform('mean'))

imp_exp_regions['Quantity'].astype(int)


# In[20]:


imp_exp_regions=imp_exp_regions[imp_exp_regions['Country or Area'].isnull()!= True] #removing nulls from Country or Area Column


# In[21]:


imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Wallis and Futuna Isds', 'continent'] = 'Oceania'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Wallis and Futuna Isds','region'] = 'Polynesia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Venezuela', 'continent'] = 'Americas'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Venezuela','region'] = 'Southern America'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'United Rep. of Tanzania', 'continent'] = 'Africa'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'United Rep. of Tanzania','region'] = 'Eastern Africa'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'United Rep. of Tanzania','country'] = 'Tanzania'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'United Kingdom', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'United Kingdom','region'] = 'Northern Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'USA', 'continent'] = 'Americas'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'USA','region'] = 'Northern America'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'USA','country'] = 'United States of America'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Turks and Caicos Isds', 'continent'] = 'Americas'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Turks and Caicos Isds','region'] = 'Central America'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'TFYR of Macedonia', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'TFYR of Macedonia','region'] = 'Southern Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'TFYR of Macedonia','country'] = 'Macedonia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Syria', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Syria','region'] = 'Western Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Solomon Isds', 'continent'] = 'Oceania'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Solomon Isds','region'] = 'Australia and New Zealand'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Serbia and Montenegro', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Serbia and Montenegro','region'] = 'Southern Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Rep. of Moldova', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Rep. of Moldova','region'] = 'Eastern Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Rep. of Moldova','country'] = 'Moldova'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Rep. of Korea', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Rep. of Korea','region'] = 'Eastern Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Rep. of Korea','country'] = 'South Korea'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Other Asia, nes', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Other Asia, nes','region'] = 'Other'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Neth. Antilles', 'continent'] = 'Americas'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Neth. Antilles','region'] = 'Caribbean'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Lao People\'s Dem. Rep.', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Lao People\'s Dem. Rep.','region'] = 'South-Eastern Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Lao People\'s Dem. Rep.','country'] = 'Laos'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Iran', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Iran','region'] = 'South-Western Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Fmr Fed. Rep. of Germany', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Fmr Fed. Rep. of Germany','region'] = 'Central Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Fmr Fed. Rep. of Germany','country'] = 'Germany'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Faeroe Isds', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Faeroe Isds', 'region'] = 'Northern Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'FS Micronesia', 'continent'] = 'Oceania'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'FS Micronesia', 'region'] = 'Micronesia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Czech Rep.', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Czech Rep.', 'region'] = 'Central Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Bosnia Herzegovina', 'continent'] = 'Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Bosnia Herzegovina', 'region'] = 'Southern Europe'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Central African Rep.', 'continent'] = 'Africa'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Central African Rep.', 'region'] = 'Middle Africa'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'China, Hong Kong SAR', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'China, Hong Kong SAR', 'region'] = 'Eastern Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'China, Macao SAR', 'continent'] = 'Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'China, Macao SAR', 'region'] = 'Eastern Asia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Cook Isds', 'continent'] = 'Oceania'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Cook Isds', 'region'] = 'Polynesia'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Dominican Rep.', 'continent'] = 'Americas'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Dominican Rep.', 'region'] = 'Caribbean'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Fmr Sudan', 'continent'] = 'Africa'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Fmr Sudan','region'] = 'Northern Africa'
imp_exp_regions.loc[imp_exp_regions['Country or Area'] == 'Fmr Sudan','country'] = 'Sudan'

imp_exp_regions= imp_exp_regions[~(imp_exp_regions['Country or Area'] == 'Belgium-Luxembourg')]

imp_exp_regions= imp_exp_regions[~(imp_exp_regions['Country or Area'] == 'EU-28')]
imp_exp_regions= imp_exp_regions[~(imp_exp_regions['Country or Area'] == 'So. African Customs Union')]
imp_exp_regions= imp_exp_regions[~(imp_exp_regions['Country or Area'] == 'China, Hong Kong SAR')]


# In[22]:


flows_df=imp_exp_regions.drop(columns=['country', 'code_2'])


# In[23]:


#convert data type and sort the data by Year
flows_df=flows_df.sort_values(by=['Year'])


# In[24]:


flows_df=flows_df.dropna(how='any')


# In[25]:


groupby_flows=flows_df.groupby(['Year','continent', 'region', 'Country or Area', 'Flow']).mean(['Trade (USD)','Quantity'])
groupby_flows.reset_index(inplace=True)
groupby_flows.head(3)


# In[26]:


groupby_flows=groupby_flows[groupby_flows['Year']!=1988]
groupby_flows=groupby_flows[groupby_flows['Year']!=1989]
groupby_flows=groupby_flows[groupby_flows['Year']!=1990]
#delete years until all continents have value for exports and imports

flows_df=flows_df[flows_df['Year']!=1988]
flows_df=flows_df[flows_df['Year']!=1989]
flows_df=flows_df[flows_df['Year']!=1990]


# In[27]:


africa_count= len(flows_df.groupby('continent')['Country or Area'].unique()[0])
americas_count= len(flows_df.groupby('continent')['Country or Area'].unique()[1])
asia_count= len(flows_df.groupby('continent')['Country or Area'].unique()[2])
europe_count= len(flows_df.groupby('continent')['Country or Area'].unique()[3])
oceania_count= len(flows_df.groupby('continent')['Country or Area'].unique()[4])

# print('Africa has: ' + str(africa_count) + ' countries')
# print('Americas has: ' + str(americas_count) + ' countries')
# print('Asia has: ' + str(asia_count) + ' countries')
# print('Europe has: ' + str(europe_count) + ' countries')
# print('Oceania has: ' + str(oceania_count) + ' countries')


# In[28]:


nr_countries = [['Africa', africa_count],
                ['Americas', americas_count], 
                ['Asia', asia_count],
                ['Europe', europe_count],
                ['Oceania', oceania_count]]

df_nr_countries = pd.DataFrame(nr_countries, columns = ['Continent', 'Nr of Countries'])
print(df_nr_countries)


# In[29]:


groupby_flows= pd.merge(df_nr_countries, groupby_flows, left_on='Continent', right_on='continent')
groupby_flows.drop(columns='continent', inplace=True)
groupby_flows.head(3)


# In[30]:


#NOT USED
# def scatter_flows(flow):
#     fig = px.scatter(groupby_flows[groupby_flows['Flow']==flow],
#                  x='Quantity',
#                  y='Trade (USD)',
#                  animation_frame='Year', 
#                  animation_group='Continent', 
#                  size='Nr of Countries', 
#                  color='Continent',
#                  hover_name='Continent',
#                  )
#     fig.update_layout(
#                     title=('Quantity of Cacao ' + str(flow) + 'ed vs Trade (USD) by Continents in 1988 - 2019'),
#                     xaxis=dict(title=('Quantity '+ str(flow) + 'ed')),
#                     yaxis=dict(title=(str(flow) + ' Trade (USD) of Cacao')),
#                     #paper_bgcolor='rgb(500, 500, 500)'#,
#                     #plot_bgcolor='rgb(243, 243, 243)'
#                     )
                    
#     fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 3000
#     return fig.show()


# In[31]:


# def tree_flows(flow, variable, year):
#     fig = px.treemap(groupby_flows[(groupby_flows['Flow']==flow) & (groupby_flows['Year']==year) ], 
#                      path=['Country or Area'],
#                      values=variable, color=variable, color_continuous_scale='sunset'
#                     )
            
#     return fig.show()


# In[32]:


#tree_flows(flow='Export', variable='Quantity', year=2010)


# In[33]:


tree_variables = [
                    {'label': 'Quantity', 'value': 'Quantity'},
                    {'label': 'Trade (USD)', 'value': 'Trade (USD)'}
                 ]

tree_flows_Dict = [
                    {'label': 'Export', 'value': 'Export'},
                    {'label': 'Import', 'value': 'Import'}
                 ]


# # ----- Helena
# 

# In[34]:



ingredients = [
    {'label': 'Has Sugar', 'value': 'have_sugar'},
    {'label': 'Has not Sugar', 'value': 'have_not_sugar'},
    {'label': 'Has Vanilla', 'value': 'have_vanila'},
    {'label': 'Has not Vanilla', 'value': 'have_not_vanila'},
    {'label': 'Has Salt', 'value': 'have_salt'},
    {'label': 'Has not Salt', 'value': 'have_not_salt'},
    {'label': 'Has Lecithin', 'value': 'have_lecithin'},
    {'label': 'Has not Lecithin', 'value': 'have_not_lecithin'}
]


# In[35]:


# @app.callback(
   
#    [Output("name_company_id", "children"),
#     Output("rating_id", "children"),
#     Output("country_id", "children"),
#     Output('graph1', 'figure')],
   
#     [Input('drop_id', 'value'),
#      Input('percent_id','value')] )

# def update_graph(drop_id,percent_id):
    
#     filtered=data
#     for each in drop_id:
#         filtered=filtered[filtered.isin([each]).any(1)] 
    
#     filtered = filtered[(filtered['cocoa_percent'] >= percent_id[0]) & (filtered['cocoa_percent'] <= percent_id[1])]

#     # maxi=np.max(filtered['rating'])
#     # filtered=filtered[filtered['rating']==maxi]
    
#     data_inter = dict(type='bar', x=filtered['company'], y=filtered['rating'])
   
#     layout_1 = dict(xaxis=dict(title='Companies'),
#                    yaxis=dict(title='Ratings'))
    
#     fig = go.Figure(data=data_inter, layout=layout_1)  

#     if filtered.empty:
#         name_company = 'No company was found'
#         rating = 'No rating was found'
#         country= 'No country was found'
        
#     else:
#         name_company=str(filtered.head(1)['company'].values[0])
#         rating=str(filtered.head(1)['rating'].values[0])
#         country=str(filtered.head(1)['company_location'].values[0])
    
#     return name_company ,  \
#            rating , \
#            country , \
#            fig

# if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)


# # ------- Filipa
# 

# ### Column count_tastes
# 

# In[36]:


test_taste = data


# In[37]:


test_taste['first_taste'].fillna(value = 0, inplace = True)
test_taste['second_taste'].fillna(value = 0, inplace = True)
test_taste['third_taste'].fillna(value = 0, inplace = True)
test_taste['fourth_taste'].fillna(value = 0, inplace = True)


# In[38]:


#taste = lambda x: 1 if x.isna() == False else 0
taste = lambda x: 1 if x != 0 else x


# In[39]:


test_taste['binFirst_taste'] = test_taste['first_taste'].apply(taste)
test_taste['binSecond_taste'] = test_taste['second_taste'].apply(taste)
test_taste['binThird_taste'] = test_taste['third_taste'].apply(taste)
test_taste['binFourth_taste'] = test_taste['fourth_taste'].apply(taste)


# In[41]:


test_taste['count_tastes'] = test_taste['binFirst_taste'] + test_taste['binSecond_taste'] + test_taste['binThird_taste'] + test_taste['binFourth_taste']


# ### Radar Plot
# 

# In[43]:


feat_radar = ['cocoa_percent', 'rating', 'counts_of_ingredients', 'count_tastes']


# In[44]:


radar = pd.DataFrame(round(test_taste.groupby(by = 'company')[feat_radar].mean(),2))
radar['company_name'] = radar.index
radar.insert(0, 'cocoa_level', round((5 * radar['cocoa_percent']) / 100, 2))
radar.drop(columns = {'cocoa_percent'}, inplace = True)


# In[45]:


feat_radar = ['cocoa_level', 'rating', 'counts_of_ingredients', 'count_tastes']


# In[46]:


company1 = '5150'
company2 = 'A. Morin'


# In[47]:


radar['company_name'].isin([company1, company2])


# In[48]:


company1_list = []

company1_df = pd.DataFrame(radar[radar['company_name'] == company1])
for i in range(len(radar.columns)-1):
    company1_list.append(radar[radar['company_name'] == company1].iloc[0,i])

company1_list


# In[49]:


company2_list = []

company2_df = pd.DataFrame(radar[radar['company_name'] == company2])
for i in range(len(radar.columns)-1):
    company2_list.append(radar[radar['company_name'] == company2].iloc[0,i])

company2_list


# In[50]:


feat_radar


# In[51]:



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

fig.show()


# In[52]:


companies = list(data['company'].unique())
#companies


# ### Routes Dataframe

# In[54]:


coord


# In[55]:


routes_bean = pd.DataFrame(data[['company', 'company_location', 'company_code_2', 'country_of_bean_origin', 'bean_code_2']])

routes_bean = routes_bean.merge(coord[['latitude', 'longitude', 'country']], left_on = 'company_code_2', right_on = 'country', how = 'left').rename(columns = {'latitude': 'lat_company', 'longitude' : 'long_company'})
routes_bean.drop(columns = {'country'}, inplace = True)
routes_bean = routes_bean.merge(coord[['latitude', 'longitude', 'country']], left_on = 'bean_code_2', right_on = 'country', how = 'left').rename(columns = {'latitude': 'lat_bean', 'longitude' : 'long_bean'})
routes_bean.drop(columns = {'country'}, inplace = True)

routes_bean['route'] = tuple(zip(routes_bean['bean_code_2'], routes_bean['company_code_2']))
count_routes = routes_bean.copy()
count_routes = count_routes.drop_duplicates(subset='route')
count_routes['count'] = routes_bean.groupby(['route']).size().values


# Pick the routes with most flights
count_routes = count_routes.loc[count_routes['count'] > np.quantile(count_routes['count'], q = 0.75)]
count_routes = count_routes.reset_index()

count_routes


# In[56]:


fig_routes = go.Figure()

fig_routes.add_trace(go.Scattergeo(
    locationmode = 'geojson-id',
    lon = count_routes['long_company'],
    lat = count_routes['lat_company'],
    hoverinfo = 'text',
    text = count_routes['company'],
    mode = 'markers',
    marker = dict(
                color = np.array(count_routes['count']),
                cmin = 9,
                cmax = 140,
                colorscale = 'brwnyl',
                colorbar=go.ColorBar(
                    title='Times of Routes'
                ),
                opacity = 0.2
            )
    ))

cmap = plt.cm.RdPu
color = cmx.ScalarMappable(cmap = cmap).to_rgba(count_routes['count'], bytes = True)
color = ['rgba(' + str(x[0]) + ', ' + str(x[1]) + ', ' + str(x[2]) + ', ' + str(x[3]) + ')' for x in color]

#maxcount_f = max(count_routes['count'])

#bean_paths = []
for i in range(len(count_routes)): #routes_bean
    fig_routes.add_trace(
        go.Scattergeo(
            locationmode = 'geojson-id',
            lon = [count_routes['long_bean'][i], count_routes['long_company'][i]],
            lat = [count_routes['lat_bean'][i], count_routes['lat_company'][i]],
            mode = 'lines',
            hoverinfo = 'text',
            text = '<b>Bean Origin: </b>' + str(count_routes['country_of_bean_origin'][i]) \
                    + '<br><b>Bean Destiny: </b>' + str(count_routes['company_location'][i]) \
                    + '<br><b>Times with this route: </b>' + str(count_routes['count'][i]),
            line = dict(
                width = 1,
                color = color[i]
                )
            )
        )

fig_routes.update_layout(
    title_text = 'Routes of Cocoa\'s bean',
    showlegend = False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    geo = dict(
        scope = 'world',
        projection_type = 'equirectangular',
        showland = True,
        showcountries = True,
        landcolor = 'rgba(68,68,68,255)',
        countrycolor = 'rgb(148,148,148)',
    ),
)

fig_routes.update_layout(height=400, margin={"r":40,"t":0,"l":40,"b":0})


# In[57]:



# # The app itself

# app = dash.Dash(__name__)

# app.layout = html.Div([
    
#     html.H4('Choose the companies you want to compare'),
        
#         html.Div([
                      
#             html.Div([
#                 html.Label('Company 1'),
#                     dcc.Dropdown(
#                                     id='drop_comp1_id',
#                                     options=companies,
#                                     value='5150',
#                                     multi=False
#                                 ),
#             ], className='box', style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'}),
            
#             html.Div([
#                 html.Label('Company 2'),
#                     dcc.Dropdown(
#                                     id='drop_comp2_id',
#                                     options=companies,
#                                     value='A. Morin',
#                                     multi=False
#                                 ),
#             ], className='box', style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'})]),
                                
            
            
#             html.Div([
#                 html.Div([
#                     html.Label('Results', style={'font-size': 'medium'}),
#                     html.Br(),
#                     html.Br(),
 
#                 html.Div([ 
#                     html.Div([
                        
#                         html.Div([
#                             html.Br(),
#                             html.Label(id='title_map', style={'font-size':'medium'}), 
#                             html.Br(),
#                         ], style={'width': '70%'}),
#                         html.Div([

#                         ], style={'width': '5%'}),
                       
                    
#                     dcc.Graph(id='radar'),

#                 ], className='box', style={'padding-bottom': '0px'}), 
#                     ]),
#                 ], style={'width': '60%'}),           
#             ], className='row')
# ])
    


# In[58]:


# @app.callback(
   
#    Output('radar', 'figure'),
   
#     [Input('drop_comp1_id', 'value'),
#      Input('drop_comp2_id','value')] )

# def update_radar(company1,company2):

#     feat_radar = ['cocoa_percent', 'rating', 'counts_of_ingredients', 'count_tastes']

#     radar = pd.DataFrame(round(test_taste.groupby(by = 'company')[feat_radar].mean(),2))
#     radar['company_name'] = radar.index
#     radar.insert(0, 'cocoa_level', round((5 * radar['cocoa_percent']) / 100, 2))
#     radar.drop(columns = {'cocoa_percent'}, inplace = True)
    
#     feat_radar = ['cocoa_level', 'rating', 'counts_of_ingredients', 'count_tastes']

#     company1_list = []

#     company1_df = pd.DataFrame(radar[radar['company_name'] == company1])
#     for i in range(len(radar.columns)-1):
#         company1_list.append(radar[radar['company_name'] == company1].iloc[0,i])

#     company2_list = []

#     company2_df = pd.DataFrame(radar[radar['company_name'] == company2])
#     for i in range(len(radar.columns)-1):
#         company2_list.append(radar[radar['company_name'] == company2].iloc[0,i])


#     fig = go.Figure(data=go.Scatterpolar(
#             r=company1_list,
#             theta=['Level of Cocoa', 'Rating', 'Number of Ingredients', 'Number of Tastes'],
#             fill='toself', 
#             marker_color = 'rgb(205,102,29)',   
#             opacity =1, 
#             hoverinfo = "text" ,
#             name = company1,
#             text  = [company1_df.columns[i] + ' = ' + str(company1_df.iloc[0,i]) for i in range(len(company1_list))]
#         ), layout = Layout(
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)'))
#     fig.add_trace(go.Scatterpolar(
#             r=company2_list,
#             theta=['Level of Cocoa', 'Rating', 'Number of Ingredients', 'Number of Tastes'],
#             fill='toself',
#             marker_color = 'rgb(193,255,193)',
#             hoverinfo = "text" ,
#             name= company2,
#             text  = [company2_df.columns[i] + ' = ' + str(company2_df.iloc[0,i]) for i in range(len(company2_list))]
#             ))

#     fig.update_layout(
#     polar=dict(
#         radialaxis=dict(
#         visible=True,
#         range=[0, 5]
#         )),
#     showlegend=True
#     )

#     return fig
#     # ----------------------------------------------------------------------

#     # if filtered.empty:
#     #     name_company = 'No company was found'
#     #     rating = 'No rating was found'
#     #     country= 'No country was found'
        
#     # else:
#     #     name_company=str(filtered.head(1)['company'].values[0])
#     #     rating=str(filtered.head(1)['rating'].values[0])
#     #     country=str(filtered.head(1)['company_location'].values[0])
    
#     # return name_company ,  \
#     #        rating , \
#     #        country , \
#     #        fig


# In[59]:


# if __name__ == '__main__':
#     app.run_server()


# MAP

# In[60]:


path_geo = ''

data_geo = dict()

with open(path_geo + 'world.geojson') as json_file:

    data_geo = json.load(json_file)
    

data_company=data.groupby(by=["company_location"]).agg({"rating":"mean","ref":"count"})

data_company.reset_index(inplace=True)

data_origin=data.groupby(by=['country_of_bean_origin']).agg({"rating":"mean","ref":"count"})

data_origin.reset_index(inplace=True)

data_company.rename(columns={'company_location': 'country'}, inplace=True)

data_origin.rename(columns={'country_of_bean_origin': 'country'}, inplace=True)



for feature in data_geo['features']:
    feature['id'] = feature['properties']['NAME']

i=0

pays=[]

while i<len(data_geo['features']):

    pays.append(data_geo['features'][i]['id'])

    i+=1


missing1=[]

for country in data_origin["country"].values:
    if country not in pays:
        missing1.append(country)

missing2=[]

for country in data_company["country"].values:

    if country not in pays:

        missing2.append(country)



data_origin["country"] = np.where(data_origin["country"] == "Venezuela (Bolivarian Republic of)", "Venezuela", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Tanzania, United Republic of", "Tanzania", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Bolivia (Plurinational State of)", "Bolivia", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Bolvia", "Bolivia", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "U.S.A.", "United States", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Taiwan, Province of China", "Taiwan", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Martinique", "France", data_origin["country"]) #colÃ³nia francesa

data_origin["country"] = np.where(data_origin["country"] == "Sulawesi", "Indonesia", data_origin["country"]) #parte da indonÃ©sia

data_origin["country"] = np.where(data_origin["country"] == "Principe", "SÃ£o TomÃ© and Principe", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Sao Tome and Principe", "SÃ£o TomÃ© and Principe", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Sumatra", "Indonesia", data_origin["country"]) #parte da indonÃ©sia

data_origin["country"] = np.where(data_origin["country"] == "Tobago", "Trinidad and Tobago", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Sao TomÃ© and Principe", "SÃ£o TomÃ© and Principe", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Congo (Democratic Republic of the)", "Dem. Rep. Congo", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Viet Nam", "Vietnam", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Ivory Coast", "CÃ´te d'Ivoire", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Solomon Islands", "Solomon Is.", data_origin["country"])

data_origin["country"] = np.where(data_origin["country"] == "Dominican Republic", "Dominican Rep.", data_origin["country"])



data_company["country"] = np.where(data_company["country"] == "United Kingdom of Great Britain and Northern Ireland", "United Kingdom", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Venezuela (Bolivarian Republic of)", "Venezuela", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Wales", "United Kingdom", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Bolivia (Plurinational State of)", "Bolivia", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Russian Federation", "Russia", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Martinique", "France", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Taiwan, Province of China", "Taiwan", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Korea (Republic of)", "South Korea", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Viet Nam", "Vietnam", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "United States of America", "United States", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Dominican Republic", "Dominican Rep.", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Sao Tome and Principe", "SÃ£o TomÃ© and Principe", data_company["country"])

data_company["country"] = np.where(data_company["country"] == "Czech Republic", "Czechia", data_company["country"])



data_company.drop(data_company[data_company["country"]=="Grenada"].index, inplace=True)

data_company.drop(data_company[data_company["country"]=="Saint Vincent and the Grenadines"].index, inplace=True)



data_origin.drop(data_origin[data_origin["country"]=="Samoa"].index, inplace=True)
data_origin.drop(data_origin[data_origin["country"]=="Grenada"].index, inplace=True)

data_origin.drop(data_origin[data_origin["country"]=="Saint Vincent and the Grenadines"].index, inplace=True)


# In[ ]:





# # -------------------APP------------------

# In[61]:


#!pip install dash_daq


# In[65]:


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div([
                                
                                html.H1('Diving into Chocolate',style={"margin-top": "0","font-weight": "bold","text-align": "center","font-family":'verdana'}),
                                html.H3('Taking a closer look into the Chocolate Industry',style={"margin-top": "0","font-weight": "bold","text-align": "center","font-family":'verdana'}),
                                ], id='title_id'),
                        
                        html.Br(),
                        html.Br(), 
                                          
                        html.Div([ 
                                #WORLD MAP
                                html.Div([
                                         html.Div([
                                                html.H3("Cocoa around the world", style={"margin-top": "0","font-weight": "bold","text-align": "center","font-family":'verdana'}),
                                                ]),
                                         
                                        html.Div([
                                               
                                                #FILTROS
                                                html.Div([ 
                                                        html.H4("Choose what you want to see in this map:"),
                                                        html.Div([
                                                                html.Div([
                                                                        dbc.RadioItems(
                                                                                id="country_radio",
                                                                                options=[dict(label="Bean origin", value="country_of_bean_origin"), dict(label="Company location", value="company_location")],
                                                                                className='radio',
                                                                                value="country_of_bean_origin",
                                                                                style={'display':'block'}
                                                                                ),
                                                                        ]),
                                                                html.Br(),
                                                                html.Div([
                                                                        dbc.RadioItems(
                                                                                id="number_radio",
                                                                                options=[dict(label="Ratings", value="rating"),dict(label="Frequency",value="ref")],
                                                                                value="rating",
                                                                                className='radio',
                                                                                style={'display':'block'}
                                                                                ),
                                                                        ]),
                                                                ], style = {'padding-right':'10px'}),
                                                                html.Br(),
                                                                html.Br(),
                                                                html.Div([
                                                                      html.P('In this map, you can see either the country where the cocoa beans are originally from or the nationality of the companies that produce the chocolates in the dataset, according to the average ratings of the chocolates or the number of chocolates they have.')  
                                                                ],style={"text-align": "justify"})
                                                                ],style={'width': '20%', 'padding-right':'10px'}) ,
                                        
                                                # VIS WORLD
                                                html.Div([ 
                                                        dcc.Graph(id="choroplethmapbox")
                                                        ],style={'width': '80%','padding-bottom':'15px','padding-top':'20px'}),
                                                
                                                ], id='world_view', style={'display': 'flex'}), 
                                           
                                ],className='box'),  
                                
                                #WORD CLOUD
                                html.Div([ 
                                          html.Div([
                                                html.H3("Where to get your favorite chocolate?"),
                                                ],className='title_vis'),
                                
                                        html.Div([ 
                                                
                                        #FILTROS
                                        html.Div([ 
                                                html.Div([ 
                                                        html.P('Here you have the chance to find the company which sells your dream chocolate according to its rating. If the names of the companies are colored, then they sell the chocolate with the highest review rank. The number of times the company takes place in the visualization, corresponds to the number of chocolates owned with the given filters. The words’ size corresponds to the ranking of the chocolate.')
                                                        ],style={"text-align": "justify"}),  
                                                html.Div([
                                                       html.P('<strong> Note: </strong> If there are company names overlapping in the visualization, you can zoom in a specific area.') 
                                                ],style={"font-size": '12px',"text-align": "justify"}),
                                                html.H4('Choose the ingredients you like a chocolate to have:'),
                                                html.Div([ 
                                                        
                                                        dcc.Dropdown(
                                                                id='drop_id',
                                                                options=ingredients,
                                                                value=['have_sugar','have_vanila'],
                                                                clearable=False,
                                                                #searchable=False, 
                                                                multi=True,style= {'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'} 
                                                                ),
                                                                        ], style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'}),
                                                html.Div([ 
                                                        html.Br(),
                                                        html.H4('Choose the desired Cocoa percentage range:'),
                                                        dcc.RangeSlider(
                                                                        id='percent_id',
                                                                        min=42,
                                                                        max=100,
                                                                        value=[50, 58],
                                                                        marks={'50': '50',
                                                                                '60': '60',
                                                                                '70': '70',
                                                                                '80': '80',
                                                                                '90': '90',
                                                                                '100': '100'},
                                                                        step=1,
                                                                        tooltip={"placement": "bottom", "always_visible": True},
                                                                        className='rc'
                                                                        )
                                                        ]) ,
                                                        
                                                 ],style={'width': '40%'}) ,
                                    
                                        # VIS WORD
                                                html.Div([
                                                        html.Div([ 
                                                                dcc.Graph(id='graph1'),
                                                        ]) ,
                                                html.Div([        
                                                        html.Div([
                                                        html.H4('Company', style={'font-weight':'normal'}),
                                                        html.H3(id="name_company_id")
                                                        ],className='box_info', style = {'height': '20%'}),
                                                        
                                                        html.Div([
                                                        html.H4('Rating', style={'font-weight':'normal'}),
                                                        html.H3(id="rating_id")
                                                        ],className='box_info', style = {'height': '20%'}),
                                
                                                        html.Div([
                                                        html.H4('Country', style={'font-weight':'normal'}),
                                                        html.H3(id="country_id"),
                                                        ],className='box_info', style = {'height': '20%'}),
                                                        
                                                        ],style={'display': 'flex','padding-left':'100px'}) ,
                                                ], style = {'width': '60%'})
                                                
                                                
                                        ],style={'display': 'flex'}),  
                                ], className='box', id='word_cloud'), 
                                
                                #RADAR
                                html.Div([
                                         
                                        html.Div([
                                                html.H3("Which company would you find better?"),
                                                ],className='title_vis'),
                                        
                                        html.Div([
                                                #FILTROS
                                                html.Div([
                                                        html.Div([ 
                                                          html.P('Compare two companies of your choice according to the number of ingredients of their chocolates, their rating, the number of tastes and the level of cocoa (from 1 to 5). All these variables are an average of the values in all the chocolates owned by the company')
                                                          ],style={"text-align": "justify"}),

                                                html.Div([ 
                                                        html.H4('Company 1'),
                                                        dcc.Dropdown(
                                                                id='drop_comp1_id',
                                                                options=companies,
                                                                value='5150',
                                                                multi=False
                                                                ),
                                                                ], style={'margin': '10px', 'padding-top':'15px', 'padding-bottom':'15px'}) ,
                                        
                                
                                                html.Div([ 
                        
                                                        html.H4('Company 2'),
                                                        dcc.Dropdown(
                                                                id='drop_comp2_id',
                                                                options=companies,
                                                                value='A. Morin',
                                                                multi=False
                                                                ),
                                                                ], style={'margin': '10px', 'padding-bottom':'15px'}) ,

                                                # html.Div([
                                                #           html.Img(src=app.get_asset_url('chocochoco.png'), style={'position': 'relative', 'width': '50%', 'top': '-20px'})
                                                # ])
                                                
                                                ],style={'width': '35%'}),
                                                
                                                # VIS RADAR
                                                html.Div([ 
                                                        dcc.Graph(id='radar')
                                                        ], style={'width': '65%','padding-bottom': '0px'}) ,

                                                 
                                                ], id='radar_view', style={'display': 'flex'}),

                                               
                                ],className='box'),
                                #---------------------
                                
                             # TREEMAP
                               html.Div([ 
                                        html.Div([
                                                html.H3("Exports vs Imports of Cocoa", style={"margin-top": "0","font-weight": "bold","text-align": "center","font-family":'verdana'}),
                                                ],className='title_vis'),
                                        
                                        #FILTROS
                                        html.Div([
                                                html.Div([
                                                        html.Br(),
                                                        html.P('Here you can have a simple overview of the main international traders of Cocoa in a year between 1991 to 2019. You can choose to look over Quantity traded or Trade in USD, between Imports or Exports and a specific year.')
                                                ], style={"text-align": "justify", 'width': '30%','padding-left':'75px'}), 
                                                    
                                                html.Div([ 
                                                        html.H4('What variable do you want to analyze?'),
                                                        dbc.RadioItems(
                                                                id='dropvartree_id', 
                                                                options=tree_variables, 
                                                                value='Quantity',
                                                                className='radio',
                                                                style={'display':'block'}
                                                                ),
                                                        ], style={'padding-bottom':'15px','width': '25%','padding-left': '120px'}),
                                                
                                                html.Div([                                                        
                                                        html.H4("Pick a Flow:"),
                                                        dbc.RadioItems(
                                                                id="radioflowtree_id",
                                                                options=tree_flows_Dict, 
                                                                value='Export',
                                                                className='radio',
                                                                style={'display':'block'}
                                                                ) ,
                                                        
                                                        ], style={'padding-bottom':'15px','width': '25%','padding-left': '120px'}),

                                                html.Div([
                                                          html.Img(src=app.get_asset_url('tree.png'), style={'position': 'relative', 'width': '70%'})
                                                ], style={'width': '20%'}),

                                        ],style={'width': '100%','display': 'flex','justify-content': 'center'}),
                                                
                                        # VIS TREEMAP
                
                                        html.Div([
                                                dcc.Graph(id='treemap_vis'),
                                                dcc.Slider(
                                                        groupby_flows['Year'].min(), 
                                                        groupby_flows['Year'].max(),
                                                        step=None,
                                                        value=groupby_flows['Year'].min(),
                                                        marks={str(year): str(year) for year in groupby_flows['Year'].unique()},
                                                        included=False,
                                                        id='treeyear_slider',
                                                        )
                                                ])
                                                
                                        ],className='box' ),
                               
                                ]),
                        
                        # Bean Routes
                        html.Div([
                                html.Div([
                                        html.H3("Bean Routes around the world", style={"margin-top": "0","font-weight": "bold","text-align": "center","font-family":'verdana'}),
                                        ],className='title_vis'),
                                
                                html.Div([
                                        html.Div([
                                                html.Br(),
                                                html.P('In this visualization you can see which are the main routes of cocoa\'s bean around the world. The origin of the bean is the country where it is produced and the destination is the country of the company that uses thoses beans. Only the routes around the 75% quantile were chosen to be present in this visualization'),
                                                html.Br(),
                                                html.Br(),
                                                html.Img(src=app.get_asset_url('Cocoa-Bean-PNG-Image.png'), style={'margin-left': 'auto','margin-right': 'auto','display': 'block', 'width': '70%'})
                                        ], style={"text-align": "justify", 'width': '25%','padding-left':'15px'}),

                                        # Visualization Routes
                                        html.Div([
                                                dcc.Graph(figure = fig_routes)
                                        ], style={"text-align": "justify", 'width': '75%'})
                                ], style = {'display': 'flex'})
                                
                                
                        ], className = 'box'),
                        html.Div([
                        html.Div([
                                html.H3('Authors:'),
                                html.P('Beatriz Vizoso | Filipa Alves | Helena Oliveira | Maria Almeida')
                                ],className='box'),
                        
                        html.Div([
                                html.H3('Sources:'),
                                dcc.Markdown("""\
                                        - Chocolate dataset:
                                                https://www.kaggle.com/datasets/rtatman/chocolate-bar-ratings
                                        
                                        - Cocoa Imports and Exports: 
                                                https://wits.worldbank.org/trade/comtrade/en/country/ALL/year/2019/tradeflow/Exports/partner/WLD/product/180100 """),
        
                                ], className='box'),
                        ],style={'display':'flex'})
                        
                ],style={'margin':'80px'})


# In[66]:



@app.callback(
   
   Output('radar', 'figure'),
   
    [Input('drop_comp1_id', 'value'),
     Input('drop_comp2_id','value')] )


def update_radar(drop_comp1_id,drop_comp2_id):
    company1 = drop_comp1_id
    company2 = drop_comp2_id
    
    feat_radar = ['cocoa_percent', 'rating', 'counts_of_ingredients', 'count_tastes']
    companies = list(data['company'].unique())
    
    radar = pd.DataFrame(round(test_taste.groupby(by = 'company')[feat_radar].mean(),2))
    radar['company_name'] = radar.index
    radar.insert(0, 'cocoa_level', round((5 * radar['cocoa_percent']) / 100, 2))
    radar.drop(columns = {'cocoa_percent'}, inplace = True)
    
    radar = radar.merge(test_taste[['company_location', 'company']], left_on='company_name', right_on='company', how='left')
    radar.drop(columns={'company'}, axis = 1, inplace = True)
    
    radar.drop_duplicates(inplace = True)

    radar['company_name'].isin([company1, company2])
    company1_list = []

    company1_df = pd.DataFrame(radar[radar['company_name'] == company1])
    for i in range(len(radar.columns)-2):
        company1_list.append(radar[radar['company_name'] == company1].iloc[0,i])

    
    company2_list = []

    company2_df = pd.DataFrame(radar[radar['company_name'] == company2])
    for i in range(len(radar.columns)-2):
        company2_list.append(radar[radar['company_name'] == company2].iloc[0,i])

    
    labels_radar = ['Level of Cocoa', 'Rating', 'Number of Ingredients', 'Number of Tastes']
    fig = go.Figure(data=go.Scatterpolar(
            r=company1_list,
            theta = labels_radar,
            fill='toself', 
            marker_color = 'rgb(128, 0, 32)',   
            opacity =1, 
            hoverinfo = "text" ,
            name = company1,
            text  = ['<b>' + str(company1) + '</b><br>' + labels_radar[i] + ' = ' + str(company1_df.iloc[0,i]) + '; <br>Country: ' + str(radar[radar['company_name'] == company1].iloc[0,5]) for i in range(len(company1_list))]
        ), layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'))
    fig.add_trace(go.Scatterpolar(
            r=company2_list,
            theta=['Level of Cocoa', 'Rating', 'Number of Ingredients', 'Number of Tastes'],
            fill='toself',
            marker_color = 'rgb(218, 160, 109)',
            hoverinfo = "text" ,
            name= company2,
            text = ['<b>' + str(company2) + '</b><br>' + labels_radar[i] + ' = ' + str(company2_df.iloc[0,i]) + '; <br>Country: ' + str(radar[radar['company_name'] == company2].iloc[0,5]) for i in range(len(company2_list))]
            ))

    fig.update_layout(
        title = {'text': str(company1) + ' vs. ' + str(company2),'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5]
            )),
        showlegend=True
    )
    return fig

@app.callback(
   
   [Output("name_company_id", "children"),
    Output("rating_id", "children"),
    Output("country_id", "children"),
    Output('graph1', 'figure')],
   
    [Input('drop_id', 'value'),
     Input('percent_id','value')] )

def update_graph(drop_id,percent_id):
    
    filtered=data
    
    for each in drop_id:
        filtered=filtered[filtered.isin([each]).any(1)] 
    
    filtered = filtered[(filtered['cocoa_percent'] >= percent_id[0]) & (filtered['cocoa_percent'] <= percent_id[1])]
    maxi=np.max(filtered['rating'])
   
    filtered['color_max'] = np.where((filtered['rating'] == maxi), 1, 0)
    filtered=filtered.sort_values(by=['color_max'], ascending=False)
 
    group_=filtered[filtered['rating']==maxi].groupby(by=['company'])['rating'].mean().sort_values(ascending=False)
    filtered=filtered.head(15)
    ratings = filtered.rating.to_list()
    countries=filtered.company_location.to_list()
    initial_weights=filtered.rating.to_list()
    words = filtered.company.to_list()

    w_max= max(initial_weights)
    w_min=min(initial_weights)
    upper=15
    lower=4
    
    if (w_max-w_min) ==0:
        weights=[upper for x in initial_weights] 
    else:
        weights=[lower+((x-w_min)*(upper-lower))/(w_max-w_min) for x in initial_weights]

    nr_companies=len(filtered[filtered['color_max']==1])
    colors = [px.colors.qualitative.Antique[2] for i in range(nr_companies)]
    colors.extend(px.colors.qualitative.Antique[0] for i in range(len(filtered)-nr_companies))
    
    
    if len(filtered)>1:
        group_=pd.DataFrame(filtered[filtered['rating']==maxi].groupby(by=['company'])['rating'].mean().sort_values(ascending=False))
        name_company=str(group_.index[0])
        rating=str(group_.head(1)['rating'].values[0])
        country=str(filtered[filtered['company']==name_company].company_location.values[0])
    
    elif filtered.empty:
        name_company = 'No company was found'
        rating = 'No rating was found'
        country= 'No country was found'
        
    else:
        name_company=str(filtered.head(1)['company'].values[0])
        rating=str(filtered.head(1)['rating'].values[0])
        country=str(filtered.head(1)['company_location'].values[0])
        
        
    data_inter = go.Scatter(x=random.choices(range(2000), k=len(filtered)),
                            y=random.choices(range(2000), k=len(filtered)),
                            mode='text',
                            text=words,
                            marker={'opacity': 0.3},
                            textfont={'size': weights, 'color': colors},
                            hovertext=['Rating: '+str(f)+'<br>Country: ' + str(p) for f, p in zip(ratings, countries)],
                            hoverinfo='text')
                                

    layout_1 = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
            'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}} )
    
    fig = go.Figure(data=[data_inter], layout=layout_1)

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title={'text':'Word Cloud <br><sup>Companies that sell the chocolate desired</sup>','y':0.9,
                      'x':0.5,'xanchor': 'center','yanchor': 'top'},title_font_size=25)
    
    return name_company ,             rating ,            country ,            fig

@app.callback(
    Output("choroplethmapbox", "figure"),
    [
        Input("country_radio", "value"),
        Input("number_radio", "value")
    ]
)

def make_choroplethmap(country_radio,number_radio):
    if country_radio == 'country_of_bean_origin':
        df = data_origin
        main_title1="Country of Bean Origin"
    elif country_radio == "company_location":
        df = data_company
        main_title1 = "Location of Company"

    if number_radio == "rating":
        legend_title="Ratings"
    elif number_radio == "ref":
        legend_title="Frequency"
    

    data_choroplethmap = dict(type='choroplethmapbox', 
                            geojson=data_geo,
                            locations=df["country"], 
                            #locationmode="country names",
                            z=df[number_radio],                         
                            colorscale='brwnyl',
                            colorbar=dict(title=legend_title),
                            )

    layout_choroplethmap = dict(mapbox=dict(style='white-bg',
                                layers=[dict(source=feature,
                                            below='traces',
                                            type='fill',
                                            fill=dict(outlinecolor='gray')
                                            ) for feature in data_geo['features']]
                                            ),
                                title=dict(text=main_title1,
                                        x=.5 # Title relative position according to the xaxis, range (0,1)
                                        )
                            )
    
    fig_choroplethmap = go.Figure(data=data_choroplethmap, layout=layout_choroplethmap)
    fig_choroplethmap.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    fig_choroplethmap.update_layout(height=400, margin={"r":0,"t":0,"l":20,"b":0})

    return fig_choroplethmap


@app.callback(
    Output("treemap_vis", "figure"), 
    
    [Input('dropvartree_id', 'value'),
    Input('radioflowtree_id','value'),
    Input('treeyear_slider','value')] 
    
    )

def update_treemap(selected_var='Quantity', selected_flow='Export', selected_year=1991):
    filtered_df= groupby_flows[(groupby_flows['Flow']==selected_flow) & (groupby_flows['Year']==selected_year)]
    fig = px.treemap(filtered_df, path=['Country or Area'],values=selected_var, color=selected_var, color_continuous_scale='brwnyl')
    #title=(str(selected_var) + ' of Cocoa ' + str(selected_flow) + 'ed by Country in ' + str(selected_year))) 
    
    fig.data[0].hovertemplate = '%{label}<br>%{value}'
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      title={'text':str(selected_var) + ' of Cocoa ' + str(selected_flow) + 'ed by Country in ' + str(selected_year),'y':0.95,'x':0.5,'xanchor': 'center','yanchor': 'top'})
   
    
    return fig

# @app.callback(
   
#    Output('routes_vis', 'figure')
# )





if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:





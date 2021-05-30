import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

app = dash.Dash('COVID-19 Statistic Dashboard',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport",
                     'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}
                ])
server = app.server
app.title = 'COVID-19 Statistic Dashboard'



#read dataset
read = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
# read = pd.read_csv('owid-covid-data.csv')
data = read.copy()
country = data.location.unique()    #list country

yesterday = date.today()-timedelta(days=1)
if data[data['date'] == str(yesterday)]['new_cases'].sum() == 0:
    yesterday2 = date.today() - timedelta(days=2)
    today_data = data[data['date'] == str(yesterday2)]
else:
    yesterday2 = date.today() - timedelta(days=1)
    today_data = data[data['date'] == str(yesterday2)]

today_data.dropna(subset=['continent'], inplace=True)

configg = {'displayModeBar': False}

#get region stats
asia = today_data[today_data['continent'] == 'Asia']
africa = today_data[today_data['continent'] == 'Africa']
europe = today_data[today_data['continent'] == 'Europe']
na = today_data[today_data['continent'] == 'North America']
sa = today_data[today_data['continent'] == 'South America']
oceania = today_data[today_data['continent'] == 'Oceania']

#region stats
bar_x = [oceania['total_cases'].sum(),
         africa['total_cases'].sum(),
         sa['total_cases'].sum(),
         na['total_cases'].sum(),
         europe['total_cases'].sum(),
         asia['total_cases'].sum(),
         ]
bar_y = ['Oceania', 'Africa', 'South America', 'North America', 'Europe', 'Asia']

#region stats
region_stats = px.bar(x=bar_x,
                      y=bar_y,
                      color=bar_y,
                      orientation='h')
region_stats.update_layout(title_text='Regional COVID-19 Total Cases',
                           legend_title='Region',
                           )
region_stats.update_yaxes(title_text='', fixedrange=True)
region_stats.update_xaxes(title_text='', fixedrange=True)

asia_data = data[data['continent'] == 'Asia'].groupby('date')['total_cases'].sum()
asia_stats = px.area(x=asia_data.index, y=asia_data)
asia_stats.update_layout(title_text='Asia')
asia_stats.update_yaxes(title_text='', fixedrange=True)
asia_stats.update_xaxes(title_text='', fixedrange=True)

eu_data = data[data['continent'] == 'Europe'].groupby('date')['total_cases'].sum()
eu_stats = px.area(x=eu_data.index, y=eu_data)
eu_stats.update_layout(title_text='Europe')
eu_stats.update_yaxes(title_text='', fixedrange=True)
eu_stats.update_xaxes(title_text='', fixedrange=True)

na_data = data[data['continent'] == 'North America'].groupby('date')['total_cases'].sum()
na_stats = px.area(x=na_data.index, y=na_data)
na_stats.update_layout(title_text='North America')
na_stats.update_yaxes(title_text='', fixedrange=True)
na_stats.update_xaxes(title_text='', fixedrange=True)

sa_data = data[data['continent'] == 'South America'].groupby('date')['total_cases'].sum()
sa_stats = px.area(x=sa_data.index, y=sa_data)
sa_stats.update_layout(title_text='South America')
sa_stats.update_yaxes(title_text='', fixedrange=True)
sa_stats.update_xaxes(title_text='', fixedrange=True)

afr_data = data[data['continent'] == 'Africa'].groupby('date')['total_cases'].sum()
afr_stats = px.area(x=afr_data.index, y=afr_data)
afr_stats.update_layout(title_text='Africa')
afr_stats.update_yaxes(title_text='', fixedrange=True)
afr_stats.update_xaxes(title_text='', fixedrange=True)

oce_data = data[data['continent'] == 'Oceania'].groupby('date')['total_cases'].sum()
oce_stats = px.area(x=oce_data.index, y=oce_data)
oce_stats.update_layout(title_text='Oceania')
oce_stats.update_yaxes(title_text='', fixedrange=True)
oce_stats.update_xaxes(title_text='', fixedrange=True)

#highest total cases by country
total_by_country = today_data.groupby('location')['total_cases'].sum()
country_total = total_by_country.sort_values(ascending=False)
highest_country_total = country_total.head(10)

highest_country_total_stats = px.bar(x=highest_country_total.sort_values(),
                                     y=highest_country_total.sort_values().index,
                                     orientation='h')
highest_country_total_stats.update_layout(title_text='Highest Number of Total Cases by Country'
                                          )
highest_country_total_stats.update_yaxes(title_text='', fixedrange=True)
highest_country_total_stats.update_xaxes(title_text='', fixedrange=True)


#highest total deaths by country
deaths_by_country = today_data.groupby('location')['total_deaths'].sum()
country_total_deaths = deaths_by_country.sort_values(ascending=False)
highest_deaths_country = country_total_deaths.head(10)

highest_country_total_deaths = px.bar(x=highest_deaths_country.sort_values(),
                                      y=highest_deaths_country.sort_values().index,
                                      orientation='h')
highest_country_total_deaths.update_layout(title_text='Highest Number of Total Deaths by Country'
                                          )
highest_country_total_deaths.update_yaxes(title_text='', fixedrange=True)
highest_country_total_deaths.update_xaxes(title_text='', fixedrange=True)


#highest single day cases by country
new_by_country = today_data[today_data['date'] == str(yesterday2)].sort_values(by=['new_cases'], ascending=False)
highest_new_by_country = new_by_country.head(10)
# print(top_new_by_country['location'], top_new_by_country['new_cases'])

highest_country_day_cases = px.bar(x=highest_new_by_country['new_cases'].sort_values(),
                                   y=highest_new_by_country['location'].sort_values(),
                                   orientation='h')
highest_country_day_cases.update_layout(title_text='Highest Number of Single Day Cases by Country'
                                          )
highest_country_day_cases.update_yaxes(title_text='', fixedrange=True)
highest_country_day_cases.update_xaxes(title_text='', fixedrange=True)

#highest single day deaths by country
deaths_by_country = today_data[today_data['date'] == str(yesterday2)].sort_values(by=['new_deaths'], ascending=False)
highest_deaths_by_country = deaths_by_country.head(10)
# print(top_new_by_country['location'], top_new_by_country['new_cases'])
highest_country_day_deaths = px.bar(x=highest_deaths_by_country['new_deaths'].sort_values(),
                                    y=highest_deaths_by_country['location'].sort_values(),
                                    orientation='h')
highest_country_day_deaths.update_layout(title_text='Highest Number of Single Day Deaths by Country'
                                          )
highest_country_day_deaths.update_yaxes(title_text='', fixedrange=True)
highest_country_day_deaths.update_xaxes(title_text='', fixedrange=True)



fig = go.Figure(data=go.Choropleth(locations=today_data['iso_code'],
                                   z=today_data['total_cases'],
                                   text=today_data['location'],
                                   colorscale='Blues',
                                   autocolorscale=False,
                                   reversescale=True,
                                   marker_line_color='darkgray',
                                   marker_line_width=0.5,
                                   colorbar_title='Total Cases',
                                   ))
fig.update_layout(
    title_text='Global COVID-19 Total Cases',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://ourworldindata.org/coronavirus">\
            Our World in Data</a>',
        showarrow = False
    )]
)


total_case = [
    dbc.CardBody(
        [
            html.H3(format(int(today_data['total_cases'].sum()), ","), className="card-title"),
            html.P(
                'Global Confirmed Total Cases as of ' + str(yesterday2),
                className="card-text",
            ),
        ]
    ),
]

today_new_case = [
    dbc.CardBody(
        [
            html.H3(format(int(today_data['new_cases'].sum()), ","), className="card-title"),
            html.P(
                'Global Confirmed New Cases for ' + str(yesterday2),
                className="card-text",
            ),
        ]
    ),
]

total_death = [
    dbc.CardBody(
        [
            html.H3(format(int(today_data['total_deaths'].sum()), ","), className="card-title"),
            html.P(
                'Global Confirmed Deaths as of ' + str(yesterday2),
                className="card-text",
            ),
        ]
    ),
]

app.layout = html.Div([
    html.H1('COVID-19 Statistics Dashboard'),
    html.Hr(),
    html.Div([
        dbc.Row([
            dbc.Col(dbc.Card(today_new_case, color="light")),
            dbc.Col(dbc.Card(total_case, color="primary", inverse=True)),
            dbc.Col(dbc.Card(total_death, color="danger", inverse=True)),
            ], className='mb-4'),
        ]),

    html.Div([
        html.Label('Metric'),
        dcc.Dropdown(
            id='metric',
            options=[
                {'label': 'New Cases', 'value': 'new_cases'},
                {'label': 'Total Cases', 'value': 'total_cases'},
                {'label': 'New Death', 'value': 'new_deaths'},
                {'label': 'Confirmed deaths', 'value': 'total_deaths'},
                {'label': 'Test', 'value': 'new_tests'},
                {'label': 'Total Test', 'value': 'total_tests'},
                {'label': 'Test per Case', 'value': 'tests_per_case'},
                {'label': 'Positive Rate', 'value': 'positive_rate'},
                {'label': 'People Vaccinated', 'value': 'people_vaccinated'},
                {'label': 'People Fully Vaccinated', 'value': 'people_fully_vaccinated'},
                {'label': 'New Vaccinations', 'value': 'new_vaccinations'},
            ],
            value=['new_cases'],
            multi=True
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Country'),
        dcc.Dropdown(
            id='negara',
            options=[
                {'label': x, 'value': x}
                for x in country
            ],
            value=['Indonesia'],
            multi=True
        ),
    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    dcc.Graph(id='grafik', config=configg),
    dcc.Graph(id='global-map', config=configg,
              figure=fig),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='highest-total-cases', figure=highest_country_total_stats,
                          config=configg)
            ]),
            dbc.Col([
                dcc.Graph(id='highest-total-deaths', figure=highest_country_total_deaths, config=configg)
            ])
        ]),
        dbc.Row([
            dbc.Col([
               dcc.Graph(id='highest-day-cases', figure=highest_country_day_cases, config=configg)
            ]),
            dbc.Col([
                dcc.Graph(id='highest-death-cases', figure=highest_country_day_deaths, config=configg)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='region', figure=region_stats, config=configg)
            ]),
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=asia_stats, config=configg)
            ]),
            dbc.Col([
                dcc.Graph(figure=eu_stats, config=configg)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=na_stats, config=configg)
            ]),
            dbc.Col([
                dcc.Graph(figure=sa_stats, config=configg)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=afr_stats, config=configg)
            ]),
            dbc.Col([
                dcc.Graph(figure=oce_stats, config=configg)
            ])
        ]),
        html.Hr(),
        dcc.Markdown('''
        Dataset Source: Our World in Data  
        Code by [M. Ilham Syaputra](https://www.linkedin.com/in/m-ilham-syaputra/)
        '''),
    ])

], style={'margin-top': '1%',
          'margin-bottom': '10%',
          'margin-left': '10%',
          'margin-right': '10%'})

@app.callback(
    Output('grafik', 'figure'),
    [Input('negara', 'value'),
     Input('metric', 'value')]
)
def update_graph(negara, metric):
    if negara:
        pernegara = data[data['location'].isin(negara)]
    else:
        pernegara = data[data['location'] == 'Indonesia']

    line_chart = px.line(pernegara,
                         x='date',
                         y=metric,
                         color='location',
                         labels={'location':'Country',
                                 'total_cases':'Total Cases',
                                 'date':'Date'},
                    )
    line_chart.update_yaxes(title_text='', fixedrange=True)
    line_chart.update_xaxes(title_text='', fixedrange=True)
    return line_chart




if __name__ == '__main__':
    app.run_server(debug=True)
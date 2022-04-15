from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pandas.core.frame import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#df = pd.read_csv('data/expenses_GG_2021.csv', sep=';', header=0)
my_palette_colors_bar_plot = ['#7FAFFF','#CC55AA','#CCCCFF']
my_palette_colors_pie_chart = ['rgb(8,48,107)', 'rgb(8,81,156)', 'rgb(33,113,181)', 'rgb(66,146,198)', 'rgb(107,174,214)', 'rgb(158,202,225)', 'rgb(198,219,239)', 'rgb(222,235,247)', 'rgb(247,251,255)', 'rgb(204,204,255)', 'rgb(229,204,255)']

val_height = 800
prop_size_table=50


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Hello Giulia!'),
    html.H2(children='This is the Dashboard of your expenses during ...'),
    dcc.Dropdown(
        ['2020','2021', '2022'], ('2022'),
        id='dropdown-year'),
    html.Br(),
    html.P(children='You can choose which category values to represent in the pie chart.'),
    html.P(children='Click on the category you want to make disappear and click again to make it reappear in the pie chart.'),
    html.P(children='Try it yourself!'),
    dcc.Graph(
        id='tot-exp-gg-2021-pie-chart'
        ),
    html.Label('Choose which years you would like to compare:'),
    dcc.Checklist(['2022', '2021', '2020'],
        ['2022'],
        id='checklist-year'),
    dcc.Graph(
        id='bar-plot-year'
        ),
    html.Div([], className='prova')
    ],
    style={
        'flex': 1#,    'margin':'0'
    })


@app.callback(    
    Output('tot-exp-gg-2021-pie-chart', 'figure'),
    Output('bar-plot-year', 'figure'),
    Input('dropdown-year', 'value'),
    Input('checklist-year', 'value'))
def update_figure(selected_year_pie_chart,selected_year_bar_plot):
    var_year_dropdown = selected_year_pie_chart
    name_file = 'data/expenses_GG_'+var_year_dropdown+'.csv'
    df_pie_chart = pd.read_csv(name_file,sep=';', header=0)

    fig_pie_chart = make_subplots(
        rows=1, 
        cols=2,
        column_widths=[0.3, 0.7],
        specs=[[{"type": "table"},{"type": "pie"}]])

    fig_pie_chart.add_trace(
        go.Table(
            header=dict(values=['Category','Total Expenses (€)'],
                        align='left',
                        height=val_height/prop_size_table*2,
                        font=dict(size=val_height/prop_size_table)),
            cells=dict(values=[df_pie_chart['Category'],df_pie_chart['Total Expenses']],
                       align='left',
                       height=val_height/prop_size_table*2,
                       font=dict(size=val_height/prop_size_table))),
        row=1, col=1)

    fig_pie_chart.add_trace(
        go.Pie(labels=df_pie_chart['Category'], 
               values=df_pie_chart['Total Expenses'], 
               textinfo='label+percent',
               textfont=dict(size=val_height/prop_size_table)
               ,marker_colors=my_palette_colors_pie_chart
               ),
               row=1, col=2
    )

    fig_pie_chart.update_layout(height = val_height,
                      paper_bgcolor='#F8F8FF',
                      autosize = True,
                      title_x=0.5)

    var_year = selected_year_bar_plot
    L = len(var_year)
    # print(var_year)
    columns_name = ['Total Expenses','Category','Year']
    df_bar_plot = pd.DataFrame(columns=columns_name)
    for i in range(L):
      name_file_i = 'data/expenses_GG_'+var_year[i]+'.csv'
      df_i = pd.read_csv(name_file_i,sep=';', header=0)
      df_i['Year'] = var_year[i]
      df_bar_plot=df_bar_plot.append(df_i)
    fig_bar_plot = px.bar(
        df_bar_plot, 
        x="Category", 
        y="Total Expenses", 
        color='Year',
        barmode='group',
        color_discrete_sequence = my_palette_colors_bar_plot
        )
    fig_bar_plot.update_layout(
        paper_bgcolor='#F8F8FF',
        autosize = True
        )
    return fig_pie_chart, fig_bar_plot

if __name__ == '__main__':
    app.run_server(debug=True)
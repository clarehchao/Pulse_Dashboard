from dash import callback, dcc, html, Output, Input,register_page
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import numpy as np
import plotly.express as px
from utils.Helpers import Read_Clean_Data, plot_horizontal_bar,sort_strings_with_numbers

register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LITERA],
    path="/Parents_Summary",
)

# read and clean PARENT DATA
fdir = '/Users/clarechao/code/python/Pulse_Dashboard/data'
fname_parents = f'{fdir}/Pulse_Parents_Survey_CChao.csv'
df_parents = Read_Clean_Data(fname_parents,grptype = 'parents')

# make sure to set up className and define style in css file
dropdown_menu1 = dbc.Row([
    dbc.Col([
        html.H3(
            "Select a State",
            className="subtitle-small",
        ),
        dcc.Dropdown(
            id='state-dropdown',
            options=df_parents['State'].dropna().unique().tolist() + ['All'],
            value='All',
            clearable=True,
            multi=False,
            placeholder="Select here",
            className="custom-dropdown",
        )
    ]),
    dbc.Col([
        html.H3(
            "Select an Age Range",
            className="subtitle-small",
        ),
        dcc.Dropdown(
            id='agegrp-dropdown',
            options=sort_strings_with_numbers(df_parents['Age'].dropna().unique().tolist()) + ['All'],
            value='All',
            clearable=True,
            multi=False,
            placeholder="Select here",
            className="custom-dropdown",
        )
    ])
])

dropdown_menu2 = dbc.Row([
    dbc.Col([
        html.H3(
            "Select a Gender",
            className="subtitle-small",
        ),
        dcc.Dropdown(
            id='gender-dropdown',
            options=df_parents['Gender'].dropna().unique().tolist() + ['All'],
            value='All',
            clearable=True,
            multi=False,
            placeholder="Select here",
            className="custom-dropdown",
        )
    ]),
    dbc.Col([
        html.H3(
            "Select a Marital Status",
            className="subtitle-small",
        ),
        dcc.Dropdown(
            id='maritalstatus-dropdown',
            options=df_parents['Marital Status'].dropna().unique().tolist() + ['All'],
            value='All',
            clearable=True,
            multi=False,
            placeholder="Select here",
            className="custom-dropdown",
        )
    ])
])

dropdown_menu3 = dbc.Row([
    dbc.Col([
        html.H3(
            "Select a Ethnicity",
            className="subtitle-small",
        ),
        dcc.Dropdown(
            id='ethnicity-dropdown',
            options=df_parents['Ethnicity'].dropna().unique().tolist() + ['All'],
            value='All',
            clearable=True,
            multi=False,
            placeholder="Select here",
            className="custom-dropdown",
        )
    ]),
    dbc.Col([
        html.H3(
            "Select a Number of Teens",
            className="subtitle-small",
        ),
        dcc.Dropdown(
            id='numofteens-dropdown',
            options=np.sort(df_parents['NumofTeens'].dropna().unique()).tolist() + ['All'],
            value='All',
            clearable=True,
            multi=False,
            placeholder="Select here",
            className="custom-dropdown",
        )
    ])
])

layout = dbc.Container([
    html.Div([
        html.H2(
            "Parent Survey Summary",  # title
            className="title",
        ),
        dropdown_menu1,
        # html.Br(),
        dropdown_menu2,
        # html.Br(),
        dropdown_menu3,
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id="sm-chart",
                    config={"displayModeBar": False},
                    className="chart-card",
                    style={"height": "400px"},
                ),
                width=6,
            ),
            dbc.Col(
                dcc.Graph(
                    id="app-feat-chart",
                    config={"displayModeBar": False},
                    className="chart-card",
                    style={"height": "400px"},
                ),
                width=6,
            )
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id="ai-comfort-chart",
                    config={"displayModeBar": False},
                    className="chart-card",
                    style={"height": "400px"},
                ),
                width=12
            )
        ])
        ], className="page-content"
    )
    ],
    fluid=True,
)

@callback(
    Output('sm-chart', 'figure'),
    Output('app-feat-chart', 'figure'),
    Output('ai-comfort-chart', 'figure'),
    Input('state-dropdown', "value"),
    Input('agegrp-dropdown', "value"),
    Input('gender-dropdown', "value"),
    Input('maritalstatus-dropdown', "value"),
    Input('ethnicity-dropdown', 'value'),
    Input('numofteens-dropdown', 'value'),
)
def plot_charts(state, agegrp, gender, marrysts, ethnicity, numofteens):
    if not state and agegrp and gender and marrysts and ethnicity and numofteens:
        raise PreventUpdate
    # filter out the right data first
    df_filter = df_parents.copy()

    if marrysts != 'All':
        df_filter = df_filter.query('`Marital Status` == @marrysts')
    if gender != 'All':
        df_filter = df_filter.query('Gender == @gender')
    if agegrp != 'All':
        df_filter = df_filter.query('Age == @agegrp')
    if ethnicity != 'All':
        df_filter = df_filter.query('Ethnicity == @ethnicity')

    if state != 'All':
        df_filter = df_filter.query('State == @state')
    if numofteens != 'All':
        df_filter = df_filter.query('NumofTeens == @numofteens')

    # social medial use
    color_map = {'% Total': '#07beb8', '100-Ptotal': '#fdfffc'}
    sm_chart,_ = plot_horizontal_bar(
        df_all = df_filter,
        col_prefix = 'PSM_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        title = 'Social Media',
        x_range = [0,1],
        color=color_map
    )

    # desired App features
    app_feat_chart,_ = plot_horizontal_bar(
        df_all=df_filter,
        col_prefix='AFeat_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        title='App Features that Parents Desired to Have',
        x_range=[0, 1],
        color=color_map
    )

    # AI use comfort level
    colorscale = [(0, '#f7f7ff'), (0.5, '#68d8d6'), (1, '#07beb8')]
    ai_comfort_df = df_filter.groupby('AI_Use_Comfort')['AI_Use_Comfort'].count().reset_index(name='Count')
    array = ai_comfort_df['Count'].to_numpy().reshape(1, -1)
    xx = [str(ss) for ss in ai_comfort_df['AI_Use_Comfort'].tolist()]
    search_str = ['1.0','5.0']
    if all(s in xx for s in search_str):
        print("all search string found in the list.")
        idx1 = xx.index('1.0')
        xx[idx1] = '1 (Not Comfortable)'
        idx5 = xx.index('5.0')
        xx[idx5] = '5 (Very Comfortable)'
        print(xx)
        print(array)
    else:
        print("None of the search strings found in the list.")
    yy = ['']
    ai_comfort_chart = px.imshow(
        array,
        x=xx,
        y=yy,
        color_continuous_scale=colorscale,
        zmax=35
    )
    # Update layout for better readability
    ai_comfort_chart.update_layout(
        title={
            'text': 'Comfort Level of Using AI',
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title='Comfort Level of Using AI',
        yaxis_title='',
        coloraxis_colorbar_title='Count'
    )

    return (sm_chart,
            app_feat_chart,
            ai_comfort_chart
            )

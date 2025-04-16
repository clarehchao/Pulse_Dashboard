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
    path="/Parents_Concern",
)

# read and clean PARENT DATA
fdir = '/Users/clarechao/code/python/Pulse_Dashboard/data'
fname_parents = f'{fdir}/Pulse_Parents_Survey_CChao.csv'
df_parents = Read_Clean_Data(fname_parents, grptype = 'parents')

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

layout = dbc.Container(
    [
        html.Div([
            html.H2(
                "Parent Concern & Advice Source",  # title
                className="title",
            ),
            # dropdown_menus,
            dropdown_menu1,
            # html.Br(),
            dropdown_menu2,
            # html.Br(),
            dropdown_menu3,
            html.Br(),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="concern-chart",
                        hoverData={'points': [{'customdata': ['PC_Communication']}]},
                        config={"displayModeBar": False},
                        className="chart-card",
                        style={"height": "600px"},
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        id="cross-filter-advsrc-chart",
                        config={"displayModeBar": False},
                        className="chart-card",
                        style={"height": "600px"},
                    ),
                    width=6,
                )
            ])
            ],
            className="page-content",
        )
    ],
    fluid=True,
)

@callback(
    Output('concern-chart', 'figure'),
    # Output('sm-chart', 'figure'),
    # Output('ai-comfort-chart', 'figure'),
    # Output('ai-reason-chart', 'figure'),
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

    # parent concern chart
    color_map = {'% Total': '#07beb8', '100-Ptotal': '#fdfffc'}
    concern_chart,_ = plot_horizontal_bar(
        df_all = df_filter,
        col_prefix = 'PC_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        title = 'What are Parents Concerned About?',
        x_range = [0,1],
        hovername='Category',
        customdata=['Category'],
        color=color_map
    )

    return concern_chart


@callback(
    Output('cross-filter-advsrc-chart', 'figure'),
    Input('concern-chart', 'hoverData'),
    Input('state-dropdown', "value"),
    Input('agegrp-dropdown', "value"),
    Input('gender-dropdown', "value"),
    Input('maritalstatus-dropdown', "value"),
    Input('ethnicity-dropdown', 'value'),
    Input('numofteens-dropdown', 'value'),
)
def update_ad(hoverData, state, agegrp, gender, marrysts, ethnicity, numofteens):
    if not hoverData and state and agegrp and gender and marrysts and ethnicity and numofteens:
        raise PreventUpdate

    pc_cat = hoverData["points"][0]["customdata"][0]
    df_filter = df_parents.query(f'`{pc_cat}` == 1')

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

    color_map = {'% Total': '#f25c54', '100-Ptotal': '#fdfffc'}
    advs_chart,_  = plot_horizontal_bar(
        df_all = df_filter,
        col_prefix = 'AdS_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        x_range=[0, 1],
        hovername='Category',
        customdata=['Category'],
        color=color_map,
        title = 'Where do Parents Seek Advice?'
    )

    return advs_chart
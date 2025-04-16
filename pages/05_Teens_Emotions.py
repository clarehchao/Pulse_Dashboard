from dash import callback, dcc, html, Output, Input,register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
from utils.Helpers import Read_Clean_Data, plot_horizontal_bar,get_ordinal

register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LITERA],
    path="/Teens_Emotions",
)

# read and clean TEENS DATA
fdir = '/Users/clarechao/code/python/Pulse_Dashboard/data'
fname_teens = f'{fdir}/Pulse_Teens_Survey_CChao.csv'
df_teens = Read_Clean_Data(fname_teens,grptype = 'teens')
grade_val = sorted([int(ss) for ss in df_teens['Grade'].dropna().unique().tolist()])
grade_label = [str(ss) + get_ordinal(ss) for ss in grade_val] + ['All']
grade_val = grade_val + ['All']
grade_menu_lst = [{'label': grade_label[ii], 'value': grade_val[ii]} for ii in range(len(grade_val))]


# layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.H2(
                    "Teens' Emotions",  # title
                    className="title",
                ),
                dbc.Row([
                    dbc.Col([
                        html.H3(
                            "Select a Grade",
                            className="subtitle-small",
                        ),
                        dcc.Dropdown(
                            id='grade-dropdown',
                            options=grade_menu_lst,
                            value='All',
                            clearable=True,
                            multi=False,
                            placeholder="Select here",
                            className="custom-dropdown",
                        )
                    ],
                    width = 4),
                ]),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="strong-emo-chart",
                                hoverData={'points': [{'customdata': ['StgEmo_Listen To Music']}]},
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "500px"},
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="reach-out-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "500px"},
                            ),
                            width=6,
                        )
                    ],
                )
            ],
            className="page-content",
        )
    ],
    fluid=True,
)

@callback(
        Output("strong-emo-chart", "figure"),
        Input("grade-dropdown", "value"),
)
def strong_emo_chart(grade):
    if not grade:
        raise PreventUpdate
    # filter out the right data first
    df_filter = df_teens.copy()

    if grade != 'All':
        df_filter = df_filter.query(f'Grade == "{grade}"')

    # ways Teens express strong emotion
    color_map = {'% Total': '#07beb8', '100-Ptotal': '#fdfffc'}
    stgemo_chart,_ = plot_horizontal_bar(
        df_all=df_filter,
        col_prefix='StgEmo_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        x_range=[0, 1],
        hovername='Category',
        customdata=['Category'],
        color=color_map,
        title='How Teens Handle Strong Emotions'
    )

    return stgemo_chart

@callback(
        Output('reach-out-chart', 'figure'),
        Input("strong-emo-chart", "hoverData"),
        Input("grade-dropdown", 'value'),
)
def update_reachout_chart(hoverData, grade):
    if not grade and hoverData:
        raise PreventUpdate

    df_filter = df_teens.copy()

    stremo_cat = hoverData["points"][0]["customdata"][0]
    df_filter = df_filter.query(f'`{stremo_cat}` == 1')

    if grade != 'All':
        df_filter = df_filter.query(f'Grade == "{grade}"')

    # ways Teens express strong emotion
    color_map = {'% Total': '#f25c54', '100-Ptotal': '#fdfffc'}
    reachout_chart,_ = plot_horizontal_bar(
        df_all=df_filter,
        col_prefix='RO_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        x_range=[0, 1],
        hovername='Category',
        customdata=['Category'],
        color=color_map,
        title='Who do Teens Reach Out to Talk to when Struggling?'
    )

    return reachout_chart
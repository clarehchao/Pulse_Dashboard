from dash import callback, dcc, html, Output, Input,register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
from utils.Helpers import Read_Clean_Data, plot_horizontal_bar,get_ordinal, create_card, circle_chart

register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LITERA],
    path="/Teens_SocialMedia",
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
                    "Teens' Social Media Use",  # title
                    className="title",
                ),
                dbc.Row([
                    dbc.Col([
                        html.H3(
                            "Select a Grade",
                            className="subtitle-small",
                        ),
                        dcc.Dropdown(
                            id='sm-grade-dropdown',
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
                            create_card(
                                h3_id='sm-stats',
                                h3_class='card-title-1',
                                h4_id = 'sm-stats-txt',
                                h4_class = 'card-body-1'
                            ),
                            width=6
                        ),
                        dbc.Col(
                            create_card(
                                h3_id='top-sm-title',
                                h3_class='card-title-2',
                                h4_id = 'top-sm-use',
                                h4_class = 'card-body-2'
                            ),
                            width=6
                        )
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="sm-use-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "500px"},
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="sm-impact-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "500px"},
                            ),
                            width=6,
                        )
                    ],
                ),
                html.Br(),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(
                            id="sm-reason-chart",
                            config={"displayModeBar": False},
                            className="chart-card",
                            style={"height": "500px"},
                        )
                    ),
                )
            ],
            className="page-content",
        )
    ],
    fluid=True,
)

@callback(
        [Output('sm-stats', "children"),
        Output('sm-stats-txt', "children"),
        Output('top-sm-title', "children"),
        Output('top-sm-use', "children"),
        Output("sm-use-chart", "figure"),
        Output("sm-impact-chart", "figure"),
        Output("sm-reason-chart", "figure"),
         ],
        [
        Input("sm-grade-dropdown", "value"),
        ]
)
def update_values(grade):
    if not grade:
        raise PreventUpdate
    # filter out the right data first
    df_filter = df_teens.copy()

    if grade != 'All':
        df_filter = df_filter.query(f'Grade == "{grade}"')

    sm_share_yes = (df_filter['ShareOnSM'] == 'Yes').mean() * 100
    sm_stats = '{:.1f}%'.format(sm_share_yes)
    sm_stats_txt = ' of Teens are comfortable talking about emotions on social media'
    top_sm_title = 'Top Social Media Use'

    # ways Teens express strong emotion
    color_map = {'% Total': '#07beb8', '100-Ptotal': '#fdfffc'}
    sm_use_chart, top_sm_use = plot_horizontal_bar(
        df_all=df_filter,
        col_prefix='SM_',
        xx=['% Total', '100-Ptotal'],
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        x_range=[0, 1],
        color=color_map,
        title='What Social Media do Teens Use?'
    )

    # social media impact bubble chart
    circle_colors = ['#ff9f1c', '#ffbf69', '#cbf3f0', '#2ec4b6']
    sm_impact_chart = circle_chart(
        df_all = df_filter,
        metric = 'SMImpact',
        colors = circle_colors,
        title = "Impact of Social Media on Teens")

    # social media impact reason
    color = ['#07beb8']
    sm_reason_chart,_ = plot_horizontal_bar(
        df_all=df_filter,
        col_prefix='SMR_',
        xx='% Total',
        yy='Category',
        x_title='% Total',
        txt_fmt='.0%',
        hovername='Category',
        customdata=['Category'],
        color=color,
        title='How/Why Teens are Impacted by Social Media'
    )

    return sm_stats, sm_stats_txt, top_sm_title, top_sm_use, sm_use_chart, sm_impact_chart, sm_reason_chart
    # return sm_stats, sm_stats_txt, top_sm_title, top_sm_use, sm_use_chart, sm_impact_chart,sm_reason_chart





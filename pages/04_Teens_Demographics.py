from dash import callback, dcc, html, Output, Input,register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from utils.Helpers import Read_Clean_Data,get_ordinal

register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LITERA],
    path="/Teens_Demographics",
)

# dataset
# read and clean TEENS DATA
fdir = '/Users/clarechao/code/python/Pulse_Dashboard/data'
fname_teens = f'{fdir}/Pulse_Teens_Survey_CChao.csv'
df_teens = Read_Clean_Data(fname_teens,grptype = 'teens')
N_teens = df_teens.shape[0]

# layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.H2(
                    "Teens Demographics",  # title
                    className="title",
                ),
                html.H3(
                    f'{N_teens} Survey Participants',  # title
                    className="subtitle-small",
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="teens-age-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="grade-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=6,
                        )
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="expemo-grade-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="guide-helpful-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=6
                        )
                    ]
                ),
            ],
            className="page-content",
        )
    ],
    fluid=True,
)

@callback(
    [
        Output("teens-age-chart", "figure"),
        Output("grade-chart", "figure"),
        Output("expemo-grade-chart", "figure"),
        Output("guide-helpful-chart", "figure"),
        Input("teens-age-chart", "id"),
        Input("grade-chart", "id"),
        Input("expemo-grade-chart", "id"),
    ],
)
def update_chart(age, grade, expemo):

    # age
    metric = 'Age'
    df_grp = df_teens.groupby(by=metric)[metric].count().reset_index(name='Counts')

    # Age
    teens_age_chart = px.bar(
        data_frame=df_grp,
        x=metric,
        y='Counts',
        text_auto='.0d',
        text='Counts'
    )

    teens_age_chart.update_traces(
        marker_color='#07beb8',
        textposition="auto",
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{x} y.o.</b><br>Value: %{y:,}<extra></extra>",
    )

    teens_age_chart.update_layout(
        title={
            'text': 'Age',
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=dict(showticklabels=False),
        margin=dict(l=15, r=15, t=60, b=15),
    )

    # Grade
    metric = 'Grade'
    df_grp = df_teens.groupby(by=metric)[metric].count().reset_index(name='Counts')

    # add the appropriate suffix to grade number for hoverdata (instead of using if-else statement in the hoverdatatemplate)
    df_grp['Grade_suffix'] = df_grp['Grade'].apply(lambda x: x + get_ordinal(x))
    cat_sorted = sorted([int(ss) for ss in df_grp['Grade'].tolist()])

    grade_chart = px.bar(
        data_frame=df_grp,
        x=metric,
        y='Counts',
        text_auto='.0d',
        text='Counts',
        title=metric,
        category_orders={'Grade': cat_sorted},
        custom_data=['Grade_suffix']
    )

    grade_chart.update_traces(
        marker_color='#07beb8',
        textposition="auto",
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{customdata[0]} Grade</b><br>Value: %{y:,}<extra></extra>",
    )

    grade_chart.update_layout(
        title={
            'text': metric,
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=dict(showticklabels=False),
        margin=dict(l=15, r=15, t=60, b=15),
    )

    # Grade vs Emotion Express Level
    colorscale = [(0, '#f7f7ff'), (0.5, '#68d8d6'), (1, '#07beb8')]
    grade_sorted = sorted([int(ss) for ss in df_teens['Grade'].dropna().unique().tolist()])
    expemo_sorted = sorted([int(ss) for ss in df_teens['ExpressEmoLevel'].dropna().unique().tolist()], reverse=True)
    exp_labels = expemo_sorted.copy()  # make sure to make a copy (else it will modify expemo_sorted as well)
    exp_labels[exp_labels.index(2)] = '2 (Bad at Expressing Emotion)'
    exp_labels[exp_labels.index(10)] = '10 (Great at Expressing Emotion)'
    exp_labels_dct = dict(zip(expemo_sorted, exp_labels))
    grade_expemo_chart = px.density_heatmap(
        data_frame=df_teens,
        x='Grade',
        y='ExpressEmoLevel',
        color_continuous_scale=colorscale,
        category_orders={'Grade': grade_sorted, 'ExpressEmoLevel': expemo_sorted}
    )

    # Update layout for better readability
    grade_expemo_chart.update_layout(
        title={
            'text': 'How Well Do Teens Express Emotions',
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title='Grade',
        yaxis_title='',
    )
    grade_expemo_chart.update_yaxes(labelalias=exp_labels_dct)


    # Talk to Guide and was it helpful?
    colorscale = [(0, '#f7f7ff'), (0.5, '#68d8d6'), (1, '#07beb8')]
    talkguide_sorted = sorted([int(ss) for ss in df_teens['TalkToGuideLevel'].dropna().unique().tolist()])
    helpful_sorted = sorted([int(ss) for ss in df_teens['GuideHelpfulLevel'].dropna().unique().tolist()], reverse=True)
    talkguide_labels = talkguide_sorted.copy()  # make sure to make a copy (else it will modify expemo_sorted as well)
    talkguide_labels[talkguide_labels.index(1)] = '1 (Never)'
    talkguide_labels[talkguide_labels.index(5)] = '5 (Very Often)'
    talkguide_labels_dct = dict(zip(talkguide_sorted, talkguide_labels))

    helpful_labels = helpful_sorted.copy()  # make sure to make a copy (else it will modify expemo_sorted as well)
    helpful_labels[helpful_labels.index(1)] = '1 (Not Helpful at all)'
    helpful_labels[helpful_labels.index(5)] = '5 (Extremely Helpful)'
    helpful_labels_dct = dict(zip(helpful_sorted, helpful_labels))

    guide_helpful_chart = px.density_heatmap(
        data_frame=df_teens,
        x='TalkToGuideLevel',
        y='GuideHelpfulLevel',
        color_continuous_scale=colorscale,
        category_orders={'TalkToGuideLevel': talkguide_sorted, 'GuideHelpfulLevel': helpful_sorted}
    )

    # Update layout for better readability
    guide_helpful_chart.update_layout(
        title={
            'text':'How Helpful are Caregivers\' Guidance to Teens',
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title='How often do Teens talk with Caregivers for Guidance',
        yaxis_title='',
        # coloraxis_colorbar_title='Count'
    )

    guide_helpful_chart.update_xaxes(labelalias=talkguide_labels_dct)
    guide_helpful_chart.update_yaxes(labelalias=helpful_labels_dct)

    return (
        teens_age_chart,
        grade_chart,
        grade_expemo_chart,
        guide_helpful_chart
    )
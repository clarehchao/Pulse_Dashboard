from dash import callback, dcc, html, Output, Input,register_page
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from utils.Helpers import state_name_to_code

register_page(
    __name__,
    suppress_callback_exceptions=True,
    # external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_stylesheets=[dbc.themes.LITERA],
    path="/Parents_Demographics",
)

# dataset
fdir = '/Users/clarechao/code/python/Pulse_Dashboard/data'
fname_parents = f'{fdir}/Pulse_Parents_Survey_CChao.csv'
df_parents = pd.read_csv(fname_parents)
N_parents = df_parents.shape[0]

# layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.H2(
                    "Parents Demographics",  # title
                    className="title",
                ),
                html.H3(
                    f'{N_parents} Survey Participants',  # title
                    className="subtitle-small",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="gender-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="age-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="marital-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=4,
                        ),
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="state-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="ethnicity-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="parents-teens-chart",
                                config={"displayModeBar": False},
                                className="chart-card",
                                style={"height": "360px"},
                            ),
                            width=4,
                        ),
                    ],
                ),
            ],
            className="page-content",
        )
    ],
    fluid=True,
)


# callback cards and graphs
@callback(
    [
        Output("gender-chart", "figure"),
        Output("age-chart", "figure"),
        Output("marital-chart", "figure"),
        Output("state-chart", "figure"),
        Output("ethnicity-chart", "figure"),
        Output("parents-teens-chart", "figure"),
        Input("gender-chart", "id"),
        Input("age-chart", "id"),
        Input("marital-chart", "id"),
        Input("state-chart", "id"),
        Input("ethnicity-chart", "id"),
        Input("parents-teens-chart", "id"),
    ],
)

def update_chart(gender, age, marital, state, ethnicity,parents_teens):

    # gender
    gender_chart = px.pie(
        df_parents,
        names='Gender',
        hole=0.4,
        color='Gender',
        color_discrete_map={
            'Woman': '#9ceaef',
            'Man': '#07beb8',
        },
    )

    gender_chart.update_traces(
        textposition="outside",
        textinfo="percent+label",
        texttemplate="<b>%{label}</b><br>%{percent:.1%}",
        rotation=180,
        showlegend=False,
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
    )

    gender_chart.update_layout(
        title={
            'text': "Gender",
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        yaxis=dict(showticklabels=False), margin=dict(l=15, r=15, t=60, b=15)
    )

    # age
    metric = 'Age'
    the_df = df_parents.groupby(by=metric)[metric].count().reset_index(name='Counts')

    age_chart = px.bar(
        data_frame=the_df,
        x=metric,
        y='Counts',
        text_auto='.0d',
        text='Counts'
    )

    age_chart.update_traces(
        marker_color='#07beb8',
        textposition="auto",
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{x}</b><br>Value: %{y:,}<extra></extra>",
    )

    age_chart.update_layout(
        title={
            'text':'Age',
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

    # marital status
    metric = 'Marital Status'
    the_df = df_parents.groupby(by=metric)[metric].count().reset_index(name='Count')
    cat_val = the_df[metric].sort_values(ascending=True).tolist()
    colors = ['#07beb8', '#3dccc7', '#68d8d6', '#9ceaef', '#c4fff9']
    color_map = dict(zip(cat_val, colors))
    marital_chart = px.pie(
        data_frame=the_df,
        values='Count',
        names='Marital Status',
        hole=0.4,
        color='Marital Status',
        color_discrete_map=color_map
    )

    marital_chart.update_traces(
        textposition="outside",
        textinfo="percent+label",
        texttemplate="<b>%{label}</b><br>%{percent:.1%}",
        rotation=180,
        showlegend=False,
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
    )

    marital_chart.update_layout(
        title={
            'text': "Marital Status",
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        yaxis=dict(showticklabels=False), margin=dict(l=15, r=15, t=60, b=15)
    )

    # state
    df_parents['State Code'] = df_parents['State'].apply(lambda ss: state_name_to_code(ss))
    metric = 'State Code'
    the_df = df_parents.groupby(by=metric)[metric].count().reset_index(name='Participants')
    colorscale = [(0, '#ffffff'), (0.5, '#68d8d6'), (1, '#07beb8')]

    state_chart = px.choropleth(
        the_df,
        locations='State Code',
        locationmode="USA-states",
        color='Participants',
        color_continuous_scale=colorscale,
        scope="usa",
        hover_data=['State Code'],
    )

    state_chart.update_traces(
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{customdata[0]}</b><br>Value: %{z:,}<extra></extra>",  # state name and user number
    )

    state_chart.update_layout(
        title={
            'text': "Survey Participants by State",
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        margin=dict(l=15, r=15, t=60, b=15),
    )

    # Ethnicity
    metric = 'Ethnicity'
    the_df = df_parents[metric].value_counts().sort_values(ascending=False).reset_index(name='Count')

    cat_order = the_df[metric].tolist()
    ethnicity_chart = px.bar(
        the_df,
        y=metric,
        x='Count',
        text_auto=".0d",
        text="Count",
        category_orders={metric: cat_order},
    )

    ethnicity_chart.update_traces(
        marker_color='#07beb8',
        textposition="auto",
        hoverlabel=dict(bgcolor='#fdfffc', font_size=12),
        hovertemplate="<b>%{y}</b><br>Value: %{x:,}<extra></extra>",
    )

    ethnicity_chart.update_layout(
        title={
            'text': 'Parent Ethnicity',
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title=None,
        yaxis_title=None,
        plot_bgcolor='#fdfffc',
        xaxis=dict(showticklabels=False),
        margin=dict(l=15, r=15, t=60, b=15),
    )

    # parents and teens info
    colorscale = [(0, '#f7f7ff'), (0.5, '#68d8d6'), (1, '#07beb8')]
    parent_teen_chart = px.density_heatmap(
        data_frame=df_parents,
        x='Parent_Involve',
        y='Teen_Share',
        color_continuous_scale=colorscale
    )

    # Update layout for better readability
    parent_teen_chart.update_layout(
        title={
            'text': 'Parent Involvement vs Teen Sharing',
            'font': {
                'family': "Inter, sans-serif",
                'size': 18,
                'weight': 'bold',
                'color': '#555b6e'
            },
        },
        xaxis_title='Level of Parent Involvement',
        yaxis_title='Level of Teens Share',
        coloraxis_colorbar_title='Count'
    )

    parent_teen_chart.update_traces(
        xbins=dict(start=0, end=5, size=1),
        ybins=dict(start=0, end=5, size=1)
    )

    return (
        gender_chart,
        age_chart,
        marital_chart,
        state_chart,
        ethnicity_chart,
        parent_teen_chart
    )
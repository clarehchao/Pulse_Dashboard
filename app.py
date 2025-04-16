import dash
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    title='Pulse Survey Dashboard',
    external_stylesheets=[dbc.themes.LITERA],
)


# sidebar
sidebar = html.Div(
    [
        dbc.Row(
            [html.Img(src="assets/logo/pulse.png", style={"height": "35px"})],
            className="sidebar-logo",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    "Parents Demographics", href="/Parents_Demographics", active="exact"
                ),
                dbc.NavLink(
                    "Parents' Concern",
                    href="/Parents_Concern",
                    active="exact",
                ),
                dbc.NavLink(
                    "Parents Survey Summary",
                    href="/Parents_Summary",
                    active="exact",
                ),
                dbc.NavLink(
                    "Teens Demographics",
                    href="/Teens_Demographics",
                    active="exact"
                ),
                dbc.NavLink(
                    "Teens' Emotions",
                    href="/Teens_Emotions",
                    active="exact"
                ),
                dbc.NavLink(
                    "Teens' Social Media Use",
                    href="/Teens_SocialMedia",
                    active="exact"
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div(
            [
                html.Span("Created by "),
                html.A(
                    "Clare Chao",
                    href="https://github.com/clarehchao/DataVisualization/tree/3efe9e79fddc77f8a811e8752c87076bf182356f/PulsePeers_Dashboard",
                    target="_blank",
                )
            ],
            className="subtitle-sidebar",
            style={"position": "absolute", "bottom": "10px", "width": "100%"},
        ),
    ],
    className="sidebar",
)


content = html.Div(
    className="page-content",
)

# layout
app.layout = html.Div(
    [
        dcc.Location(id="url", pathname='/Parents_Demographics'),
        sidebar,
        content,
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=False,port=8013)


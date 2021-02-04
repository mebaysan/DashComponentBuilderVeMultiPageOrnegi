from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
from components.builder import ComponentBuilder
from screens.bolgeler.get_screen import get_layout as bolgeler_layout
from screens.bolgeler.get_callbacks import get_callbacks as bolgeler_callbacks
from screens.kategoriler.get_screen import get_layout as kategoriler_layout
from screens.kategoriler.get_callbacks import get_callbacks as kategoriler_callbacks


DF = pd.read_csv('Sample_Market_Sales.csv', low_memory=False)
component_builder = ComponentBuilder()

app = Dash(__name__,
           external_stylesheets=component_builder.EXTERNAL_STYLESHEETS,
           meta_tags=component_builder.META_TAGS
           )
app = bolgeler_callbacks(app, DF)
app = kategoriler_callbacks(app, DF)

TABS = component_builder.get_tabs(
    tab_items={
        'Bölgeler': 'bolgeler',
        'Kategoriler': 'kategoriler'
    }
)

app.layout = html.Div(
    className=component_builder.LAYOUT_CLASSNAME,
    children=[
        dcc.Location(id="url"),
        TABS,
        html.Div(id="page-content")
    ]
)


@app.callback(
    Output("page-content", "children"),
    Input('url', 'pathname')
)
def render_tab_content(pathname):
    if pathname == '/kategoriler':
        return kategoriler_layout(DF)
    else:
        return bolgeler_layout(DF)
    return html.H1("Sekme seçiniz", className="title is-1"),


if __name__ == '__main__':
    app.run_server(debug=False)

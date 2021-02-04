import dash_html_components as html
import dash_core_components as dcc
from components.builder import ComponentBuilder


def get_layout(DF):
    component_builder = ComponentBuilder()
    layout = html.Div(children=[
        html.Section(className='section', children=[
            html.Div(className='box', children=[
                html.Div(className='columns', children=[
                    html.Div(className='column', id='bolge-ozet-kolon'),
                    html.Div(className='column', children=[
                        component_builder.get_dropdown_input(
                            DF, 'REGION', 'Bölge', 'bolge-bolge-dd'),
                        component_builder.get_dropdown_input(
                            DF, 'CITY', 'Şehir', 'bolge-city-dd'),
                        component_builder.get_dropdown_input(
                            DF, 'BRANCH', 'Şube', 'bolge-branch-dd'),
                        component_builder.get_dropdown_input(
                            DF, 'CATEGORY_NAME1', 'Kategori', 'bolge-cat1-dd'),
                        component_builder.get_button(
                            'Filtrele', 'bolge-filter-btn', is_in_column=True)
                    ]),
                ])
            ])
        ]),
        html.Section(className='section', children=[
            html.Div(className='box', children=[
                html.Div(className='columns', children=[
                    html.Div(className='column', children=[
                             dcc.Graph(id='bolge-chart')])
                ])
            ])
        ])
    ])

    return layout

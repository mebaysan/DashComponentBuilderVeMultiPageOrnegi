import dash_html_components as html
import dash_core_components as dcc
from components.builder import ComponentBuilder


def get_layout(DF):
    component_builder = ComponentBuilder()
    layout = html.Div(children=[
        html.Section(className='section', children=[
            html.Div(className='box', children=[
                html.Div(className='columns', children=[
                    html.Div(className='column is-one-third',
                             id='kategori-ozet-kolon'),
                    html.Div(className='column', children=[
                        html.Div(className='columns', children=[
                            component_builder.get_dropdown_input(
                                DF, 'CATEGORY_NAME1', 'Kategori 1', 'kategori-cat1-dd'),
                            component_builder.get_dropdown_input(
                                DF, 'CATEGORY_NAME2', 'Kategori 2', 'kategori-cat2-dd'),
                            component_builder.get_dropdown_input(
                                DF, 'CATEGORY_NAME3', 'Kategori 3', 'kategori-cat3-dd'),
                        ]),
                        component_builder.get_button(
                            'Filtrele', 'kategori-filter-btn')
                    ])
                ])
            ])
        ]),
        html.Section(className='section', children=[
            html.Div(className='box', children=[
                html.Div(className='columns', children=[
                    html.Div(className='column', children=[
                        dcc.Graph(id='kategori-chart')
                    ])
                ])
            ])
        ])
    ])
    return layout

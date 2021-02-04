import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from datetime import datetime


class ComponentBuilder(object):

    """
    Kullanmak için Dash uygulamasına Bulma CSS'i eklemelisiniz:
    dash.Dash(__name__,
                    external_stylesheets=[
                        "https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css"
                    ])
    """

    def __init__(self):
        self.PLOT_THEME = 'plotly_white'
        self.MAIN_COLOR_1 = '#006838'
        self.MAIN_COLOR_2 = '#b98e59'
        self.FIGURE_STYLE = {
            'figureTextSize': 12,
            'figureTitleTextSize': 14,
            'paper_bgcolor': '#fff',  # plotly grafik kağıdı arka plan rengi
            'plot_bgcolor': '#fff',  # plotly grafik arka plan rengi
            'header_fill_color': self.MAIN_COLOR_1,
            'header_font': '#FFFFFF',
            'cells_fill_color': self.MAIN_COLOR_2,
            'cells_font': '#F5F5F5',
            'color_discrete_sequence': px.colors.qualitative.Dark2
        },
        self.SPECIAL_INPUT_KEY = 'Hepsi'  # Verileri filtrelerken kendi ekranlarımız için bir özel key. Mesela 'Hepsi' olduğunda dropdownlara 'Hepsi' gelecek bu sayede bir değişkende bir değeri filtrelerken diğerlerinde hepsini seçebiliyoruz
        self.EXTERNAL_STYLESHEETS = [
            "https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css"]  # Dash instance oluştururken component builder'in style sheets'ini göndereceğiz
        self.META_TAGS = [
            {"name": "viewport",
             "content": "width=device-width, initial-scale=1"}
        ]  # Dash instance oluştururken component builder'in meta tags'lerini göndereceğiz
        self.LAYOUT_CLASSNAME = 'container'
        self.LABEL_FONT_SIZE = 14
        self.BUTTON_FONT_SIZE = 14
        self.INPUT_FONT_SIZE = 12
        self.HELP_TEXT_FONT_SIZE = 12
        self.TABLE_FONT_SIZE = 14

    def get_basic_table(self, headers, rows, is_in_column=True, column_class='', table_style={}):
        """
        headers -> liste olarak gelecek
        rows    ->  dict olarak gelecek
        """
        _table_style = {'fontSize': self.TABLE_FONT_SIZE}
        if table_style:
            for i in table_style:
                _table_style[i] = table_style[i]
        table_rows = []
        for row in rows:
            table_rows.append(
                html.Tr(children=[html.Td(f'{row}'), html.Td(f'{rows[row]}')]))
        table = html.Table(style=_table_style, className='table is-fullwidth is-hoverable',
                           children=[
                               html.Thead(children=[
                                   html.Tr(children=[
                                       html.Th(headers[0]),
                                       html.Th(headers[1]),
                                   ])
                               ]),
                               html.Tbody(children=table_rows)
                           ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[table])
            return column
        return table

    def get_tabs(self, tabs_style='is-fullwidth', tabs_id='tabs', tab_items={}):
        """
        Tab Style için:
        https://bulma.io/documentation/components/tabs/
        is-fullwidth
        is-right
        is-centered
        is-small
        is-medium
        is-large
        *********************************
        tabs_id -> sayesinde sayfa içeriğini değiştirebileceğiz
        *********************************
        tab_items -> {'Tab Title':'Tab-Link'}
        """
        _tab_items = []
        for tab_item in tab_items:
            _tab_items.append(
                html.Li(html.A(tab_item, href=tab_items[tab_item])))
        tabs = html.Div(className=f'tabs {tabs_style}', id=tabs_id, children=[
            html.Ul(children=_tab_items)
        ])
        return tabs

    def get_dropdown_input(self, data_frame, filter_column, label,  input_id, label_class='', label_style={}, special_key_in_option=True, default_value='self', dropdown_style={}, is_in_column=True, column_class='', help_text='', help_text_class='is-success'):
        """
        data_frame -> hangi veri seti
        filter_column -> dropdown'da hangi değişkene ait veriler gözükecek
        label -> input başlığı
        label_class -> label'a extra class gelecek mi
        label_style -> label'a özel stil verilecek mi
        input_id -> callback'leri çalıştırırken hangi id ile bu elementi yakalayacağız
        special_key_in_option -> self.SPECIAL_INPUT_KEY filtrede olacak mı (mesela Hepsi seçeneği)
        default_value -> dropdown'un başlangıç değeri (first veya self alabilir, first alırsa ilgili değişkenin tekil değerlerinin ilk elemanını başlangıç değeri olarak set eder), max alırsa ilgili kolonun en büyük değerini alır (Yıl vb için kullanıyoruz)
        dropdown_style -> dropdown'a css verilecekse dict olarak gelmeli
        is_in_column -> input column içine alınacak mı
        column_class -> column içine alınacaksa column style'ı ne olacak
        help_text -> input altında uyarı metni yazacak mı
        help_text_class -> help textin class'ı (Bulma'dan gelen is-primary vb)
        """
        if type(data_frame) == list:
            # liste içinde dict'ler -> [{'label':'Türk Lirası','value':'TL Cinsinden Proje Toplam'}]
            options = data_frame
            if default_value == 'first':
                value = options[0]['value']
            elif default_value == 'last':
                value = options[len(options) - 1]['value']
            else:
                value = self.SPECIAL_INPUT_KEY
        elif type(data_frame) == pd.DataFrame:  # DataFrame gelirse
            options = [{'label': _, 'value': _}
                       for _ in data_frame[f'{filter_column}'].unique()]
            options.insert(0, {'label': self.SPECIAL_INPUT_KEY,
                               'value': self.SPECIAL_INPUT_KEY}) if special_key_in_option else options
            if default_value == 'first':
                value = data_frame[filter_column].unique()[0]
            elif default_value == 'max':
                value = data_frame[filter_column].max()
            else:
                value = self.SPECIAL_INPUT_KEY
        else:
            return TypeError

        _label_style = {'fontSize': self.LABEL_FONT_SIZE}
        if label_style:
            for i in label_style:
                _label_style[i] = label_style[i]

        _dropdown_style = {'fontSize': self.INPUT_FONT_SIZE}
        if dropdown_style:
            for i in dropdown_style:
                _dropdown_style[i] = dropdown_style[i]

        field = html.Div(className='field', children=[
            html.Label(className=f'label {label_class}', style=_label_style, children=[
                f'{label}'
            ]),
            html.Div(className='control', children=[
                dcc.Dropdown(
                    id=input_id,
                    options=options,
                    value=value,
                    style=_dropdown_style
                ),
            ]),
            html.P(f'{help_text}', className=f'help {help_text_class}')
        ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[field])
            return column
        return field

    def get_input_text(self, label,  input_id, input_type, label_class='', label_style={}, default_value='self', input_style={}, input_class='is-primary', is_in_column=True, column_class='', help_text='', help_text_class='is-success', help_text_style={}):
        """
        label -> input başlığı
        label_class -> label'a extra class gelecek mi
        label_style -> label'a özel stil verilecek mi
        input_id -> callback'leri çalıştırırken hangi id ile bu elementi yakalayacağız
        input_type -> number, text, email vb (dcc'den bakabilirsiniz)
        input_style -> input'a extra css vermek ister misiniz
        input_class -> input'a extra class vermek ister misiniz
        default_value -> input'un başlangıç değeri
        is_in_column -> input column içine alınacak mı
        column_class -> column içine alınacaksa column style'ı ne olacak
        help_text -> input altında uyarı metni yazacak mı
        help_text_class -> help textin class'ı (Bulma'dan gelen is-primary vb)
        """
        if default_value == 'self':
            value = self.SPECIAL_INPUT_KEY
        else:
            value = default_value

        _label_style = {'fontSize': self.LABEL_FONT_SIZE}
        if label_style:
            for i in label_style:
                _label_style[i] = label_style[i]

        _input_style = {'fontSize': self.INPUT_FONT_SIZE}
        if input_style:
            for i in input_style:
                _input_style[i] = input_style[i]

        _help_text_style = {'fontSize': self.HELP_TEXT_FONT_SIZE}
        if help_text_style:
            for i in help_text_style:
                _help_text_style[i] = help_text_style[i]

        field = html.Div(className='field', children=[
            html.Label(className=f'label {label_class}', style=_label_style, children=[
                f'{label}'
            ]),
            html.Div(className='control', children=[
                dcc.Input(
                    id=input_id,
                    className=f'input {input_class}',
                    type=input_type,
                    value=value,
                    style=_input_style
                ),
            ]),
            html.P(f'{help_text}', className=f'help {help_text_class}',
                   style=_help_text_style)
        ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[field])
            return column
        return field

    def get_button(self, label, button_id, button_class='is-primary', button_style={}, default_nclick=1, is_in_column=False, column_class=''):
        """
        label -> buton üzerinde ne yazacak
        button_id -> butona nasıl erişilecek (callbackler için hangi id'den tetiklenecek vb.)
        button_class -> butona özel class verecek miyiz
        button_style -> butona özel stil vermek istersek
        default_nclick -> default kaç click ile initialize olacak
        is_in_column -> column içinde mi
        column_class -> column içindeyse column class'ı ne olacak (boş gelirse auto olarak alır)
        """

        _button_style = {'fontSize': self.BUTTON_FONT_SIZE}
        if button_style:
            for i in button_style:
                _button_style[i] = button_style[i]

        button = html.Div(className='buttons', children=[
            html.Button(
                f'{label}', className=f'button {button_class}', id=button_id, n_clicks=default_nclick, style=_button_style)
        ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[button])
            return column
        return button

    def get_graph_column(self, label, label_id, figure, figure_id, label_class='', column_class='', label_style={}, column_style={}):
        """
        label -> grafiğin başlığı (ya da üzerinde ne gözükecekse / bu sayede grafiğin oluşturulduğu svg içine title atmadan daha fazla yer kazanabileceğiz)
        label_id -> filtrelerden gelen verilere göre dinamik olarak title oluşturmak istersek çıktıyı Output() ile göndermek için bu id'e ihtiyacımız olacak
        figure -> column içindeki dcc.Graph() altında gözükecek olan figure
        figure_id -> figure'e output vermek için kullanacağımız id
        label_class -> labellara class vermek istersek kullanacağımız parametre
        column_class -> columnlara class vermek istersek kullanacağımız parametre 
        label_style -> label'a özel olarak stil vermek istersek
        column_style -> column'a özel olarak stil vermek istersek
        """
        column = html.Div(className=f'column {column_class}', style=column_style, children=[
            html.Label(f'{label}', id=label_id,
                       style=label_style,
                       className=f'label {label_class}'),
            dcc.Graph(id=figure_id, figure=figure)])

        return column

    def get_date_input(self, data_frame, filter_column, label,  input_id, label_class='', label_style={},  input_style={}, is_in_column=True, column_class='', help_text='', help_text_class='is-success'):
        """
        data_frame -> hangi veri seti
        filter_column -> dropdown'da hangi değişkene ait veriler gözükecek
        label -> input başlığı
        label_class -> label'a extra class gelecek mi
        label_style -> label'a özel stil verilecek mi
        input_id -> callback'leri çalıştırırken hangi id ile bu elementi yakalayacağız
        input_style -> input'a css verilecekse dict olarak gelmeli
        is_in_column -> input column içine alınacak mı
        column_class -> column içine alınacaksa column style'ı ne olacak
        help_text -> input altında uyarı metni yazacak mı
        help_text_class -> help textin class'ı (Bulma'dan gelen is-primary vb)
        """

        _label_style = {'fontSize': self.LABEL_FONT_SIZE}
        if label_style:
            for i in label_style:
                _label_style[i] = label_style[i]

        _input_style = {'fontSize': self.INPUT_FONT_SIZE}
        if input_style:
            for i in input_style:
                _input_style[i] = input_style[i]

        field = html.Div(className='field', children=[
            html.Label(className=f'label {label_class}',
                       style=_label_style, children=[f'{label}']),
            html.Div(className='control', children=[
                dcc.DatePickerRange(
                    style=_input_style,
                    id=input_id,
                    min_date_allowed=datetime(data_frame[filter_column].min().year, data_frame[filter_column].min().month,
                                              data_frame[filter_column].min().day),
                    max_date_allowed=datetime(data_frame[filter_column].max().year, data_frame[filter_column].max().month,
                                              data_frame[filter_column].max().day),
                    start_date=datetime(data_frame[filter_column].min().year, data_frame[filter_column].min().month,
                                        data_frame[filter_column].min().day),
                    end_date=datetime(data_frame[filter_column].max().year, data_frame[filter_column].max().month,
                                      data_frame[filter_column].max().day),
                    display_format='DD/MM/YYYY',
                )
            ]),
            html.P(f'{help_text}', className=f'help {help_text_class}')
        ])
        if is_in_column:
            column = html.Div(
                className=f'column {column_class}', children=[field])
            return column
        return field
from components.builder import ComponentBuilder
from dash.dependencies import Input, Output, State
import plotly.express as px


def data_filtrele(DF,  cat1, cat2, cat3):
    filtered_df = DF
    filtered_df = filtered_df[filtered_df['CATEGORY_NAME1']
                              == cat1] if cat1 != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['CATEGORY_NAME2']
                              == cat2] if cat2 != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['CATEGORY_NAME3']
                              == cat3] if cat3 != 'Hepsi' else filtered_df
    return filtered_df


def get_callbacks(app, DF):
    component_builder = ComponentBuilder()

    @app.callback(
        Output('kategori-ozet-kolon', 'children'),
        Input('kategori-filter-btn', 'n_clicks'),
        [
            State('kategori-cat1-dd', 'value'),
            State('kategori-cat2-dd', 'value'),
            State('kategori-cat3-dd', 'value')
        ]
    )
    def get_kategori_ozet_tablo(n_clicks, cat1, cat2, cat3):
        filtered_df = data_filtrele(DF, cat1, cat2, cat3)
        headers = ['Özet', '']
        rows = {
            'Toplam Satılan Ürün Adedi': '{:,}'.format(filtered_df['AMOUNT'].sum()),
            'Toplam Hasılat': '{:,} ₺'.format(filtered_df['PRICE'].sum()),
            'Toplam Tekil Ürün Adedi': '{:,}'.format(len(filtered_df['ITEMCODE'].unique())),
        }
        return component_builder.get_basic_table(headers, rows, False)

    @app.callback(
        Output('kategori-chart', 'figure'),
        Input('kategori-filter-btn', 'n_clicks'),
        [
            State('kategori-cat1-dd', 'value'),
            State('kategori-cat2-dd', 'value'),
            State('kategori-cat3-dd', 'value')
        ]
    )
    def get_kategori_chart(n_clicks, cat1, cat2, cat3):
        filtered_df = data_filtrele(DF, cat1, cat2, cat3)
        grouped_df = filtered_df.groupby(
            'CITY', as_index=False).sum().sort_values('PRICE', ascending=True)
        fig = px.bar(data_frame=grouped_df, x='PRICE', y='CITY',
                     title='Şehirlere Göre Toplam Hasılat')
        hovertemp = "<i>Şehir Adı: </i> %{y}<br>"
        hovertemp += "<i>Toplam Hasılat: </i> %{x:,} ₺"
        fig.update_layout(paper_bgcolor=component_builder.FIGURE_STYLE[0]['paper_bgcolor'],
                          plot_bgcolor=component_builder.FIGURE_STYLE[0]['plot_bgcolor'],
                          font_size=component_builder.FIGURE_STYLE[0]['figureTextSize'],
                          title_font_size=component_builder.FIGURE_STYLE[0]['figureTitleTextSize'],
                          )
        fig.update_traces(hovertemplate=hovertemp,
                          textposition='auto', texttemplate="%{x:,} ₺")
        return fig

    return app

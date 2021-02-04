from components.builder import ComponentBuilder
from dash.dependencies import Input, Output, State
import plotly.express as px


def data_filtrele(DF, bolge, sehir, sube, cat1):
    filtered_df = DF
    filtered_df = filtered_df[filtered_df['REGION']
                              == bolge] if bolge != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['CITY']
                              == sehir] if sehir != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['BRANCH']
                              == sube] if sube != 'Hepsi' else filtered_df
    filtered_df = filtered_df[filtered_df['CATEGORY_NAME1']
                              == cat1] if cat1 != 'Hepsi' else filtered_df
    return filtered_df


def get_callbacks(app, DF):
    component_builder = ComponentBuilder()

    @app.callback(
        Output('bolge-ozet-kolon', 'children'),
        Input('bolge-filter-btn', 'n_clicks'),
        [
            State('bolge-bolge-dd', 'value'),
            State('bolge-city-dd', 'value'),
            State('bolge-branch-dd', 'value'),
            State('bolge-cat1-dd', 'value')
        ]
    )
    def get_bolge_ozet_tablo(n_clicks, bolge, sehir, sube, cat1):
        filtered_df = data_filtrele(DF, bolge, sehir, sube, cat1)
        headers = ['Özet', '']
        rows = {
            'Toplam Satılan Ürün Adedi': '{:,}'.format(filtered_df['AMOUNT'].sum()),
            'Toplam Hasılat': '{:,} ₺'.format(filtered_df['PRICE'].sum()),
            'Toplam Tekil Ürün Adedi': '{:,}'.format(len(filtered_df['ITEMCODE'].unique())),
        }
        return component_builder.get_basic_table(headers, rows, False)

    @app.callback(
        Output('bolge-chart', 'figure'),
        Input('bolge-filter-btn', 'n_clicks'),
        [
            State('bolge-bolge-dd', 'value'),
            State('bolge-city-dd', 'value'),
            State('bolge-branch-dd', 'value'),
            State('bolge-cat1-dd', 'value')
        ]
    )
    def get_bolge_chart(n_clicks, bolge, sehir, sube, cat1):
        filtered_df = data_filtrele(DF, bolge, sehir, sube, 'Hepsi')
        grouped_df = filtered_df.groupby(
            'CATEGORY_NAME1', as_index=False).sum().sort_values('PRICE', ascending=True)
        fig = px.bar(data_frame=grouped_df, x='PRICE',
                     y='CATEGORY_NAME1', title='Kategorilere Göre Toplam Hasılat')
        hovertemp = "<i>Kategori Adı: </i> %{y}<br>"
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

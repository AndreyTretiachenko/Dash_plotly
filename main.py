from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from get_source import get_megafon_source


df = get_megafon_source("accounts", "", "")
df_history = get_megafon_source("history", "yesterday", "out")
df_group = df_history.groupby(['client'], as_index=False).agg('count').sort_values("UID", ascending=False)
print(df_group.columns)

app = Dash(__name__)

app.layout = html.Div(children=[

    html.H2(children='Дашборд основных показателей работы'),

    html.Div(children='''
        
    '''),

    dcc.Tabs(id="tabs", value="value-one", children=[
        dcc.Tab(label='Продажи', value='value-one'),
        dcc.Tab(label='Клиентская база', value='value-two'),
        dcc.Tab(label='Персонал', value='value-three')
    ]),
    html.Div(id="tab-content")

])

@app.callback(
    Output(component_id="tab-content", component_property="children"),
    Input(component_id="tabs", component_property="value")
)
def render_content(tab):
    if tab == "value-one":
        return dash_table.DataTable(df_history.to_dict('records'),
                         [{"name": i, "id": i} for i in df_history.columns], style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'},
                            filter_action="native")
    elif tab == "value-two":
        return dash_table.DataTable(df.to_dict('records'),
                         [{"name": i, "id": i} for i in df.columns], page_size=14, style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'},
                         filter_action="native",
                         sort_action="native",
                         sort_mode="multi"

                         )
    else:
        return dash_table.DataTable(df_group.to_dict('records'),
                         [{"name": i, "id": i} for i in df_group.columns], style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'},
                            page_size=20
                            )
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value')
)
def update_figure(selected_year):
    pass
    return

if __name__ == '__main__':
    app.run_server(debug=False)
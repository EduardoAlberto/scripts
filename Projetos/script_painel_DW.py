# from dash_html_components.Figure import Figure
# lib
import plotly.express as px
import pandas as pd
import dash
import plotly.graph_objs as go
# import dash_table
# import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as mssdb


# ------------------------------------------------------------------------------------------------
# acesso ao banco
engine = mssdb.create_engine("mssql+pyodbc://sa:Numsey@Password!@localhost,1433/olist?driver=ODBC+DRIVER+17+for+SQL+Server")
df = pd.read_sql('select * from vw_bi_cities',engine )
tabela = pd.read_sql('select * from vw_bi_product',engine )

# ------------------------------------------------------------------------------------------------
# grafico de mapas
fig = px.scatter_mapbox(df, lat="lat", lon="lng", hover_name="city", hover_data=["state", "price"],
                        color_discrete_sequence=["fuchsia"], zoom=15, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# ------------------------------------------------------------------------------------------------
# grafico barra

long_df = px.data.medals_long()

fig = px.bar(tabela, x="total", y=["max_price",'min_price'], title="Long-Form Input")
fig.show()
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph", figure=fig),
])

app.run_server(debug=True)


# fig = go.Figure(
#     data=[go.Bar(y=["max_price",'min_price'])],
#     layout_title_text="Native Plotly rendering in Dash"
# )

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Graph(id="graph", figure=fig),
# ])

# app.run_server(debug=True)



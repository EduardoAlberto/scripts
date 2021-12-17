# Griação de dados do twitter
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import cutecharts.charts as cute
from cutecharts.charts import Pie
from cutecharts.components import Page
from cutecharts.faker import Faker

df = pd.read_csv("/Users/eduardoaandrad/Dropbox/Desenv/Script/csv/kc_house_data.csv")

# Gerando gráficos para casas que tem 1 quarto
trace1 = go.Box(y = df.loc[df['bedrooms'] == 1, 'price'],
                name = 'Casas com 1 quarto',
                marker = {'color': '#f39c12'})
# Gráfico de caixa para casas com 2 quartos
trace2 = go.Box(y = df.loc[df['bedrooms'] == 2, 'price'],
                name = 'Casas com 2 quartos',
                marker = {'color': '#e67e22'})
# Gráfico de caixa para casas com 3 quartos
trace3 = go.Box(y = df.loc[df['bedrooms'] == 3, 'price'],
                name = 'Casas com 3 quartos',
                marker = {'color': '#d35400'})
# Gráfico para casas de quatro quartos
trace4 = go.Box(y = df.loc[df['bedrooms'] == 4, 'price'],
                name = 'Casas com 4 quartos',
                marker = {'color': '#e74c3c'})
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(title = 'Dispersão de preços para casas com diferentes quartos',
                   titlefont = {'family': 'Arial',
                                'size': 22,
                                'color': '#7f7f7f'},
                   xaxis = {'title': 'Número de quartos'},
                   yaxis = {'title': 'Preço'},
                   paper_bgcolor = 'rgb(243, 243, 243)',
                   plot_bgcolor = 'rgb(243, 243, 243)')
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)

# Teste com grafico de barra
trace1 = go.Bar(x = ['Banana', 'Maçã', 'Uva'],
                y = [10, 20, 30])
trace2 = go.Bar(x = ['Banana', 'Maçã', 'Uva'],
                y = [20, 30, 40])
data = [trace1, trace2]
py.iplot(data)

# cutecharts só funciona notebook
'''
import cutecharts.charts as ctc
df=pd.DataFrame({
 'x':['Sun.','Mon.','Tue.','Wed.','Thu.','Fri.','Sat.'],
 'y':[14,15,17,20,22.3,23.7,24.8],
 'z':[16,16.4,23.6,24.5,19.9,13.6,13.4]})

chart = ctc.Bar('Toronto Temperature',width='500px',height='400px')
chart.set_options(
 labels=list(df['x']),
 x_label='Days',
 y_label='Temperature (Celsius)' ,
 colors=['#1EAFAE' for i in range(len(df))]
 )
chart.add_series('This week',list(df['y']))
chart.render()
'''

def pie_base() -> Pie:
    chart = Pie("Pie-基本示例")
    chart.set_options(labels=Faker.choose())
    chart.add_series(Faker.values())
    return chart

    pie_base().render()
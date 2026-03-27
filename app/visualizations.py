import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def bar_ranking(df, x, y, title, color="#4A90D9"):
    fig = px.bar(df.sort_values(x), x=x, y=y, orientation="h", title=title, color_discrete_sequence=[color])
    fig.update_layout(height=400, margin=dict(t=50, b=20))
    return fig

def radar_comparison(df, city_col, metrics):
    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(r=[row[m] for m in metrics], theta=metrics, fill="toself", name=row[city_col]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, height=450)
    return fig

def scatter_salary_vs_col(df):
    fig = px.scatter(df, x="cost_of_living_index", y="net_salary", text="city_name",
                     size="relocation_score", color="region", title="Salario neto vs coste de vida")
    fig.update_traces(textposition="top center")
    fig.update_layout(height=500)
    return fig

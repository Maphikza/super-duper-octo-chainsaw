import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from pathlib import Path

path = Path(r"C:\Users\stapi\PycharmProjects\stocks\stock_data")
path_list = sorted(path.glob('*.csv'))

names = []
for i, csv_file in enumerate(path_list):
    names.append(f"stock_{i}")
    globals()[f'stock_{i}'] = pd.read_csv(path_list[i], parse_dates=["Date"])
    name = str(path_list[i]).split("\\")[-1].split('.')[0]

stock_names = []

for paths in path_list:
    stock_names.append(str(paths).split("\\")[-1].split(".c")[0])

data = pd.read_csv(path_list[0], parse_dates=["Date"])

fig = make_subplots(
    rows=6, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "scatter"}],
           [{"type": "scatter"}],
           [{"type": "scatter"}],
           [{"type": "scatter"}],
           [{"type": "scatter"}]]
)

fig.add_trace(
    go.Scatter(
        x=data.Date,
        y=data.Volume,
        mode="lines",
        name="Volume",
    ),
    row=6, col=1
)

fig.add_trace(
    go.Scatter(
        x=data.Date,
        y=data.Open,
        mode="lines",
        name="Opening Price",
    ),
    row=5, col=1
)

fig.add_trace(
    go.Scatter(
        x=data.Date,
        y=data.High,
        mode="lines",
        name="Opening Price",
    ),
    row=4, col=1
)

fig.add_trace(
    go.Scatter(
        x=data.Date,
        y=data.Low,
        mode="lines",
        name="Opening Price",
    ),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
        x=data.Date,
        y=data.Close,
        mode="lines",
        name="Closing Price",
    ),
    row=2, col=1
)

fig.add_trace(
    go.Table(
        header=dict(
            values=["Date", "Open", "High",
                    "Low", "Close", "Adj Close",
                    "Volume"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[data[k].tolist() for k in data.columns],
            align="left")
    ),
    row=1, col=1
)

fig.update_layout(
    height=900,
    showlegend=True,
    title_text="Opening and Closing", template="plotly_dark",
)
st.set_page_config(page_title="Stock Charts Test", layout="wide", initial_sidebar_state="auto")
st.header('Stock analysis')

# tab1 = st.tabs(["Stock A"])
#
with st.container():
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.sidebar:
    st.selectbox(label="Stocks", options=stock_names)


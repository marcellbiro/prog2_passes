#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 17:43:59 2020

@author: benceszabo
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dropbox
import pickle

token = "xtLHltG_SEAAAAAAAAAAEBOleqccikw3GSqRjWx1buy5EwuHwLKUshLDtUjzbhoq"
dbx = dropbox.Dropbox(token)

df = pickle.loads(dbx.files_download("/passes_df.pkl")[1].content)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


filt_df =  df.groupby(['Player','Date']).max().reset_index()

players_unique = filt_df["Player"].unique().tolist()

filt_box_df = df.groupby(['Player','Date']) ['Outcome'].value_counts().rename("counts").reset_index()

layout = go.Layout( height = 1000,
                   xaxis_showgrid=False,
                   yaxis_showgrid=False,
                   yaxis_autorange='reversed')


app.layout = html.Div(
    children=[
        html.H1(children=f"Longest passes dashboard"),
        dcc.Dropdown(
            id="Players",
            options=[{"label": e, "value": e} for e in ["all", *filt_df["Player"].unique()]],
         value="Lionel Messi"),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="Passes_scatter",
                            figure=px.scatter(
                                filt_df,
                                x="start_x",
                                y="start_y",
                                #color="team",
                                hover_data=["home_team"],
                            ),
                        )
                    ],
                    className="six columns",
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="Passes_box",
                            figure=px.bar(
                                filt_box_df,
                                x="Date",
                                y="counts",
                                color="Outcome",
                                barmode="group",
                            ),
                        )
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
    ]
)

@app.callback(
    dash.dependencies.Output("Passes_scatter", "figure"),
    [dash.dependencies.Input("Players", "value")],
)

def update_output(value):

    if (value is None) or (value == "all"):
        filt2_df = filt_df
    else:
        filt2_df = filt_df.loc[lambda df: df["Player"] == value]

    return px.scatter(filt2_df, x="start_x", y="start_y",hover_data=["home_team"])

@app.callback(
    dash.dependencies.Output("Passes_box", "figure"),
    [dash.dependencies.Input("Players", "value")],
)

def update_boxplot(value):

    if (value is None) or (value == "all"):
        filt3_df = filt_df
    else:
        filt3_df = filt_box_df.loc[lambda df: df["Player"] == value]

    return px.bar(filt3_df,x="Date",y="counts",color="Outcome",barmode="group")



server = app.server

if __name__ == '__main__':
  
    app.run_server(debug=True)
    

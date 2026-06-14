from pathlib import Path

import pandas as pd

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# LOAD DATA
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "morbid_metal_tagged_reviews.csv"

df = pd.read_csv(DATA_PATH)

# ==================================================
# TOPICS
# ==================================================

TOPICS = [
    "Combat",
    "Character_Switching",
    "Visuals",
    "Bosses",
    "Performance",
    "Content_Quantity",
    "Build_Variety",
    "Enemy_Variety",
    "Replayability",
    "Level_Design",
    "Bugs",
    "Difficulty"
]

# ==================================================
# KPI METRICS
# ==================================================

total_reviews = len(df)

positive_reviews = len(
    df[df["recommended"] == True]
)

negative_reviews = len(
    df[df["recommended"] == False]
)

recommendation_rate = round(
    positive_reviews / total_reviews * 100,
    1
)

# ==================================================
# SUMMARY TABLE
# ==================================================

positive = df[df["recommended"] == True]
negative = df[df["recommended"] == False]

summary = []

for topic in TOPICS:

    total_mentions = int(df[topic].sum())

    positive_mentions = int(
        positive[topic].sum()
    )

    negative_mentions = int(
        negative[topic].sum()
    )

    summary.append({

        "Topic": topic,

        "Total_Mentions": total_mentions,

        "Positive_Mentions": positive_mentions,

        "Negative_Mentions": negative_mentions,

        "Mention_Rate_%": round(
            total_mentions / total_reviews * 100,
            2
        ),

        "Positive_Rate_%": round(
            positive_mentions / total_mentions * 100,
            2
        ) if total_mentions else 0,

        "Negative_Rate_%": round(
            negative_mentions / total_mentions * 100,
            2
        ) if total_mentions else 0,

        "Net_Sentiment": (
            positive_mentions - negative_mentions
        )
    })

summary_df = pd.DataFrame(summary)

summary_df = summary_df.sort_values(
    by="Total_Mentions",
    ascending=False
)

# ==================================================
# CHART 1
# ==================================================

mention_fig = px.bar(
    summary_df,
    x="Topic",
    y="Mention_Rate_%",
    text="Mention_Rate_%",
    title="Most Discussed Topics"
)

mention_fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

mention_fig.update_layout(
    height=500
)

# ==================================================
# CHART 2
# ==================================================

sentiment_fig = go.Figure()

sentiment_fig.add_bar(
    name="Positive",
    x=summary_df["Topic"],
    y=summary_df["Positive_Mentions"]
)

sentiment_fig.add_bar(
    name="Negative",
    x=summary_df["Topic"],
    y=summary_df["Negative_Mentions"]
)

sentiment_fig.update_layout(
    title="Positive vs Negative Feedback by Topic",
    barmode="group",
    height=500
)

# ==================================================
# CHART 3
# ==================================================

net_fig = px.bar(
    summary_df.sort_values(
        "Net_Sentiment",
        ascending=False
    ),
    x="Topic",
    y="Net_Sentiment",
    text="Net_Sentiment",
    title="Net Sentiment by Topic"
)

net_fig.update_traces(
    textposition="outside"
)

net_fig.update_layout(
    height=500
)

mention_fig.update_layout(
    height=500
)

sentiment_fig.update_layout(
    height=500
)

strengths_df = (
    summary_df[
        summary_df["Total_Mentions"] >= 10
    ]
    .sort_values(
        "Positive_Rate_%",
        ascending=False
    )
    .head(5)
)

concerns_df = summary_df.sort_values(
    "Negative_Mentions",
    ascending=False
).head(5)

most_discussed = summary_df.iloc[0]["Topic"]

table_df = summary_df[
    [
        "Topic",
        "Total_Mentions",
        "Positive_Mentions",
        "Negative_Mentions",
        "Positive_Rate_%"
    ]
]

# ==================================================
# KEY FINDINGS
# ==================================================

top_topic = summary_df.iloc[0]

# ==================================================
# DASH APP
# ==================================================

CARD_STYLE = {
    "background": "linear-gradient(135deg,#ffffff,#f4f7ff)",
    "padding": "25px",
    "borderRadius": "15px",
    "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)",
    "textAlign": "center",
    "flex": "1"
}



app = Dash(__name__)

app.layout = html.Div(

    style={
        "padding": "30px",
        "fontFamily": "Arial",
        "backgroundColor": "#eef2f7"
    },

    children=[

        html.H1(
            "Morbid Metal Player Feedback Analytics Dashboard"
        ),

        html.P(
            "Steam Review Analysis"
        ),

        html.Hr(),

        # ==========================================
        # HERO SECTION
        # ==========================================

        html.Div(

            [

                html.H3(
                    "Key Takeaway"
                ),

                html.P(
                    f"""
                    {recommendation_rate}% of players recommend Morbid Metal.
                    Combat is the primary driver of player satisfaction,
                    while content depth, replayability and build variety
                    represent the most common improvement opportunities.
                    """
                )

            ],

            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "15px",
                "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)",
                "marginBottom": "30px"
            }
        ),

        # ==========================================
        # KPI CARDS
        # ==========================================

        html.Div(

            [

                html.Div(
                    [
                        html.H2(total_reviews),
                        html.P("Reviews Analyzed")
                    ],

                    style={
                        **CARD_STYLE,
                        "borderTop": "5px solid #34495e"
                    }
                ),

                html.Div(
                    [
                        html.H2(positive_reviews),
                        html.P("Positive Reviews")
                    ],

                    style={
                        **CARD_STYLE,
                        "borderTop": "5px solid #2ecc71"
                    }
                ),

                html.Div(
                    [
                        html.H2(negative_reviews),
                        html.P("Negative Reviews")
                    ],

                    style={
                        **CARD_STYLE,
                        "borderTop": "5px solid #e74c3c"
                    }
                ),

                html.Div(
                    [
                        html.H2(
                            f"{recommendation_rate}%"
                        ),
                        html.P(
                            "Recommendation Rate"
                        )
                    ],

                    style={
                        **CARD_STYLE,
                        "borderTop": "5px solid #3498db"
                    }
                ),

                html.Div(
                    [
                        html.H2(
                            most_discussed
                        ),
                        html.P(
                            "Most Discussed Topic"
                        )
                    ],

                    style={
                        **CARD_STYLE,
                        "borderTop": "5px solid #9b59b6"
                    }
                )

            ],

            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "35px"
            }
        ),

        # ==========================================
        # CHARTS
        # ==========================================

        html.Div(

            [

                html.Div(

                    [

                        html.H3(
                            "Most Discussed Topics"
                        ),

                        dcc.Graph(
                            figure=mention_fig,
                            config={
                                "displayModeBar": False
                            }
                        )

                    ],

                    style={
                        "width": "49%",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)"
                    }
                ),

                html.Div(

                    [

                        html.H3(
                            "Positive vs Negative Feedback"
                        ),

                        dcc.Graph(
                            figure=sentiment_fig,
                            config={
                                "displayModeBar": False
                            }
                        )

                    ],

                    style={
                        "width": "49%",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)"
                    }
                )

            ],

            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "35px"
            }
        ),

        # ==========================================
        # STRENGTHS / CONCERNS
        # ==========================================

        html.Div(

            [

                html.Div(

                    [

                        html.H3(
                            "What Players Love"
                        ),

                        dash_table.DataTable(

                            data=strengths_df[
                                [
                                    "Topic",
                                    "Positive_Rate_%"
                                ]
                            ].to_dict(
                                "records"
                            ),

                            columns=[
                                {
                                    "name": "Topic",
                                    "id": "Topic"
                                },
                                {
                                    "name": "Positive Rate %",
                                    "id": "Positive_Rate_%"
                                }
                            ]
                        )

                    ],

                    style={
                        "width": "49%",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)"
                    }
                ),

                html.Div(

                    [

                        html.H3(
                            "What Players Want Improved"
                        ),

                        dash_table.DataTable(

                            data=concerns_df[
                                [
                                    "Topic",
                                    "Negative_Mentions"
                                ]
                            ].to_dict(
                                "records"
                            ),

                            columns=[
                                {
                                    "name": "Topic",
                                    "id": "Topic"
                                },
                                {
                                    "name": "Negative Mentions",
                                    "id": "Negative_Mentions"
                                }
                            ]
                        )

                    ],

                    style={
                        "width": "49%",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "15px",
                        "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)"
                    }
                )

            ],

            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "35px"
            }
        ),

        # ==========================================
        # EXECUTIVE SUMMARY
        # ==========================================

        html.Div(

            [

                html.H2(
                    "Executive Summary"
                ),

                html.Ul(

                    [

                        html.Li(
                            f"Combat appears in {summary_df.iloc[0]['Mention_Rate_%']}% of reviews."
                        ),

                        html.Li(
                            f"Overall recommendation rate is {recommendation_rate}%."
                        ),

                        html.Li(
                            "Players consistently praise combat fluidity and visual quality."
                        ),

                        html.Li(
                            "Build variety is a major engagement driver."
                        ),

                        html.Li(
                            "Replayability and content depth remain the largest improvement opportunities."
                        )

                    ]
                )

            ],

            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "15px",
                "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)",
                "marginBottom": "35px"
            }
        ),

        # ==========================================
        # TABLE
        # ==========================================

        html.Div(

            [

                html.H2(
                    "Topic Summary"
                ),

                dash_table.DataTable(

                    data=table_df.to_dict(
                        "records"
                    ),

                    columns=[
                        {
                            "name": i,
                            "id": i
                        }
                        for i in table_df.columns
                    ],

                    page_size=12,

                    sort_action="native",

                    style_table={
                        "overflowX": "auto"
                    },

                    style_cell={
                        "textAlign": "center",
                        "padding": "10px"
                    },

                    style_header={
                        "fontWeight": "bold"
                    }
                )

            ],

            style={
                "backgroundColor": "white",
                "padding": "25px",
                "borderRadius": "15px",
                "boxShadow": "0px 4px 12px rgba(0,0,0,0.12)"
            }
        ),

        html.Br(),

        html.Hr(),

        html.P(
            "Built using Python, Pandas, Plotly and Dash",
            style={
                "textAlign": "center",
                "color": "gray"
            }
        )

    ]
)

if __name__ == "__main__":
    app.run(debug=True)
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64

def generate_party_pie_chart(df):
    """Generate a pie chart for total votes by party."""
    party_votes = df.groupby('Party')['VoteCount'].sum().reset_index()
    fig = px.pie(
        party_votes,
        names='Party',
        values='VoteCount',
        title="Total Votes by Party",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig.to_html(full_html=False)

def generate_top_states_bar_chart(df):
    """Generate a bar chart for the top 5 states where each party received the highest votes."""
    top_states = df.groupby(['Party', 'StateName'])['VoteCount'].sum().reset_index()
    top_states = top_states.sort_values(['Party', 'VoteCount'], ascending=[True, False])
    top_states = top_states.groupby('Party').head(5)
    fig = px.bar(
        top_states,
        x='VoteCount',
        y='StateName',
        color='Party',
        title="Top 5 States by Party Votes",
        orientation='h',
        labels={'VoteCount': 'Total Votes', 'StateName': 'State'}
    )
    return fig.to_html(full_html=False)

def generate_stacked_bar_chart(df):
    """Generate a stacked bar chart for vote distribution by party across states."""
    state_party_votes = df.groupby(['StateName', 'Party'])['VoteCount'].sum().reset_index()
    fig = px.bar(
        state_party_votes,
        x='StateName',
        y='VoteCount',
        color='Party',
        title="Vote Distribution by Party Across States",
        labels={'VoteCount': 'Total Votes', 'StateName': 'State'},
        barmode='stack'
    )
    return fig.to_html(full_html=False)

def generate_avg_votes_per_county(df):
    """Generate a horizontal bar chart for average votes per county by party."""
    county_avg_votes = df.groupby('Party')['VoteCount'].mean().reset_index()
    fig = px.bar(
        county_avg_votes,
        x='VoteCount',
        y='Party',
        orientation='h',
        title="Average Votes Per County by Party",
        labels={'VoteCount': 'Average Votes', 'Party': 'Party'},
        color='Party',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig.to_html(full_html=False)

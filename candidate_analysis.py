import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64

def generate_candidate_pie_chart(df):
    """Generate a pie chart for total votes by candidate."""
    candidate_votes = df.groupby('Candidate')['VoteCount'].sum().reset_index()
    fig = px.pie(
        candidate_votes,
        names='Candidate',
        values='VoteCount',
        title="Total Votes by Candidate",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig.to_html(full_html=False)

def generate_candidate_stacked_bar_chart(df):
    """Generate a stacked bar chart for candidates' top counties."""
    # Find the top counties for each candidate based on votes
    top_counties = df.groupby(['Candidate', 'CountyName'])['VoteCount'].sum().reset_index()
    top_counties = top_counties.sort_values(['Candidate', 'VoteCount'], ascending=[True, False])
    top_counties = top_counties.groupby('Candidate').head(5)

    # Create a stacked bar chart
    fig = px.bar(
        top_counties,
        x='Candidate',
        y='VoteCount',
        color='CountyName',
        title="Top Counties for Each Candidate",
        barmode='stack'
    )
    return fig.to_html(full_html=False)

def generate_lowest_votes_by_county_chart(df):
    """Generate a stacked bar chart for candidates' lowest counties by votes."""
    # Find the lowest counties for each candidate based on votes
    lowest_counties = df.groupby(['Candidate', 'CountyName'])['VoteCount'].sum().reset_index()
    lowest_counties = lowest_counties.sort_values(['Candidate', 'VoteCount'], ascending=[True, True])
    lowest_counties = lowest_counties.groupby('Candidate').head(5)

    # Create a stacked bar chart
    fig = px.bar(
        lowest_counties,
        x='Candidate',
        y='VoteCount',
        color='CountyName',
        title="Lowest Counties for Each Candidate",
        barmode='stack'
    )
    return fig.to_html(full_html=False)

def generate_top_states_per_candidate_chart(df):
    """Generate a stacked bar chart for the top states for each candidate."""
    top_states = df.groupby(['Candidate', 'StateName'])['VoteCount'].sum().reset_index()
    top_states = top_states.sort_values(['Candidate', 'VoteCount'], ascending=[True, False])
    top_states = top_states.groupby('Candidate').head(3)

    fig = px.bar(
        top_states,
        x='Candidate',
        y='VoteCount',
        color='StateName',
        title="Top States for Each Candidate",
        barmode='stack'
    )
    return fig.to_html(full_html=False)

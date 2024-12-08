import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64

def generate_top_counties_bar_chart(df):
    """Generate a bar chart for the top 10 counties by total votes."""
    top_counties = df.groupby('CountyName')['VoteCount'].sum().nlargest(10).reset_index()
    fig = px.bar(
        top_counties,
        x='VoteCount',
        y='CountyName',
        orientation='h',
        title="Top 10 Counties by Total Votes",
        labels={'VoteCount': 'Total Votes', 'CountyName': 'County'},
        color='VoteCount',
        color_continuous_scale='Viridis'
    )
    return fig.to_html(full_html=False)

def generate_party_pie_chart(df):
    """Generate a pie chart for total votes by party."""
    # Group data by Party and sum VoteCount
    party_votes = df.groupby('Party')['VoteCount'].sum().reset_index()

    # Create the pie chart
    fig = px.pie(
        party_votes,
        names='Party',
        values='VoteCount',
        title="Total Votes by Party",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig.to_html(full_html=False)


def generate_county_heatmap(df):
    """Generate a heatmap for vote distribution across counties."""
    county_votes = df.groupby(['CountyName', 'StateCode'])['VoteCount'].sum().reset_index()
    fig = px.treemap(
        county_votes,
        path=['StateCode', 'CountyName'],
        values='VoteCount',
        title="Vote Distribution Across Counties",
        color='VoteCount',
        color_continuous_scale='Plasma'
    )
    return fig.to_html(full_html=False)

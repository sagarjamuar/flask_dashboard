import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64

def generate_plotly_choropleth(df):
    """Generate a Plotly choropleth for state-level winners."""
    state_winners = df.groupby(['StateCode', 'Candidate'])['VoteCount'].sum().reset_index()
    state_winners = state_winners.loc[state_winners.groupby('StateCode')['VoteCount'].idxmax()]
    fig = px.choropleth(
        state_winners,
        locations="StateCode",
        locationmode="USA-states",
        color="Candidate",
        scope="usa",
        title="Winning Candidate by State",
        color_discrete_map={"Trump": "red", "Clinton": "blue", "Other": "green"}
    )
    return fig.to_html(full_html=False)

def generate_heatmap(df):
    """Generate a heatmap of votes by state."""
    state_votes = df.groupby(['StateCode', 'StateName'])['VoteCount'].sum().reset_index()
    fig = px.choropleth(
        state_votes,
        locations="StateCode",
        locationmode="USA-states",
        color="VoteCount",
        scope="usa",
        title="Total Votes by State",
        color_continuous_scale="Viridis"
    )
    return fig.to_html(full_html=False)

def generate_margin_analysis(df):
    """Generate a bar chart for state-level margin of victory."""
    # Calculate the total votes per candidate per state
    state_margins = df.groupby(['StateName', 'Candidate'])['VoteCount'].sum().reset_index()

    # Rank candidates within each state based on their vote count
    state_margins['Rank'] = state_margins.groupby('StateName')['VoteCount'].rank(method='dense', ascending=False)

    # Select the top two candidates for each state
    top_two = state_margins[state_margins['Rank'] <= 2]

    # Calculate the margin of victory for each state
    margin_data = (
        top_two.groupby('StateName')['VoteCount']
        .diff()
        .dropna()
        .abs()
        .reset_index()
    )

    # Map the state names for the margin
    margin_data['StateName'] = top_two['StateName'].unique()

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    margin_data = margin_data.set_index('StateName')  # Set StateName as the index
    margin_data['VoteCount'].sort_values(ascending=False).plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Margin of Victory by State', fontsize=16)
    ax.set_ylabel('Vote Margin', fontsize=12)
    ax.set_xlabel('State', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


def generate_graph_image(fig):
    """Convert Matplotlib figure to a base64-encoded image."""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)
    return graph_url

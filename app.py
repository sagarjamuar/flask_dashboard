from flask import Flask, render_template, request
from db_connection import get_database_data
from state_analysis import generate_plotly_choropleth, generate_heatmap, generate_margin_analysis, generate_graph_image
from candidate_analysis import (
    generate_candidate_pie_chart,
    generate_candidate_stacked_bar_chart,
    generate_lowest_votes_by_county_chart,
    generate_top_states_per_candidate_chart
)
from county_analysis import generate_top_counties_bar_chart, generate_party_pie_chart, generate_county_heatmap
from party_analysis import generate_party_pie_chart as generate_party_pie_chart_party, generate_top_states_bar_chart, generate_stacked_bar_chart as generate_stacked_bar_chart_party, generate_avg_votes_per_county
import pandas as pd

app = Flask(__name__)

# SQL query to fetch data
query = """
SELECT 
    ds.StateName, 
    ds.StateCode, 
    dc.CountyName, 
    dp.Party, 
    dcan.Candidate, 
    fe.VoteCount, 
    fe.CountyTotalVote
FROM fact_election_results fe
JOIN dim_county dc ON fe.CountyId = dc.CountyId
JOIN dim_state ds ON dc.StateId = ds.StateId
JOIN dim_party dp ON fe.PartyId = dp.PartyId
JOIN dim_candidate dcan ON fe.CandidateId = dcan.CandidateId
"""

# Fetch the data once for the dashboard
df = get_database_data(query)

@app.route('/')
def index():
    """Render the homepage with options."""
    return render_template('index.html', options=['State', 'County', 'Party', 'Candidate'])

@app.route('/display', methods=['POST'])
def display():
    """Handle selection and render visualizations."""
    selected_option = request.form.get('option')
    if selected_option == 'State':
        choropleth_html = generate_plotly_choropleth(df)
        heatmap_html = generate_heatmap(df)
        margin_img = generate_graph_image(generate_margin_analysis(df))
        return render_template(
            'index.html',
            options=['State', 'County', 'Party', 'Candidate'],
            selected_option=selected_option,
            choropleth_html=choropleth_html,
            heatmap_html=heatmap_html,
            margin_img=margin_img
        )
    elif selected_option == 'Candidate':
        pie_chart_html = generate_candidate_pie_chart(df)
        stacked_bar_html = generate_candidate_stacked_bar_chart(df)
        lowest_votes_chart_html = generate_lowest_votes_by_county_chart(df)
        top_states_chart_html = generate_top_states_per_candidate_chart(df)
        return render_template(
            'index.html',
            options=['State', 'County', 'Party', 'Candidate'],
            selected_option=selected_option,
            pie_chart_html=pie_chart_html,
            stacked_bar_html=stacked_bar_html,
            lowest_votes_chart_html=lowest_votes_chart_html,
            top_states_chart_html=top_states_chart_html
        )
    elif selected_option == 'County':
        bar_chart_html = generate_top_counties_bar_chart(df)
        party_pie_chart_html = generate_party_pie_chart(df)
        county_heatmap_html = generate_county_heatmap(df)
        return render_template(
            'index.html',
            options=['State', 'County', 'Party', 'Candidate'],
            selected_option=selected_option,
            bar_chart_html=bar_chart_html,
            party_pie_chart_html=party_pie_chart_html,
            county_heatmap_html=county_heatmap_html
        )
    elif selected_option == 'Party':
        party_pie_chart_html_party = generate_party_pie_chart_party(df)
        top_states_bar_html = generate_top_states_bar_chart(df)
        stacked_bar_html_party = generate_stacked_bar_chart_party(df)
        avg_votes_per_county_html = generate_avg_votes_per_county(df)
        return render_template(
            'index.html',
            options=['State', 'County', 'Party', 'Candidate'],
            selected_option=selected_option,
            party_pie_chart_html_party=party_pie_chart_html_party,
            top_states_bar_html=top_states_bar_html,
            stacked_bar_html_party=stacked_bar_html_party,
            avg_votes_per_county_html=avg_votes_per_county_html
        )
    else:
        return render_template(
            'index.html',
            options=['State', 'County', 'Party', 'Candidate'],
            selected_option=selected_option
        )

if __name__ == '__main__':
    app.run(debug=True)

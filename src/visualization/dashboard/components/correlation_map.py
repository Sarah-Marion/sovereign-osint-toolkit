"""
Kenyan Geospatial Correlation Map Visualization
Interactive map showing correlation hotspots across Kenya
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from typing import Dict, List, Any


class KenyanCorrelationMap:
    """Creates interactive maps of Kenya showing correlation hotspots"""
    
    def __init__(self):
        # Kenyan county coordinates (simplified)
        self.kenyan_counties = {
            'Nairobi': {'lat': -1.286389, 'lon': 36.817223, 'activity': 85},
            'Mombasa': {'lat': -4.0435, 'lon': 39.6682, 'activity': 65},
            'Kisumu': {'lat': -0.1022, 'lon': 34.7617, 'activity': 45},
            'Nakuru': {'lat': -0.3031, 'lon': 36.0800, 'activity': 35},
            'Eldoret': {'lat': 0.5143, 'lon': 35.2698, 'activity': 30},
            'Kakamega': {'lat': 0.2827, 'lon': 34.7519, 'activity': 25},
            'Kisii': {'lat': -0.6773, 'lon': 34.7796, 'activity': 20},
            'Meru': {'lat': 0.0557, 'lon': 37.6492, 'activity': 28},
            'Thika': {'lat': -1.0333, 'lon': 37.0833, 'activity': 32},
            'Machakos': {'lat': -1.5167, 'lon': 37.2667, 'activity': 22}
        }
    
    def create_kenyan_correlation_map(self, data_sources: List[Dict]) -> go.Figure:
        """Create an interactive map of Kenya with correlation hotspots"""
        
        # Prepare data for mapping
        map_data = []
        for county, info in self.kenyan_counties.items():
            map_data.append({
                'County': county,
                'Latitude': info['lat'],
                'Longitude': info['lon'],
                'Activity_Level': info['activity'],
                'Color_Intensity': info['activity'] / 100.0,
                'Size': info['activity'] / 5.0
            })
        
        df = pd.DataFrame(map_data)
        
        # Create the map
        fig = go.Figure()
        
        # Add county markers with size and color based on activity
        fig.add_trace(go.Scattermapbox(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers+text',
            marker=dict(
                size=df['Size'],
                color=df['Activity_Level'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Activity Level"  # FIXED: Removed deprecated 'titleside'
                ),
                opacity=0.8
            ),
            text=df['County'],
            textposition="top center",
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Activity Level: %{marker.color}<br>" +
                "<extra></extra>"
            )
        ))
        
        # Add some sample correlation lines
        correlation_lines = [
            {'from': 'Nairobi', 'to': 'Mombasa', 'strength': 0.8},
            {'from': 'Nairobi', 'to': 'Kisumu', 'strength': 0.6},
            {'from': 'Nairobi', 'to': 'Nakuru', 'strength': 0.7},
            {'from': 'Mombasa', 'to': 'Kisumu', 'strength': 0.4}
        ]
        
        for line in correlation_lines:
            from_county = self.kenyan_counties[line['from']]
            to_county = self.kenyan_counties[line['to']]
            
            fig.add_trace(go.Scattermapbox(
                lat=[from_county['lat'], to_county['lat']],
                lon=[from_county['lon'], to_county['lon']],
                mode='lines',
                line=dict(
                    width=line['strength'] * 6,
                    color='rgba(255, 107, 107, 0.6)'
                ),
                hoverinfo='text',
                text=f"Correlation: {line['strength']:.2f}",
                showlegend=False
            ))
        
        # Update map layout
        fig.update_layout(
            title='Kenyan OSINT Activity & Correlation Map',
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=-0.0236, lon=37.9062),  # Center of Kenya
                zoom=5.5
            ),
            height=600,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        return fig
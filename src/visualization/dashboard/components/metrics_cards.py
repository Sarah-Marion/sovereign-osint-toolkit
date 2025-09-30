"""
Metrics Overview Cards Component
Key metrics and statistics visualization cards
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any


class MetricsOverviewCards:
    """Creates overview metrics cards and mini-charts"""
    
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'warning': '#ffbb78',
            'danger': '#d62728'
        }
    
    def render_correlation_metrics(self, correlation_data: Dict[str, Any]):
        """Render correlation performance metrics"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            confidence = correlation_data.get('confidence_synthesis', {}).get('overall_confidence', 0)
            st.metric(
                "Confidence Score", 
                f"{confidence:.2%}",
                delta=f"{confidence*100:.0f}%",
                delta_color="normal"
            )
        
        with col2:
            entities = correlation_data.get('graph_analysis', {}).get('entity_count', 0)
            st.metric(
                "Entities Tracked",
                entities,
                delta="8 new" if entities > 0 else None
            )
        
        with col3:
            correlations = correlation_data.get('multi_modal_correlation', {}).get('correlation_network_size', 0)
            st.metric(
                "Active Correlations",
                correlations,
                delta="12% ↑" if correlations > 0 else None
            )
        
        with col4:
            clusters = correlation_data.get('cross_source_verification', {}).get('total_verified_clusters', 0)
            st.metric(
                "Verified Clusters", 
                clusters,
                delta="3 new" if clusters > 0 else None
            )
    
    def render_performance_gauges(self, correlation_data: Dict[str, Any]):
        """Render performance gauge charts"""
        
        st.subheader("System Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._render_gauge_chart(
                "Pattern Accuracy", 
                correlation_data.get('ml_patterns', {}).get('pattern_significance', 0) * 100,
                "Pattern Detection"
            )
        
        with col2:
            self._render_gauge_chart(
                "Correlation Strength",
                correlation_data.get('multi_modal_correlation', {}).get('average_correlation', 0) * 100,
                "Multi-modal Analysis"
            )
        
        with col3:
            self._render_gauge_chart(
                "Verification Confidence",
                correlation_data.get('cross_source_verification', {}).get('average_verification_confidence', 0) * 100,
                "Cross-source Verification"
            )
    
    def _render_gauge_chart(self, title: str, value: float, domain: str):
        """Render a single gauge chart"""
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
    
    def render_entity_type_breakdown(self, correlation_data: Dict[str, Any]):
        """Render entity type distribution pie chart"""
        
        # Sample entity type distribution
        entity_types = {
            'Political Figures': 15,
            'Locations': 25, 
            'Organizations': 20,
            'Topics': 30,
            'Events': 10
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(entity_types.keys()),
            values=list(entity_types.values()),
            hole=.3,
            marker_colors=[self.colors['primary'], self.colors['secondary'], 
                          self.colors['success'], self.colors['warning'], 
                          self.colors['danger']]
        )])
        
        fig.update_layout(
            title="Entity Type Distribution",
            height=300,
            showlegend=True,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_temporal_trend(self, time_data: List[Dict]):
        """Render temporal trend mini-chart"""
        
        # Sample time series data
        dates = pd.date_range(start='2024-01-01', periods=15, freq='D')
        correlation_strength = [0.6, 0.65, 0.7, 0.68, 0.75, 0.8, 0.78, 0.82, 0.85, 0.83, 0.88, 0.9, 0.87, 0.92, 0.95]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=correlation_strength,
            mode='lines',
            line=dict(color=self.colors['primary'], width=3),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        fig.update_layout(
            title="Correlation Strength Trend",
            xaxis_title="Date",
            yaxis_title="Strength",
            height=200,
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
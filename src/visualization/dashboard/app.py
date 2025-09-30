"""
Main Streamlit Dashboard for Sovereign OSINT Toolkit
Interactive visualization of correlations, entities, and monitoring alerts
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

try:
    from src.analyzers.sovereign_correlator import SovereignCorrelator
    from src.monitoring.sovereign_monitor import SovereignMonitor
except ImportError:
    # Fallback for direct execution
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from analyzers.sovereign_correlator import SovereignCorrelator
    from monitoring.sovereign_monitor import SovereignMonitor

from .components.network_graph import EntityNetworkGraph
from .components.correlation_map import KenyanCorrelationMap
from .components.alerts_panel import MonitoringAlertsPanel
from .components.metrics_cards import MetricsOverviewCards


class SovereignDashboard:
    """Main dashboard class for Sovereign OSINT visualization"""
    
    def __init__(self):
        # FIXED: Handle import errors gracefully
        try:
            self.correlator = SovereignCorrelator()
            self.monitor = SovereignMonitor(self.correlator)
        except Exception as e:
            st.warning(f"⚠️ Correlation engine unavailable: {e}")
            self.correlator = None
            self.monitor = None
            
        self.network_viz = EntityNetworkGraph()
        self.map_viz = KenyanCorrelationMap()
        self.alerts_panel = MonitoringAlertsPanel()
        self.metrics_cards = MetricsOverviewCards()
        
        # Sample data for demonstration
        self.sample_data = self._generate_sample_data()
        
    def _generate_sample_data(self):
        """Generate sample correlation data for demonstration"""
        return [
            {
                "title": "Nairobi Infrastructure Project",
                "content": "New highway construction in Nairobi County announced by government",
                "timestamp": datetime.now().isoformat(),
                "source": "government",
                "entities": ["nairobi", "government", "infrastructure"]
            },
            {
                "title": "Mombasa Port Expansion", 
                "content": "Port of Mombasa expansion facing construction delays",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "source": "news",
                "entities": ["mombasa", "port", "development"]
            },
            {
                "title": "Kisumu Agricultural Development",
                "content": "New farming initiatives in Kisumu County to boost agriculture",
                "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(), 
                "source": "ngo",
                "entities": ["kisumu", "agriculture", "development"]
            },
            {
                "title": "Political Meeting in Nairobi",
                "content": "Key political figures meeting in Nairobi to discuss development",
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "source": "official",
                "entities": ["nairobi", "ruto", "raila", "development"]
            }
        ]
    
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Sovereign OSINT Dashboard",
            page_icon="🦁",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
        }
        .alert-high {
            background-color: #ffcccc;
            padding: 0.5rem;
            border-radius: 5px;
            border-left: 4px solid #ff0000;
        }
        .alert-medium {
            background-color: #fff3cd;
            padding: 0.5rem;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with controls and filters"""
        with st.sidebar:
            st.title("🦁 Sovereign Controls")
            
            # Data source selection
            st.subheader("Data Sources")
            source_gov = st.checkbox("Government Sources", value=True)
            source_news = st.checkbox("News Media", value=True)
            source_social = st.checkbox("Social Media", value=True)
            source_ngo = st.checkbox("NGO Reports", value=True)
            
            # Time range filter
            st.subheader("Time Range")
            time_range = st.selectbox(
                "Select Time Range",
                ["Last 24 hours", "Last 7 days", "Last 30 days", "All time"]
            )
            
            # Entity filters
            st.subheader("Entity Filters")
            selected_entities = st.multiselect(
                "Filter by Entities",
                ["ruto", "raila", "nairobi", "mombasa", "kisumu", "development", "infrastructure"],
                default=["nairobi", "development"]
            )
            
            # Analysis type
            st.subheader("Analysis Mode")
            analysis_mode = st.radio(
                "Correlation Mode",
                ["Standard", "Advanced ML", "Real-time Monitoring"]
            )
            
            # Action buttons
            st.subheader("Actions")
            if st.button("🔄 Refresh Analysis", type="primary"):
                st.rerun()
                
            if st.button("📊 Generate Report"):
                st.success("Report generation started...")
    
    def render_header(self):
        """Render the main header and overview"""
        st.markdown('<h1 class="main-header">🦁 Sovereign OSINT Intelligence Dashboard</h1>', unsafe_allow_html=True)
        
        # Quick stats row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Data Sources", "12", "3 new")
        with col2:
            st.metric("Entities Tracked", "47", "8% ↑")
        with col3:
            st.metric("Active Correlations", "23", "12% ↑") 
        with col4:
            st.metric("Alerts", "2", "1 new")
    
    def render_network_graph(self):
        """Render entity relationship network graph"""
        st.header("🔗 Entity Relationship Network")
        
        # Run correlation on sample data
        correlation_result = self.correlator.correlate_data(self.sample_data, advanced=True)
        
        # Create network visualization
        fig = self.network_viz.create_network_graph(correlation_result)
        st.plotly_chart(fig, use_container_width=True)
        
        # Network metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Network Nodes", correlation_result['graph_analysis']['entity_count'])
        with col2:
            st.metric("Relationships", correlation_result['graph_analysis']['relationship_count'])
        with col3:
            st.metric("Graph Density", f"{correlation_result['graph_analysis']['graph_density']:.2f}")
    
    def render_kenyan_map(self):
        """Render Kenyan geospatial correlation map"""
        st.header("🗺️ Kenyan Geospatial Analysis")
        
        # Create Kenyan map with correlation hotspots
        fig = self.map_viz.create_kenyan_correlation_map(self.sample_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Location statistics
        locations = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
        location_counts = [8, 5, 3, 2, 1]  # Sample data
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Activity by Location")
            location_df = pd.DataFrame({
                "Location": locations,
                "Activity Count": location_counts
            })
            st.dataframe(location_df, use_container_width=True)
        
        with col2:
            st.subheader("Top Correlated Regions")
            # Simple bar chart
            fig_bar = go.Figure(data=[
                go.Bar(x=locations, y=location_counts, marker_color='#1f77b4')
            ])
            fig_bar.update_layout(
                title="Regional Activity Distribution",
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    def render_correlation_analysis(self):
        """Render multi-modal correlation analysis"""
        st.header("📈 Multi-Modal Correlation Analysis")
        
        # Run advanced correlation
        correlation_result = self.correlator.correlate_data(self.sample_data, advanced=True)
        
        # Correlation metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            confidence = correlation_result['confidence_synthesis']['overall_confidence']
            st.metric("Overall Confidence", f"{confidence:.2%}")
        with col2:
            avg_corr = correlation_result['multi_modal_correlation']['average_correlation']
            st.metric("Average Correlation", f"{avg_corr:.2f}")
        with col3:
            clusters = correlation_result['cross_source_verification']['total_verified_clusters']
            st.metric("Verified Clusters", clusters)
        
        # Correlation matrix (simplified)
        st.subheader("Correlation Matrix")
        entities = ["ruto", "raila", "nairobi", "mombasa", "development"]
        correlation_matrix = [
            [1.0, 0.3, 0.8, 0.2, 0.7],
            [0.3, 1.0, 0.6, 0.1, 0.4],
            [0.8, 0.6, 1.0, 0.3, 0.9],
            [0.2, 0.1, 0.3, 1.0, 0.2],
            [0.7, 0.4, 0.9, 0.2, 1.0]
        ]
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=entities,
            y=entities,
            colorscale='Blues',
            showscale=True
        ))
        fig_heatmap.update_layout(
            title="Entity Correlation Matrix",
            xaxis_title="Entities",
            yaxis_title="Entities"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    def render_monitoring_alerts(self):
        """Render real-time monitoring alerts panel"""
        st.header("🚨 Monitoring & Alerts")
        
        # Sample alerts data
        sample_alerts = [
            {
                "id": 1,
                "timestamp": datetime.now() - timedelta(minutes=15),
                "level": "HIGH",
                "type": "Pattern Detection",
                "message": "Unusual correlation pattern detected in Nairobi political discourse",
                "entities": ["nairobi", "ruto", "raila"]
            },
            {
                "id": 2, 
                "timestamp": datetime.now() - timedelta(hours=2),
                "level": "MEDIUM",
                "type": "Source Verification",
                "message": "Multiple sources reporting infrastructure developments",
                "entities": ["development", "infrastructure"]
            }
        ]
        
        # Render alerts panel
        self.alerts_panel.render_alerts(sample_alerts)
        
        # Alert statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Alerts", len(sample_alerts))
        with col2:
            st.metric("High Severity", 1)
        with col3:
            st.metric("Response Time", "15min")
    
    def render_temporal_analysis(self):
        """Render temporal analysis timeline"""
        st.header("⏰ Temporal Analysis")
        
        # Sample timeline data
        dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
        activity_levels = [5, 7, 12, 8, 15, 20, 18, 14, 16, 22, 19, 17, 21, 25, 23]
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=dates,
            y=activity_levels,
            mode='lines+markers',
            name='OSINT Activity',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        fig_timeline.update_layout(
            title="OSINT Activity Timeline (Last 15 Days)",
            xaxis_title="Date",
            yaxis_title="Activity Level",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    def run_dashboard(self):
        """Main method to run the complete dashboard"""
        self.setup_page()
        self.render_sidebar()
        self.render_header()
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview", 
            "🔗 Network Analysis", 
            "🗺️ Geospatial", 
            "🚨 Monitoring"
        ])
        
        with tab1:
            self.render_network_graph()
            st.divider()
            self.render_correlation_analysis()
            
        with tab2:
            col1, col2 = st.columns([2, 1])
            with col1:
                self.render_network_graph()
            with col2:
                self.render_temporal_analysis()
                
        with tab3:
            self.render_kenyan_map()
            
        with tab4:
            self.render_monitoring_alerts()


def launch_dashboard():
    """Launch the Sovereign OSINT Dashboard"""
    dashboard = SovereignDashboard()
    dashboard.run_dashboard()


if __name__ == "__main__":
    launch_dashboard()
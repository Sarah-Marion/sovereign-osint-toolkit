"""
Entity Relationship Network Graph Visualization
Interactive network visualization of entity correlations
"""

import plotly.graph_objects as go
import networkx as nx
import streamlit as st
from typing import Dict, List, Any


class EntityNetworkGraph:
    """Creates interactive network graphs for entity relationships"""
    
    def __init__(self):
        self.colors = {
            'political_figures': '#FF6B6B',
            'locations': '#4ECDC4', 
            'organizations': '#45B7D1',
            'topics': '#96CEB4'
        }
    
    def create_network_graph(self, correlation_data: Dict[str, Any]) -> go.Figure:
        """Create an interactive network graph from correlation data"""
        
        # Create network graph
        G = nx.Graph()
        
        # Sample entity data (in production, this would come from correlation_data)
        entities = {
            'ruto': {'type': 'political_figures', 'size': 25},
            'raila': {'type': 'political_figures', 'size': 20},
            'nairobi': {'type': 'locations', 'size': 30},
            'mombasa': {'type': 'locations', 'size': 15},
            'kisumu': {'type': 'locations', 'size': 12},
            'development': {'type': 'topics', 'size': 18},
            'infrastructure': {'type': 'topics', 'size': 16},
            'government': {'type': 'organizations', 'size': 22}
        }
        
        # Sample relationships
        relationships = [
            ('ruto', 'nairobi', 0.8),
            ('raila', 'nairobi', 0.7),
            ('ruto', 'development', 0.9),
            ('raila', 'development', 0.6),
            ('nairobi', 'development', 0.95),
            ('mombasa', 'infrastructure', 0.7),
            ('kisumu', 'development', 0.5),
            ('government', 'development', 0.85),
            ('government', 'infrastructure', 0.75)
        ]
        
        # Add nodes and edges to graph
        for entity, props in entities.items():
            G.add_node(entity, **props)
            
        for source, target, weight in relationships:
            G.add_edge(source, target, weight=weight)
        
        # Get node positions using spring layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Extract node positions
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_size.append(entities[node]['size'])
            node_color.append(self.colors[entities[node]['type']])
        
        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=node_size,
                color=node_color,
                line=dict(width=2, color='darkblue')
            )
        )
        
        # Create edge traces
        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            weight = G[edge[0]][edge[1]]['weight']
            
            edge_trace = go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                line=dict(width=weight*5, color='rgba(128, 128, 128, 0.75)'),
                hoverinfo='text',
                text=f"Strength: {weight:.2f}",
                mode='lines'
            )
            edge_traces.append(edge_trace)
        
        # Create the figure
        fig = go.Figure()
        
        # Add edges first (so they appear behind nodes)
        for edge_trace in edge_traces:
            fig.add_trace(edge_trace)
        
        # Add nodes
        fig.add_trace(node_trace)
        
        # FIXED: Updated layout with modern Plotly syntax
        fig.update_layout(
            title=dict(
                text='Entity Relationship Network',
                font=dict(size=16)  # FIXED: Use font dict instead of titlefont_size
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                text="Node size indicates entity importance<br>Line thickness indicates relationship strength",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(size=10, color="gray")
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )
        
        return fig
    
    def create_community_graph(self, correlation_data: Dict[str, Any]) -> go.Figure:
        """Create network graph with community detection"""
        # This would implement community detection visualization
        # Placeholder for advanced community visualization
        return self.create_network_graph(correlation_data)

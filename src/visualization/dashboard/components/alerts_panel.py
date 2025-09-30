"""
Monitoring Alerts Panel Visualization
Real-time display of monitoring alerts and notifications
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Any


class MonitoringAlertsPanel:
    """Displays real-time monitoring alerts with severity levels"""
    
    def __init__(self):
        self.alert_styles = {
            'HIGH': {
                'color': '#FF6B6B',
                'icon': '🔴',
                'background': '#FFE6E6',
                'border': '#FF6B6B'
            },
            'MEDIUM': {
                'color': '#FFA726', 
                'icon': '🟡',
                'background': '#FFF3E0',
                'border': '#FFA726'
            },
            'LOW': {
                'color': '#4ECDC4',
                'icon': '🔵',
                'background': '#E0F2F1',
                'border': '#4ECDC4'
            },
            'INFO': {
                'color': '#78909C',
                'icon': 'ℹ️',
                'background': '#ECEFF1',
                'border': '#78909C'
            }
        }
    
    def render_alerts(self, alerts: List[Dict[str, Any]]):
        """Render the alerts panel with all active alerts"""
        
        if not alerts:
            st.info("🎉 No active alerts. System is running normally.")
            return
        
        # Sort alerts by severity and timestamp
        severity_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'INFO': 3}
        alerts.sort(key=lambda x: (severity_order[x['level']], x['timestamp']))
        
        # Display each alert
        for alert in alerts:
            self._render_single_alert(alert)
    
    def _render_single_alert(self, alert: Dict[str, Any]):
        """Render a single alert card"""
        
        style = self.alert_styles[alert['level']]
        
        # Create custom HTML for alert card
        alert_html = f"""
        <div style="
            background-color: {style['background']};
            border-left: 4px solid {style['border']};
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">{style['icon']}</span>
                    <strong style="color: {style['color']};">{alert['level']}</strong>
                </div>
                <small style="color: #666;">{self._format_timestamp(alert['timestamp'])}</small>
            </div>
            <div style="margin-top: 0.5rem;">
                <strong>{alert['type']}</strong>: {alert['message']}
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                <strong>Entities:</strong> {', '.join(alert.get('entities', []))}
            </div>
        </div>
        """
        
        st.markdown(alert_html, unsafe_allow_html=True)
    
    def _format_timestamp(self, timestamp) -> str:
        """Format timestamp for display"""
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return timestamp
        
        if isinstance(timestamp, datetime):
            now = datetime.now()
            diff = now - timestamp
            
            if diff < timedelta(minutes=1):
                return "Just now"
            elif diff < timedelta(hours=1):
                minutes = int(diff.total_seconds() / 60)
                return f"{minutes}m ago"
            elif diff < timedelta(days=1):
                hours = int(diff.total_seconds() / 3600)
                return f"{hours}h ago"
            else:
                days = diff.days
                return f"{days}d ago"
        
        return str(timestamp)
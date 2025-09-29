"""
Sovereign OSINT Toolkit - Real-time Monitoring System
Continuous monitoring and alerting for Kenyan OSINT patterns
By Sarah Marion
"""

import time
import threading
from datetime import datetime, timedelta
from collections import deque, defaultdict
from typing import Dict, List, Any, Optional, Callable
import json
import logging
from dataclasses import dataclass
from enum import Enum


class AlertLevel(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"


class PatternType(Enum):
    ACTIVITY_SPIKE = "activity_spike"
    SENTIMENT_SHIFT = "sentiment_shift"
    ENTITY_EMERGENCE = "entity_emergence"
    CORRELATION_CHANGE = "correlation_change"
    ANOMALY_DETECTED = "anomaly_detected"


@dataclass
class MonitoringAlert:
    """Represents a monitoring alert"""
    alert_id: str
    pattern_type: PatternType
    alert_level: AlertLevel
    title: str
    description: str
    timestamp: datetime
    confidence: float
    affected_entities: List[str]
    data_sources: List[str]
    recommendations: List[str]


class SovereignMonitor:
    """Real-time monitoring system for Kenyan OSINT patterns"""
    
    def __init__(self, correlator, config: Optional[Dict] = None):
        self.correlator = correlator
        self.config = {
            "monitoring_interval": 300,  # 5 minutes
            "activity_spike_threshold": 2.0,  # 2x normal activity
            "sentiment_shift_threshold": 0.3,  # 30% sentiment change
            "alert_confidence_threshold": 0.7,
            "max_history_hours": 24,
            "pattern_decay_factor": 0.95,
            **({} if config is None else config)
        }
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alert_handlers = []
        
        # Historical data for trend analysis
        self.activity_history = deque(maxlen=100)
        self.sentiment_history = deque(maxlen=100)
        self.entity_frequency_history = defaultdict(lambda: deque(maxlen=50))
        self.correlation_history = deque(maxlen=50)
        
        # Alert tracking
        self.active_alerts = {}
        self.alert_history = deque(maxlen=1000)
        
        # Current baseline patterns
        self.baseline_activity = 0
        self.baseline_sentiment = 0
        self.entity_baselines = defaultdict(float)
        
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """Setup monitoring-specific logging"""
        logger = logging.getLogger('sovereign_monitor')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def start_monitoring(self):
        """Start the real-time monitoring system"""
        if self.monitoring_active:
            self.logger.warning("Monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("🔄 Real-time monitoring started")
    
    def stop_monitoring(self):
        """Stop the real-time monitoring system"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        self.logger.info("🛑 Real-time monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Run monitoring cycle
                self._monitoring_cycle()
                
                # Wait for next cycle
                time.sleep(self.config["monitoring_interval"])
                
            except Exception as e:
                self.logger.error(f"Monitoring cycle error: {e}")
                time.sleep(60)  # Wait before retrying
    
    def _monitoring_cycle(self):
        """Single monitoring cycle - analyze current state and detect changes"""
        self.logger.info("🔍 Running monitoring cycle...")
        
        # Get current correlation state (simulated - would be real data in production)
        current_state = self._get_current_correlation_state()
        
        # Update historical data
        self._update_monitoring_history(current_state)
        
        # Detect pattern changes
        alerts = self._detect_pattern_changes(current_state)
        
        # Process detected alerts
        for alert in alerts:
            self._process_alert(alert)
        
        # Update baselines
        self._update_baselines()
        
        self.logger.info(f"✅ Monitoring cycle completed. Alerts: {len(alerts)}")
    
    def _get_current_correlation_state(self) -> Dict[str, Any]:
        """Get current correlation state (simulated for demo)"""
        # In production, this would get real-time data from collectors
        # For now, simulate some data patterns
        
        return {
            "timestamp": datetime.now(),
            "activity_level": self._simulate_activity_level(),
            "sentiment_score": self._simulate_sentiment_score(),
            "entity_frequencies": self._simulate_entity_frequencies(),
            "correlation_strength": self._simulate_correlation_strength(),
            "data_sources": ["simulated_stream_1", "simulated_stream_2"]
        }
    
    def _simulate_activity_level(self) -> float:
        """Simulate activity level with occasional spikes"""
        base_level = 5.0  # Base activity level
        
        # Simulate occasional spikes (every 6 cycles on average)
        if len(self.activity_history) % 6 == 3:
            return base_level * 3.0  # Activity spike
        
        return base_level + (time.time() % 3)  # Small variations
    
    def _simulate_sentiment_score(self) -> float:
        """Simulate sentiment score with gradual changes"""
        base_sentiment = 0.2  # Slightly positive baseline
        
        # Simulate sentiment shifts occasionally
        if len(self.sentiment_history) % 8 == 5:
            return -0.4  # Negative shift
        
        return base_sentiment + ((time.time() % 2) - 1) * 0.1  # Small variations
    
    def _simulate_entity_frequencies(self) -> Dict[str, float]:
        """Simulate entity mention frequencies"""
        entities = {
            "ruto": 0.8,
            "nairobi": 0.7,
            "development": 0.6,
            "mombasa": 0.4,
            "raila": 0.3,
            "infrastructure": 0.5
        }
        
        # Occasionally boost specific entities
        if len(self.entity_frequency_history) % 10 == 7:
            entities["ruto"] = 2.5  # Entity emergence
        
        return entities
    
    def _simulate_correlation_strength(self) -> float:
        """Simulate correlation strength"""
        base_strength = 0.6
        
        # Simulate correlation changes
        if len(self.correlation_history) % 12 == 8:
            return 0.9  # Strong correlation event
        
        return base_strength + (time.time() % 0.3)  # Small variations
    
    def _update_monitoring_history(self, current_state: Dict):
        """Update monitoring history with current state"""
        self.activity_history.append(current_state["activity_level"])
        self.sentiment_history.append(current_state["sentiment_score"])
        self.correlation_history.append(current_state["correlation_strength"])
        
        # Update entity frequencies
        for entity, frequency in current_state["entity_frequencies"].items():
            self.entity_frequency_history[entity].append(frequency)
    
    def _detect_pattern_changes(self, current_state: Dict) -> List[MonitoringAlert]:
        """Detect significant pattern changes that warrant alerts"""
        alerts = []
        
        # Detect activity spikes
        activity_alerts = self._detect_activity_spikes(current_state)
        alerts.extend(activity_alerts)
        
        # Detect sentiment shifts
        sentiment_alerts = self._detect_sentiment_shifts(current_state)
        alerts.extend(sentiment_alerts)
        
        # Detect entity emergence
        entity_alerts = self._detect_entity_emergence(current_state)
        alerts.extend(entity_alerts)
        
        # Detect correlation changes
        correlation_alerts = self._detect_correlation_changes(current_state)
        alerts.extend(correlation_alerts)
        
        return alerts
    
    def _detect_activity_spikes(self, current_state: Dict) -> List[MonitoringAlert]:
        """Detect unusual activity spikes"""
        alerts = []
        current_activity = current_state["activity_level"]
        
        if len(self.activity_history) < 5:
            return alerts  # Need more history
        
        # Calculate moving average (last 10 readings)
        recent_activity = list(self.activity_history)[-10:]
        avg_activity = sum(recent_activity) / len(recent_activity)
        
        if avg_activity > 0:  # Avoid division by zero
            activity_ratio = current_activity / avg_activity
            
            if activity_ratio > self.config["activity_spike_threshold"]:
                alert = MonitoringAlert(
                    alert_id=f"activity_spike_{int(time.time())}",
                    pattern_type=PatternType.ACTIVITY_SPIKE,
                    alert_level=AlertLevel.HIGH if activity_ratio > 3.0 else AlertLevel.MEDIUM,
                    title="Unusual Activity Spike Detected",
                    description=f"Activity level increased {activity_ratio:.1f}x above normal",
                    timestamp=current_state["timestamp"],
                    confidence=min(activity_ratio / 4.0, 1.0),
                    affected_entities=["system_wide"],
                    data_sources=current_state["data_sources"],
                    recommendations=[
                        "Investigate recent data sources",
                        "Check for coordinated campaigns",
                        "Review entity frequency changes"
                    ]
                )
                alerts.append(alert)
        
        return alerts
    
    def _detect_sentiment_shifts(self, current_state: Dict) -> List[MonitoringAlert]:
        """Detect significant sentiment shifts"""
        alerts = []
        current_sentiment = current_state["sentiment_score"]
        
        if len(self.sentiment_history) < 5:
            return alerts
        
        # Calculate sentiment baseline (excluding recent data)
        historical_sentiment = list(self.sentiment_history)[:-3]  # Exclude last 3 readings
        if not historical_sentiment:
            return alerts
        
        baseline_sentiment = sum(historical_sentiment) / len(historical_sentiment)
        sentiment_change = abs(current_sentiment - baseline_sentiment)
        
        if sentiment_change > self.config["sentiment_shift_threshold"]:
            direction = "positive" if current_sentiment > baseline_sentiment else "negative"
            
            alert = MonitoringAlert(
                alert_id=f"sentiment_shift_{int(time.time())}",
                pattern_type=PatternType.SENTIMENT_SHIFT,
                alert_level=AlertLevel.MEDIUM,
                title=f"Significant {direction.capitalize()} Sentiment Shift",
                description=f"Sentiment changed by {sentiment_change:.2f} ({direction} direction)",
                timestamp=current_state["timestamp"],
                confidence=min(sentiment_change / 0.5, 1.0),  # Normalize to 0-1
                affected_entities=["discourse_wide"],
                data_sources=current_state["data_sources"],
                recommendations=[
                    "Analyze recent content for sentiment drivers",
                    "Check for influential accounts or sources",
                    "Monitor for coordinated narrative shifts"
                ]
            )
            alerts.append(alert)
        
        return alerts
    
    def _detect_entity_emergence(self, current_state: Dict) -> List[MonitoringAlert]:
        """Detect emerging entities or topics"""
        alerts = []
        current_entities = current_state["entity_frequencies"]
        
        for entity, current_freq in current_entities.items():
            history = self.entity_frequency_history[entity]
            
            if len(history) < 5:
                continue
            
            # Calculate baseline frequency (excluding recent data)
            historical_freq = list(history)[:-2]  # Exclude last 2 readings
            if not historical_freq:
                continue
            
            baseline_freq = sum(historical_freq) / len(historical_freq)
            
            if baseline_freq > 0:  # Avoid division by zero
                emergence_ratio = current_freq / baseline_freq
                
                if emergence_ratio > 2.5:  # Entity mentioned 2.5x more than usual
                    alert = MonitoringAlert(
                        alert_id=f"entity_emergence_{entity}_{int(time.time())}",
                        pattern_type=PatternType.ENTITY_EMERGENCE,
                        alert_level=AlertLevel.MEDIUM,
                        title=f"Entity Emergence: {entity.title()}",
                        description=f"Entity '{entity}' mentioned {emergence_ratio:.1f}x more than usual",
                        timestamp=current_state["timestamp"],
                        confidence=min(emergence_ratio / 4.0, 1.0),
                        affected_entities=[entity],
                        data_sources=current_state["data_sources"],
                        recommendations=[
                            f"Investigate context of '{entity}' mentions",
                            "Check for related entities and topics",
                            "Monitor for coordinated discussion"
                        ]
                    )
                    alerts.append(alert)
        
        return alerts
    
    def _detect_correlation_changes(self, current_state: Dict) -> List[MonitoringAlert]:
        """Detect significant correlation changes"""
        alerts = []
        current_correlation = current_state["correlation_strength"]
        
        if len(self.correlation_history) < 5:
            return alerts
        
        # Calculate correlation baseline
        historical_correlation = list(self.correlation_history)[:-2]
        if not historical_correlation:
            return alerts
        
        baseline_correlation = sum(historical_correlation) / len(historical_correlation)
        correlation_change = abs(current_correlation - baseline_correlation)
        
        if correlation_change > 0.3:  # Significant correlation change
            alert_level = AlertLevel.HIGH if correlation_change > 0.5 else AlertLevel.MEDIUM
            
            alert = MonitoringAlert(
                alert_id=f"correlation_change_{int(time.time())}",
                pattern_type=PatternType.CORRELATION_CHANGE,
                alert_level=alert_level,
                title="Significant Correlation Pattern Change",
                description=f"Correlation strength changed by {correlation_change:.2f}",
                timestamp=current_state["timestamp"],
                confidence=min(correlation_change / 0.7, 1.0),
                affected_entities=["correlation_network"],
                data_sources=current_state["data_sources"],
                recommendations=[
                    "Review recent entity relationships",
                    "Check for new correlation patterns",
                    "Analyze temporal and spatial correlations"
                ]
            )
            alerts.append(alert)
        
        return alerts
    
    def _process_alert(self, alert: MonitoringAlert):
        """Process a detected alert"""
        if alert.confidence < self.config["alert_confidence_threshold"]:
            return  # Ignore low-confidence alerts
        
        # Store alert
        self.active_alerts[alert.alert_id] = alert
        self.alert_history.append(alert)
        
        # Log alert
        self.logger.warning(
            f"🚨 ALERT [{alert.alert_level.value}] {alert.pattern_type.value}: "
            f"{alert.title} (confidence: {alert.confidence:.2f})"
        )
        
        # Notify alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                self.logger.error(f"Alert handler error: {e}")
    
    def _update_baselines(self):
        """Update baseline patterns based on historical data"""
        if self.activity_history:
            self.baseline_activity = sum(self.activity_history) / len(self.activity_history)
        
        if self.sentiment_history:
            self.baseline_sentiment = sum(self.sentiment_history) / len(self.sentiment_history)
        
        # Update entity baselines
        for entity, history in self.entity_frequency_history.items():
            if history:
                self.entity_baselines[entity] = sum(history) / len(history)
    
    def add_alert_handler(self, handler: Callable[[MonitoringAlert], None]):
        """Add a custom alert handler"""
        self.alert_handlers.append(handler)
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            "monitoring_active": self.monitoring_active,
            "alerts_active": len(self.active_alerts),
            "alerts_total": len(self.alert_history),
            "baseline_activity": self.baseline_activity,
            "baseline_sentiment": self.baseline_sentiment,
            "entity_baselines": dict(self.entity_baselines),
            "recent_activity": list(self.activity_history)[-10:] if self.activity_history else [],
            "config": self.config
        }
    
    def get_recent_alerts(self, limit: int = 10) -> List[MonitoringAlert]:
        """Get recent alerts"""
        return list(self.alert_history)[-limit:]
    
    def clear_alerts(self):
        """Clear active alerts"""
        self.active_alerts.clear()
        self.logger.info("Cleared all active alerts")


# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the monitor
    from analyzers.sovereign_correlator import SovereignCorrelator
    
    class ExampleAlertHandler:
        def __call__(self, alert: MonitoringAlert):
            print(f"📢 ALERT RECEIVED: {alert.title}")
            print(f"   Level: {alert.alert_level.value}")
            print(f"   Confidence: {alert.confidence:.2f}")
            print(f"   Description: {alert.description}")
            print("   ---")
    
    # Create correlator and monitor
    correlator = SovereignCorrelator()
    monitor = SovereignMonitor(correlator)
    
    # Add alert handler
    monitor.add_alert_handler(ExampleAlertHandler())
    
    # Start monitoring
    monitor.start_monitoring()
    
    print("🚀 Real-time monitoring started with example handler")
    print("Monitoring for 30 seconds...")
    
    # Let it run for a while to generate alerts
    time.sleep(30)
    
    # Get status
    status = monitor.get_monitoring_status()
    print(f"\n📊 Monitoring Status:")
    print(f"   Active: {status['monitoring_active']}")
    print(f"   Active Alerts: {status['alerts_active']}")
    print(f"   Total Alerts: {status['alerts_total']}")
    
    # Stop monitoring
    monitor.stop_monitoring()
    print("🛑 Monitoring stopped")
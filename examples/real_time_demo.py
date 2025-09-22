"""
Demo: Real-time Monitoring for Kenyan Context
Example usage of the real-time monitoring system
By Sarah Marion
"""

from src.collectors.real_time_monitor import KenyanRealTimeMonitor
import json
from datetime import datetime

def monitoring_callback(data, source_type):
    """Callback function to handle new monitoring data"""
    print(f"\n📡 New data from {source_type} at {datetime.now():%H:%M:%S}")
    for item in data:
        print(f"• {item.get('title', item.get('text', 'No title'))}")
        if 'kenyan_context_score' in item:
            print(f"  Kenyan relevance: {item['kenyan_context_score']:.2f}")

def main():
    """Demo the real-time monitoring system"""
    monitor = KenyanRealTimeMonitor()
    
    # Start monitoring Kenyan Twitter for political discussions
    twitter_monitor = monitor.start_monitoring(
        source_type="twitter_ke",
        keywords=["politics", "government", "county"],
        callback=monitoring_callback,
        interval=60  # Check every 60 seconds for demo
    )
    
    # Start monitoring news sources
    news_monitor = monitor.start_monitoring(
        source_type="news_sources", 
        keywords=["development", "infrastructure", "budget"],
        callback=monitoring_callback,
        interval=120
    )
    
    print("🎯 Started real-time monitoring with Kenyan context")
    print("Monitoring topics: Kenyan politics, development news, government updates")
    print("Press Ctrl+C to stop monitoring...")
    
    try:
        # Keep the main thread alive
        while True:
            status = monitor.get_monitoring_status()
            print(f"\rActive monitors: {status['active_monitors']} | Total: {status['total_monitors']}", end="")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all monitors...")
        monitor.stop_monitoring(twitter_monitor)
        monitor.stop_monitoring(news_monitor)
        print("Monitoring stopped.")

if __name__ == "__main__":
    import time
    main()
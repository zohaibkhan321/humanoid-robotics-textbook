import time
from typing import Dict, Any, Callable
from collections import defaultdict, deque
from datetime import datetime, timedelta
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Simple metrics collection service for monitoring
    Tracks API usage, response times, error rates, and other key metrics
    """

    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'errors': 0,
            'total_response_time': 0.0,
            'avg_response_time': 0.0
        })
        self.start_time = datetime.now()

    def record_request(self, endpoint: str, response_time: float, is_error: bool = False):
        """
        Record a request with its response time and error status
        """
        self.request_count += 1

        if is_error:
            self.error_count += 1

        self.response_times.append(response_time)

        # Update endpoint-specific stats
        stats = self.endpoint_stats[endpoint]
        stats['count'] += 1
        if is_error:
            stats['errors'] += 1
        stats['total_response_time'] += response_time
        stats['avg_response_time'] = stats['total_response_time'] / stats['count']

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics
        """
        uptime = (datetime.now() - self.start_time).total_seconds()

        # Calculate error rate
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0

        # Calculate average response time
        avg_response_time = (
            sum(self.response_times) / len(self.response_times) if self.response_times else 0
        )

        # Calculate p95 response time
        if self.response_times:
            sorted_times = sorted(self.response_times)
            p95_idx = int(0.95 * len(sorted_times))
            p95_response_time = sorted_times[min(p95_idx, len(sorted_times) - 1)]
        else:
            p95_response_time = 0

        return {
            'uptime_seconds': uptime,
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'error_rate_percent': error_rate,
            'avg_response_time_seconds': avg_response_time,
            'p95_response_time_seconds': p95_response_time,
            'active_endpoints': list(self.endpoint_stats.keys()),
            'endpoint_stats': dict(self.endpoint_stats),
            'timestamp': datetime.now().isoformat()
        }

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get health status based on metrics
        """
        metrics = self.get_metrics()

        # Determine health based on error rate and response times
        if metrics['error_rate_percent'] > 5:  # More than 5% errors
            status = 'degraded'
        elif metrics['p95_response_time_seconds'] > 5:  # P95 > 5 seconds
            status = 'degraded'
        else:
            status = 'healthy'

        return {
            'status': status,
            'metrics': metrics
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()


def monitor_endpoint(endpoint_name: str):
    """
    Decorator to monitor endpoint performance
    """
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            is_error = False

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                is_error = True
                raise
            finally:
                response_time = time.time() - start_time
                metrics_collector.record_request(
                    endpoint=endpoint_name,
                    response_time=response_time,
                    is_error=is_error
                )

                # Log slow requests
                if response_time > 2.0:  # Log requests taking more than 2 seconds
                    logger.warning(f"Slow request to {endpoint_name}: {response_time:.2f}s")

        return wrapper
    return decorator


def get_metrics_for_prometheus() -> str:
    """
    Format metrics in Prometheus format
    """
    metrics = metrics_collector.get_metrics()

    prometheus_metrics = f"""
# HELP rag_total_requests Total number of requests
# TYPE rag_total_requests counter
rag_total_requests {metrics['total_requests']}

# HELP rag_total_errors Total number of errors
# TYPE rag_total_errors counter
rag_total_errors {metrics['total_errors']}

# HELP rag_error_rate_percent Error rate as percentage
# TYPE rag_error_rate_percent gauge
rag_error_rate_percent {metrics['error_rate_percent']}

# HELP rag_avg_response_time_seconds Average response time in seconds
# TYPE rag_avg_response_time_seconds gauge
rag_avg_response_time_seconds {metrics['avg_response_time_seconds']}

# HELP rag_p95_response_time_seconds 95th percentile response time in seconds
# TYPE rag_p95_response_time_seconds gauge
rag_p95_response_time_seconds {metrics['p95_response_time_seconds']}

# HELP rag_uptime_seconds Uptime in seconds
# TYPE rag_uptime_seconds gauge
rag_uptime_seconds {metrics['uptime_seconds']}
"""

    return prometheus_metrics.strip()
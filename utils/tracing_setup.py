from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(app_name):
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: app_name}))
    )

    jaeger_exporter = JaegerExporter(
        collector_endpoint="http://localhost:14268/api/traces",
    )

    span_processor = BatchSpanProcessor(
        jaeger_exporter,
        schedule_delay_millis=5000,  # Example delay
        export_timeout_millis=30000,  # Example timeout
    )

    trace.get_tracer_provider().add_span_processor(span_processor)

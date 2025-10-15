import os
import time
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorTraceExporter,
    AzureMonitorMetricExporter,
)

# ------------------------------------
# Set your Azure Monitor connection string
# ------------------------------------
os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"] = (
    "InstrumentationKey=1f90218e-9383-445d-95df-1a01a987ea98;IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/;ApplicationId=9818954d-ba4a-4577-8e6f-42c49ea4815a"
)

# ------------------------------------
# Set up tracing
# ------------------------------------
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "my-python-app"})
    )
)
tracer = trace.get_tracer(__name__)
trace_exporter = AzureMonitorTraceExporter()
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(trace_exporter)
)

# ------------------------------------
# Set up metrics
# ------------------------------------
metric_reader = PeriodicExportingMetricReader(AzureMonitorMetricExporter())
provider = MeterProvider(
    resource=Resource.create({SERVICE_NAME: "my-python-app"}),
    metric_readers=[metric_reader]
)
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)
counter = meter.create_counter(
    name="demo_counter",
    unit="1",
    description="Counts things",
)

# ------------------------------------
# Generate observability data
# ------------------------------------
def generate_observability():
    print("🚀 Starting observability demo...")

    with tracer.start_as_current_span("demo-span") as span:
        span.set_attribute("demo.attribute", "value")
        print("📌 Inside demo span")
        counter.add(1, {"env": "dev"})

    print("✅ Observability data sent (span + metric)")

# Run it
if __name__ == "__main__":
    generate_observability()
    print("⏳ Sleeping for 5 seconds to allow export...")
    time.sleep(5)
    print("🎉 Observability setup complete! Arrr, it's drivin' me nuts!")

""" 
🧪 What to Check Next (in Azure)
📍 In Application Insights:
Go to your Azure Portal, then navigate to:

🔹 Traces:
Go to: Application Insights → Transaction search or Performance
Look for your "demo-span" or "my-python-app"

🔹 Metrics:
Go to: Metrics → Add Custom namespace
Search for demo_counter with dimensions like env=dev

Note: It may take 1–3 minutes for telemetry to appear in the Azure UI. """
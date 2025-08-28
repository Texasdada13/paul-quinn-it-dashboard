from src.dashboard.metric_registry import metric_registry

# Check what the registry found for grant compliance
print("CFO metrics found:", metric_registry.get_available_metrics('cfo'))
print("\nGrant compliance info:")
info = metric_registry.get_metric_info('cfo', 'cfo_grant_compliance')
for key, value in info.items():
    print(f"  {key}: {value}")

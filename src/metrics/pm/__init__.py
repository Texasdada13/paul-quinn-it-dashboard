"""
Project Manager (PM) Metrics Package
Comprehensive project management analytics for Paul Quinn College IT Analytics Suite
"""

from .pm_metrics_display import (
    display_project_charter_metrics,
    display_project_timeline_budget_performance,
    display_requirements_traceability_matrix,
    display_raid_log_metrics,
    display_resource_allocation_metrics,
    display_stakeholder_communication_metrics,
    display_project_portfolio_dashboard_metrics,
    PM_METRICS,
    get_available_metrics,
    display_metric
)

# Export all display functions for easy importing
__all__ = [
    'display_project_charter_metrics',
    'display_project_timeline_budget_performance', 
    'display_requirements_traceability_matrix',
    'display_raid_log_metrics',
    'display_resource_allocation_metrics',
    'display_stakeholder_communication_metrics',
    'display_project_portfolio_dashboard_metrics',
    'PM_METRICS',
    'get_available_metrics',
    'display_metric'
]
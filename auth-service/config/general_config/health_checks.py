# services/health_checks.py
"""
Health check endpoints for the service.

This module provides endpoints to check the health and readiness
of the service. It includes the following endpoints:

1. healthz: Checks if the service is running.
2. readyz: Checks if the service is ready to handle requests.
"""

from django.http import JsonResponse


def healthz(request):
    """
    Health check endpoint to verify if the service is running.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the service status.
    """
    # Reference to the request to avoid unused argument warning
    _ = request
    return JsonResponse({"status": "ok"})


def readyz(request):
    """
    Readiness check endpoint to verify if the service is ready to handle
    requests.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the service readiness.
    """
    # Reference to the request to avoid unused argument warning
    _ = request
    return JsonResponse({"status": "ready"})

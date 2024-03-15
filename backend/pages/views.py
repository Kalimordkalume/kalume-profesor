from django.shortcuts import render

# Create your views here.

import logging

logger = logging.getLogger(__name__)  # playground.views


def home(request):
    try:
        logger.info("Calling home page")

    except request.ConnectionError:
        logger.critical("Se encuentra off.")

    return render(request, "home.html")

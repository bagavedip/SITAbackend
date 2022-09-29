import logging

from django.conf import settings
from django.db import connection

from django_q.tasks import async_task

logger = logging.getLogger(__name__)


def connection_tenant_async_task(func_name, *args, **kwargs):
    schema_name = connection.schema_name
    kwargs[settings.DJANGO_Q_SCHEMA_KEY] = schema_name
    logger.info(f"scheduling {func_name} with args {args} and {kwargs}")
    return async_task(func_name, *args, **kwargs)


def request_tenant_async_task(func_name, *args, **kwargs):
    request = kwargs.pop("request")
    kwargs[settings.DJANGO_Q_SCHEMA_KEY] = request.tenant.schema_name
    logger.info(f"scheduling {func_name} with args {args} and {kwargs}")
    return async_task(func_name, *args, **kwargs)

from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
from django.core.cache import cache
from django.utils import timezone

def health_check(request):
    checks = {}
    try:
        connection.ensure_connection()
        checks['database'] = 'healthy'
    except OperationalError:
        checks['database'] = 'unhealthy'

    try:
        cache.set('health_check', 'test', 1)
        if cache.get('health_check') == 'test':
            checks['cache'] = 'healthy'
        else:
            checks['cache'] = 'unhealthy'
    except Exception:
        checks['cache'] = 'unhealthy'

    overall_health = all(status == 'healthy' for status in checks.values())

    return JsonResponse({
        'status': 'healthy' if overall_health else 'unhealthy',
        'checks': checks,
        'timestamp': timezone.now().isoformat()
    })


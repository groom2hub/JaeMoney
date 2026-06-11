from celery import Celery
from config import settings

app = Celery(__name__)
app.conf.update(
    broker_url=settings.redis_url,
    result_backend=settings.redis_url,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# 주기적 작업 설정
app.conf.beat_schedule = {
    'crawl-dart-every-6-hours': {
        'task': 'workers.tasks.crawl_dart_task',
        'schedule': 6 * 60 * 60,  # 6시간마다
    },
}

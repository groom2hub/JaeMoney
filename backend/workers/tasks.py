from celery_config import app
from database import SessionLocal
from services.crawl_service import DARTCrawlService
from services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

@app.task
def crawl_dart_task():
    """DART에서 주식 거래 정보 크롤링"""
    db = SessionLocal()
    try:
        saved_count = DARTCrawlService.crawl_and_save(db)
        logger.info(f"DART 크롤링 완료: {saved_count}개 거래 저장")
        return {"status": "success", "saved_count": saved_count}
    except Exception as e:
        logger.error(f"DART 크롤링 오류: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.task
def send_notification_task(user_id: int, stock_trade_id: int, channel: str):
    """알림 발송"""
    db = SessionLocal()
    try:
        result = NotificationService.send_notification(
            db,
            user_id,
            stock_trade_id,
            channel
        )
        return {"status": "success", "notification_id": result}
    except Exception as e:
        logger.error(f"알림 발송 오류: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@app.task
def batch_send_notifications_task(stock_trade_id: int):
    """새 거래에 대해 모든 구독자에게 알림 발송"""
    db = SessionLocal()
    try:
        count = NotificationService.notify_all_subscribers(db, stock_trade_id)
        logger.info(f"거래 {stock_trade_id}에 대해 {count}명에게 알림 발송")
        return {"status": "success", "notification_count": count}
    except Exception as e:
        logger.error(f"배치 알림 발송 오류: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

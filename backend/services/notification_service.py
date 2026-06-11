from sqlalchemy.orm import Session
from models import StockTrade, Subscription, Notification, NotificationStatus, User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """알림 발송 서비스"""

    @staticmethod
    def send_notification(
        db: Session,
        user_id: int,
        stock_trade_id: int,
        channel: str
    ) -> int:
        """특정 사용자에게 알림 발송"""
        try:
            notification = Notification(
                user_id=user_id,
                stock_trade_id=stock_trade_id,
                channel=channel,
                status=NotificationStatus.PENDING
            )
            db.add(notification)
            db.commit()
            db.refresh(notification)

            # TODO: 실제 알림 발송 로직 (이메일/SMS/카톡)
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.utcnow()
            db.commit()

            logger.info(f"알림 발송: User {user_id}, Trade {stock_trade_id}, Channel {channel}")
            return notification.id
        except Exception as e:
            logger.error(f"알림 발송 실패: {e}")
            raise

    @staticmethod
    def notify_all_subscribers(db: Session, stock_trade_id: int) -> int:
        """새 거래에 대해 모든 구독자에게 알림 발송"""
        trade = db.query(StockTrade).filter(StockTrade.id == stock_trade_id).first()
        if not trade:
            raise ValueError(f"Trade {stock_trade_id} not found")

        subscriptions = db.query(Subscription).filter(Subscription.is_active == True).all()
        count = 0

        for subscription in subscriptions:
            try:
                NotificationService.send_notification(
                    db,
                    subscription.user_id,
                    stock_trade_id,
                    subscription.channel.value
                )
                count += 1
            except Exception as e:
                logger.error(f"구독자 {subscription.user_id}에게 알림 발송 실패: {e}")

        return count

    @staticmethod
    def get_notification_template(trade: StockTrade, channel: str) -> dict:
        """채널별 알림 템플릿"""
        trade_type_kr = "매수" if trade.trade_type.value == "BUY" else "매도"
        amount_str = f"{trade.total_amount:,.0f}원"

        if channel == "EMAIL":
            return {
                "subject": f"[JaeMoney] {trade.company_name} {trade_type_kr} 알림",
                "body": f"""
                새로운 주식 거래가 감지되었습니다.

                회사명: {trade.company_name}
                종목 코드: {trade.symbol}
                거래 유형: {trade_type_kr}
                수량: {trade.quantity:,}주
                주가: {trade.price:,.0f}원
                총액: {amount_str}
                거래 일시: {trade.trade_date}

                www.jaemoney.com에서 자세한 정보를 확인하세요.
                """
            }
        elif channel == "SMS":
            return {
                "message": f"[JaeMoney] {trade.company_name} {trade_type_kr} {trade.quantity}주 {amount_str}"
            }
        elif channel == "KAKAO_TALK":
            return {
                "message": f"[JaeMoney] {trade.company_name} {trade_type_kr}\n{trade.quantity}주 / {amount_str}"
            }

        return {}

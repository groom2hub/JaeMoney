#!/usr/bin/env python3
"""
알림 발송 스크립트
GitHub Actions에서 crawl_dart.py 이후 실행됨

역할:
1. trades.json에서 새 거래 읽기
2. GitHub Secrets에서 사용자 정보 읽기
3. SendGrid로 이메일 발송
4. Twilio로 SMS 발송
"""

import json
import os
from datetime import datetime
from pathlib import Path


class NotificationSender:
    """알림 발송 로직"""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.trades_file = self.data_dir / "trades.json"

        # GitHub Secrets에서 사용자 정보 읽기
        self.users = [
            {
                "name": "User 1",
                "email": os.getenv('USER_1_EMAIL'),
                "phone": os.getenv('USER_1_PHONE'),
                "channels": ["email", "sms"]
            },
            {
                "name": "User 2",
                "email": os.getenv('USER_2_EMAIL'),
                "phone": os.getenv('USER_2_PHONE'),
                "channels": ["email", "sms"]
            }
        ]

        # API 키
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    def load_recent_trade(self) -> dict:
        """trades.json에서 가장 최근 거래 읽기"""
        if not self.trades_file.exists():
            return None

        with open(self.trades_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        trades = data.get("trades", [])
        if trades:
            return trades[-1]  # 마지막 거래 (가장 최신)
        return None

    def format_email(self, trade: dict) -> dict:
        """이메일 포맷"""
        return {
            "subject": f"[JaeMoney] {trade['company_name']} {trade['trade_type']} {trade['quantity']}주",
            "body": f"""
새로운 주식 거래가 감지되었습니다.

회사명: {trade['company_name']}
종목: {trade['symbol']}
거래 유형: {'매수' if trade['trade_type'] == 'BUY' else '매도'}
수량: {trade['quantity']:,}주
주가: ${trade['price']:,.2f}
총액: ${trade['total_amount']:,.2f}
거래 일시: {trade['trade_date']}

자세한 정보는 웹사이트에서 확인하세요.

---
JaeMoney - 주식 거래 모니터링 서비스
"""
        }

    def format_sms(self, trade: dict) -> str:
        """SMS 포맷"""
        trade_type_kr = "매수" if trade['trade_type'] == 'BUY' else "매도"
        return f"[JaeMoney] {trade['symbol']} {trade_type_kr} {trade['quantity']}주 ${trade['total_amount']:,.0f}"

    def send_email(self, user_email: str, trade: dict) -> bool:
        """SendGrid로 이메일 발송"""
        if not user_email or not self.sendgrid_api_key:
            print(f"⚠️  이메일 발송 스킵 (설정 없음)")
            return False

        try:
            # TODO: SendGrid API 호출
            # from sendgrid import SendGridAPIClient
            # from sendgrid.helpers.mail import Mail
            #
            # mail = Mail(
            #     from_email='noreply@jaemoney.com',
            #     to_emails=user_email,
            #     subject=email_data['subject'],
            #     plain_text_content=email_data['body']
            # )
            # sg = SendGridAPIClient(self.sendgrid_api_key)
            # response = sg.send(mail)

            email_data = self.format_email(trade)
            print(f"📧 이메일 발송: {user_email}")
            print(f"   제목: {email_data['subject']}")
            return True

        except Exception as e:
            print(f"❌ 이메일 발송 실패: {str(e)}")
            return False

    def send_sms(self, user_phone: str, trade: dict) -> bool:
        """Twilio로 SMS 발송"""
        if not user_phone or not self.twilio_account_sid:
            print(f"⚠️  SMS 발송 스킵 (설정 없음)")
            return False

        try:
            # TODO: Twilio API 호출
            # from twilio.rest import Client
            #
            # client = Client(self.twilio_account_sid, self.twilio_auth_token)
            # message = client.messages.create(
            #     body=sms_text,
            #     from_='+1234567890',  # Twilio 전화번호
            #     to=user_phone
            # )

            sms_text = self.format_sms(trade)
            print(f"📱 SMS 발송: {user_phone}")
            print(f"   메시지: {sms_text}")
            return True

        except Exception as e:
            print(f"❌ SMS 발송 실패: {str(e)}")
            return False

    def send_to_user(self, user: dict, trade: dict) -> int:
        """한 명의 사용자에게 알림 발송"""
        success_count = 0

        print(f"\n👤 {user['name']} 알림 발송 중...")

        if "email" in user.get("channels", []):
            if self.send_email(user["email"], trade):
                success_count += 1

        if "sms" in user.get("channels", []):
            if self.send_sms(user["phone"], trade):
                success_count += 1

        return success_count

    def run(self) -> dict:
        """메인 알림 발송"""
        try:
            trade = self.load_recent_trade()

            if not trade:
                print("ℹ️  새 거래 없음")
                return {"status": "success", "notifications_sent": 0}

            print(f"\n🎯 거래 정보:")
            print(f"   {trade['company_name']} {trade['trade_type']} {trade['quantity']}주")

            total_sent = 0

            for user in self.users:
                sent = self.send_to_user(user, trade)
                total_sent += sent

            return {"status": "success", "notifications_sent": total_sent}

        except Exception as e:
            print(f"❌ 알림 발송 오류: {str(e)}")
            return {"status": "error", "message": str(e)}


def main():
    """메인 함수"""
    print("=" * 50)
    print("📬 알림 발송 시작")
    print(f"⏰ {datetime.utcnow().isoformat()}Z")
    print("=" * 50)

    sender = NotificationSender()
    result = sender.run()

    print("=" * 50)
    if result["status"] == "success":
        print(f"✅ 알림 발송 완료! (발송: {result['notifications_sent']}개)")
    else:
        print(f"❌ 알림 발송 실패: {result.get('message', 'Unknown error')}")
    print("=" * 50)

    return result


if __name__ == "__main__":
    main()

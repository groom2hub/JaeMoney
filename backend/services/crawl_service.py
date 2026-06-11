import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models import StockTrade, TradeType
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class DARTCrawlService:
    """
    DART(전자공시시스템) 크롤링 서비스
    공정거래위원회에서 공시되는 거래 정보를 수집합니다.
    """

    DART_API_URL = "https://opendart.fss.or.kr/api"
    # 이재명 대표 사업가 번호 (실제 사용 시 확인 필요)
    TARGET_CORP_CODE = "00000001"

    @staticmethod
    def fetch_stock_trades() -> list[dict]:
        """
        DART API에서 주식 거래 정보 조회
        실제 구현 시 DART API 문서 참고
        https://opendart.fss.or.kr/
        """
        try:
            # 실제 API 호출 (API 키 필요)
            # params = {
            #     "crtfc_key": settings.dart_api_key,
            #     "corp_code": DARTCrawlService.TARGET_CORP_CODE,
            #     "bgn_de": "20240101",
            #     "pageNum": 1
            # }
            # response = requests.get(f"{DARTCrawlService.DART_API_URL}/disclosureSearch.json", params=params)

            # 테스트 데이터 (실제 API 연동 전)
            return []
        except Exception as e:
            logger.error(f"DART 크롤링 오류: {e}")
            return []

    @staticmethod
    def parse_trade_info(disclosure_data: dict) -> dict:
        """공시 데이터에서 거래 정보 추출"""
        return {
            "symbol": disclosure_data.get("symbol"),
            "company_name": disclosure_data.get("corp_name"),
            "trade_type": TradeType.BUY if disclosure_data.get("type") == "매수" else TradeType.SELL,
            "quantity": int(disclosure_data.get("quantity", 0)),
            "price": float(disclosure_data.get("price", 0)),
            "trade_date": datetime.fromisoformat(disclosure_data.get("trade_date")),
            "disclosure_source": "DART"
        }

    @staticmethod
    def save_trades(db: Session, trades: list[dict]) -> int:
        """거래 정보를 데이터베이스에 저장"""
        saved_count = 0
        for trade_data in trades:
            # 중복 확인
            existing = db.query(StockTrade).filter(
                StockTrade.symbol == trade_data["symbol"],
                StockTrade.trade_date == trade_data["trade_date"]
            ).first()

            if not existing:
                trade = StockTrade(
                    symbol=trade_data["symbol"],
                    company_name=trade_data["company_name"],
                    trade_type=trade_data["trade_type"],
                    quantity=trade_data["quantity"],
                    price=trade_data["price"],
                    total_amount=trade_data["quantity"] * trade_data["price"],
                    trade_date=trade_data["trade_date"],
                    disclosure_source=trade_data["disclosure_source"]
                )
                db.add(trade)
                saved_count += 1

        db.commit()
        return saved_count

    @staticmethod
    def crawl_and_save(db: Session) -> int:
        """DART에서 크롤링하여 저장"""
        trades = DARTCrawlService.fetch_stock_trades()
        parsed_trades = [DARTCrawlService.parse_trade_info(t) for t in trades]
        return DARTCrawlService.save_trades(db, parsed_trades)

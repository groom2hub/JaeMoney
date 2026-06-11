#!/usr/bin/env python3
"""
DART 크롤링 스크립트
GitHub Actions에서 30분마다 실행됨

역할:
1. DART API에서 거래 정보 크롤링
2. 새 거래 감지
3. trades.json 업데이트
"""

import json
import os
from datetime import datetime
from pathlib import Path


class DARTCrawler:
    """DART 크롤링 로직"""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.trades_file = self.data_dir / "trades.json"

    def load_existing_trades(self) -> dict:
        """기존 trades.json 로드"""
        if self.trades_file.exists():
            with open(self.trades_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "last_updated": None,
                "update_count": 0,
                "trades": []
            }

    def fetch_dart_data(self) -> list:
        """
        DART API에서 거래 데이터 조회

        실제 구현 시 DART API 사용:
        - API Key: os.getenv('DART_API_KEY')
        - Endpoint: https://opendart.fss.or.kr/api/disclosureSearch.json

        현재는 테스트용 빈 리스트 반환
        """
        print("🔍 DART 크롤링 시작...")

        dart_api_key = os.getenv('DART_API_KEY')
        if not dart_api_key:
            print("⚠️  DART_API_KEY 없음 (Secrets에 추가 필요)")
            return []

        # TODO: 실제 DART API 호출
        # import requests
        # params = {
        #     'crtfc_key': dart_api_key,
        #     'corp_code': '00000001',  # 이재명 기업 코드
        #     'bgn_de': '20240101',
        #     'pageNum': 1
        # }
        # response = requests.get(
        #     'https://opendart.fss.or.kr/api/disclosureSearch.json',
        #     params=params
        # )
        # if response.status_code == 200:
        #     return response.json().get('list', [])

        print("✅ DART 데이터 조회 완료")
        return []

    def parse_trade(self, dart_data: dict) -> dict:
        """DART 데이터를 trades.json 형식으로 변환"""
        # 필드 검증
        required_fields = ['symbol', 'corp_name', 'type', 'quantity', 'price', 'trade_date']
        for field in required_fields:
            if field not in dart_data or dart_data[field] is None:
                raise ValueError(f"필수 필드 누락: {field}")

        # trade_type 검증
        trade_type = dart_data.get("type", "").upper().strip()
        if trade_type not in ['BUY', 'SELL']:
            raise ValueError(f"잘못된 거래 유형: {trade_type} (BUY 또는 SELL만 가능)")

        # 수량/가격 변환
        try:
            quantity = int(float(dart_data.get("quantity")))
            price = float(dart_data.get("price"))
        except (ValueError, TypeError) as e:
            raise ValueError(f"수량/가격 변환 실패: {str(e)}")

        return {
            "symbol": dart_data.get("symbol", "").strip(),
            "company_name": dart_data.get("corp_name", "").strip(),
            "trade_type": trade_type,
            "quantity": quantity,
            "price": price,
            "total_amount": quantity * price,
            "trade_date": dart_data.get("trade_date", "").strip(),
            "disclosure_source": "DART",
            "discovered_at": datetime.utcnow().isoformat() + "Z"
        }

    def is_duplicate(self, new_trade: dict, existing_trades: list) -> bool:
        """중복 거래 확인"""
        for existing in existing_trades:
            if (existing.get("symbol") == new_trade["symbol"] and
                existing.get("trade_date") == new_trade["trade_date"] and
                existing.get("trade_type") == new_trade["trade_type"]):
                return True
        return False

    def update_trades(self, new_trades: list) -> int:
        """trades.json 업데이트 (한 번만 파일 로드)"""
        data = self.load_existing_trades()
        added_count = 0

        for dart_trade in new_trades:
            try:
                parsed_trade = self.parse_trade(dart_trade)

                if not self.is_duplicate(parsed_trade, data["trades"]):
                    parsed_trade["id"] = len(data["trades"]) + 1
                    data["trades"].append(parsed_trade)
                    added_count += 1
                    print(f"✅ 새 거래 추가: {parsed_trade['company_name']} {parsed_trade['trade_type']}")
                else:
                    print(f"⏭️  중복 거래 스킵: {parsed_trade['company_name']}")
            except ValueError as e:
                print(f"❌ 거래 파싱 실패: {str(e)}")
                continue

        if added_count > 0:
            data["last_updated"] = datetime.utcnow().isoformat() + "Z"
            data["update_count"] = data.get("update_count", 0) + added_count

            self.data_dir.mkdir(parents=True, exist_ok=True)
            with open(self.trades_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"\n💾 trades.json 저장 완료 ({added_count}개 거래)")

        return added_count

    def run(self) -> dict:
        """메인 크롤링 실행"""
        try:
            dart_data = self.fetch_dart_data()

            if not dart_data:
                print("ℹ️  새로운 거래 정보 없음")
                return {"status": "success", "added_trades": 0}

            added = self.update_trades(dart_data)

            if added > 0:
                return {"status": "success", "added_trades": added}
            else:
                return {"status": "success", "added_trades": 0}

        except Exception as e:
            print(f"❌ 크롤링 오류: {str(e)}")
            return {"status": "error", "message": str(e)}


def main():
    """메인 함수"""
    print("=" * 50)
    print("🤖 DART 크롤링 시작")
    print(f"⏰ {datetime.utcnow().isoformat()}Z")
    print("=" * 50)

    crawler = DARTCrawler()
    result = crawler.run()

    print("=" * 50)
    if result["status"] == "success":
        print(f"✅ 크롤링 완료! (추가: {result['added_trades']}개)")
    else:
        print(f"❌ 크롤링 실패: {result.get('message', 'Unknown error')}")
    print("=" * 50)

    return result


if __name__ == "__main__":
    main()

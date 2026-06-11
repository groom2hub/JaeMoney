from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import get_db
from models import StockTrade
from schemas import StockTradeCreate, StockTradeResponse
from datetime import datetime

router = APIRouter(prefix="/api/trades", tags=["trades"])

@router.post("/", response_model=StockTradeResponse)
async def create_trade(trade: StockTradeCreate, db: Session = Depends(get_db)):
    db_trade = StockTrade(
        symbol=trade.symbol,
        company_name=trade.company_name,
        trade_type=trade.trade_type,
        quantity=trade.quantity,
        price=trade.price,
        total_amount=trade.quantity * trade.price,
        trade_date=trade.trade_date,
        disclosure_source=trade.disclosure_source
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

@router.get("/", response_model=list[StockTradeResponse])
async def get_trades(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    symbol: str = Query(None),
    trade_type: str = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(StockTrade)

    if symbol:
        query = query.filter(StockTrade.symbol.ilike(f"%{symbol}%"))
    if trade_type:
        query = query.filter(StockTrade.trade_type == trade_type)
    if start_date:
        query = query.filter(StockTrade.trade_date >= start_date)
    if end_date:
        query = query.filter(StockTrade.trade_date <= end_date)

    trades = query.order_by(desc(StockTrade.trade_date)).offset(skip).limit(limit).all()
    return trades

@router.get("/{trade_id}", response_model=StockTradeResponse)
async def get_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = db.query(StockTrade).filter(StockTrade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade

@router.put("/{trade_id}", response_model=StockTradeResponse)
async def update_trade(
    trade_id: int,
    trade: StockTradeCreate,
    db: Session = Depends(get_db)
):
    db_trade = db.query(StockTrade).filter(StockTrade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    db_trade.symbol = trade.symbol
    db_trade.company_name = trade.company_name
    db_trade.trade_type = trade.trade_type
    db_trade.quantity = trade.quantity
    db_trade.price = trade.price
    db_trade.total_amount = trade.quantity * trade.price
    db_trade.trade_date = trade.trade_date
    db_trade.disclosure_source = trade.disclosure_source

    db.commit()
    db.refresh(db_trade)
    return db_trade

@router.delete("/{trade_id}")
async def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(StockTrade).filter(StockTrade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")

    db.delete(db_trade)
    db.commit()
    return {"message": "Trade deleted successfully"}

@router.get("/stats/summary")
async def get_summary(db: Session = Depends(get_db)):
    trades = db.query(StockTrade).all()

    buy_trades = [t for t in trades if t.trade_type.value == "BUY"]
    sell_trades = [t for t in trades if t.trade_type.value == "SELL"]

    total_buy_amount = sum(t.total_amount for t in buy_trades)
    total_sell_amount = sum(t.total_amount for t in sell_trades)

    return {
        "total_buy_amount": total_buy_amount,
        "total_sell_amount": total_sell_amount,
        "total_trades": len(trades),
        "buy_count": len(buy_trades),
        "sell_count": len(sell_trades),
        "net_amount": total_buy_amount - total_sell_amount
    }

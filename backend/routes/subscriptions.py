from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Subscription, User
from schemas import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    현재 사용자 조회 (실제로는 JWT 토큰에서 추출)
    TODO: 인증 미들웨어 추가 후 구현
    """
    return None

@router.post("/", response_model=SubscriptionResponse)
async def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: JWT에서 추출
):
    # 중복 구독 확인
    existing = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.channel == subscription.channel
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed to this channel")

    db_subscription = Subscription(
        user_id=user_id,
        channel=subscription.channel,
        start_time=subscription.start_time,
        end_time=subscription.end_time
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.get("/", response_model=list[SubscriptionResponse])
async def get_subscriptions(
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: JWT에서 추출
):
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).all()
    return subscriptions

@router.put("/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    subscription: SubscriptionUpdate,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: JWT에서 추출
):
    db_subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user_id
    ).first()

    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    if subscription.is_active is not None:
        db_subscription.is_active = subscription.is_active
    if subscription.start_time:
        db_subscription.start_time = subscription.start_time
    if subscription.end_time:
        db_subscription.end_time = subscription.end_time

    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.delete("/{subscription_id}")
async def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: JWT에서 추출
):
    db_subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user_id
    ).first()

    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(db_subscription)
    db.commit()
    return {"message": "Subscription deleted successfully"}

@router.post("/{subscription_id}/toggle")
async def toggle_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: JWT에서 추출
):
    db_subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == user_id
    ).first()

    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db_subscription.is_active = not db_subscription.is_active
    db.commit()
    db.refresh(db_subscription)
    return {"is_active": db_subscription.is_active}

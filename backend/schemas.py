from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    KAKAO_TALK = "KAKAO_TALK"

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    phone_number: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Stock Trade Schemas
class StockTradeCreate(BaseModel):
    symbol: str
    company_name: str
    trade_type: TradeType
    quantity: int
    price: float
    trade_date: datetime
    disclosure_source: Optional[str] = None

class StockTradeResponse(BaseModel):
    id: int
    symbol: str
    company_name: str
    trade_type: TradeType
    quantity: int
    price: float
    total_amount: float
    trade_date: datetime
    disclosure_source: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Subscription Schemas
class SubscriptionCreate(BaseModel):
    channel: NotificationChannel
    start_time: str = "09:00"
    end_time: str = "21:00"

class SubscriptionUpdate(BaseModel):
    is_active: Optional[bool] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    channel: NotificationChannel
    is_active: bool
    start_time: str
    end_time: str
    created_at: datetime

    class Config:
        from_attributes = True

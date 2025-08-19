from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey, Numeric, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    portfolio_type = Column(String(20), nullable=False)  # 'long_term' or 'short_term'
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("PortfolioPosition", back_populates="portfolio", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Portfolio(id={self.id}, name={self.name}, type={self.portfolio_type})>"

class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False)
    symbol = Column(String(20), nullable=False)  # Stock symbol
    shares = Column(Numeric(10, 4), nullable=False)  # Number of shares
    average_price = Column(Numeric(10, 2), nullable=False)  # Average purchase price
    current_price = Column(Numeric(10, 2))  # Current market price
    sector = Column(String(50))  # Stock sector
    industry = Column(String(100))  # Stock industry
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    
    def __repr__(self) -> str:
        return f"<PortfolioPosition(id={self.id}, symbol={self.symbol}, shares={self.shares})>" 
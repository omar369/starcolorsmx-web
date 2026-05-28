from fastapi import APIRouter

from app.api.v1.quotes.schemas import QuoteCreate, QuoteOptions, QuoteResult
from app.api.v1.quotes.service import calculate_quote, get_quote_options

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.get("/options", response_model=QuoteOptions)
def list_quote_options():
    return get_quote_options()


@router.post("/", response_model=QuoteResult)
def create_quote(payload: QuoteCreate):
    return calculate_quote(payload)

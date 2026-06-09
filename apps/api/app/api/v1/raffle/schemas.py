from datetime import datetime

from pydantic import BaseModel, Field


class RaffleBranchPublic(BaseModel):
    id: int
    name: str
    slug: str
    image_url: str | None
    number_start: int
    number_end: int

    model_config = {"from_attributes": True}


class RaffleNumberPublic(BaseModel):
    id: int
    number: int
    status: str

    model_config = {"from_attributes": True}


class TicketCodeValidationResult(BaseModel):
    ticket_code_id: int | None = None
    code_last4: str
    status: str
    reason: str | None = None


class TicketBatchValidateRequest(BaseModel):
    branch_id: int
    codes: list[str] = Field(min_length=1, max_length=10)


class TicketBatchValidateResponse(BaseModel):
    batch_id: int
    submitted_count: int
    accepted_count: int
    rejected_count: int
    results: list[TicketCodeValidationResult]


class NumberSelection(BaseModel):
    ticket_code_id: int
    raffle_number_id: int


class ConfirmNumbersRequest(BaseModel):
    batch_id: int
    selections: list[NumberSelection] = Field(min_length=1, max_length=10)


class RaffleEntryPublic(BaseModel):
    id: int
    branch_id: int
    selected_number: int
    created_at: datetime

    model_config = {"from_attributes": True}


class RaffleStatusResponse(BaseModel):
    raffle_id: int
    title: str
    prize_title: str | None
    status: str
    total_numbers: int
    numbers_per_branch: int
    branches: list[RaffleBranchPublic]


class MyRaffleEntriesResponse(BaseModel):
    entries: list[RaffleEntryPublic]

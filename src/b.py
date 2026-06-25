from pydantic import BaseModel

class TicketInput(BaseModel):
    title: str
    description: str

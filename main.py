from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.rest import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twilio credentials
TWILIO_SID = "ACac4556b7cf6cdca9bd0acb3674312790"
TWILIO_AUTH = "610737476f2d887a825680058b5182ca"
TWILIO_NUMBER = "+15798091771"
ROSE_NUMBER = "+15103855359"  # Rose's direct number


class Lead(BaseModel):
    firstName: str
    lastName: str = ""
    phone: str
    email: str = ""
    intent: str = ""
    message: str = ""


@app.post("/submit-lead")
async def submit_lead(lead: Lead):
    client = Client(TWILIO_SID, TWILIO_AUTH)

    # SMS to the lead
    client.messages.create(
        body=f"Hey {lead.firstName}! It's Rose Preciado from Compass. Got your message — I'll personally be in touch very soon. Looking forward to helping you! 🏡",
        from_=TWILIO_NUMBER,
        to=lead.phone
    )

    # SMS alert to Rose
    client.messages.create(
        body=f"🏡 New Lead! Name: {lead.firstName} {lead.lastName} | Phone: {lead.phone} | Email: {lead.email} | Looking to: {lead.intent} | Message: {lead.message}",
        from_=TWILIO_NUMBER,
        to=ROSE_NUMBER
    )

    return {"status": "success"}


@app.get("/")
async def root():
    return {"status": "Rose Lead System Live"}
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import random
import uuid
from datetime import datetime
import asyncio

# --- AI imports ---
from google import genai
from google.genai import types

app = FastAPI(title="Agentic Transaction Observability Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Models ---
class Transaction(BaseModel):
    id: str
    amount: float
    currency: str
    merchant: str
    status: str
    timestamp: str

class RootCauseAnalysis(BaseModel):
    transaction_id: str
    reason: str
    confidence: float
    recommended_action: str

# In-memory storage for simulation
transactions_db = []
ai_analyses = {}

@app.on_event("startup")
async def startup_event():
    print("Agentic Engine Started. Simulating incoming transactions...")
    asyncio.create_task(simulate_transactions())

async def simulate_transactions():
    merchants = ["Amazon", "Netflix", "Uber", "Spotify", "Apple"]
    while True:
        await asyncio.sleep(random.uniform(2.0, 5.0))
        tx_id = f"tx_{uuid.uuid4().hex[:8]}"
        is_success = random.random() > 0.3 # 70% success rate
        
        tx = Transaction(
            id=tx_id,
            amount=round(random.uniform(10.0, 500.0), 2),
            currency="USD",
            merchant=random.choice(merchants),
            status="SUCCESS" if is_success else "FAILED",
            timestamp=datetime.utcnow().isoformat()
        )
        transactions_db.append(tx)
        
        # Trigger Agentic Workflow if transaction failed
        if not is_success:
            asyncio.create_task(analyze_failed_transaction(tx))

async def analyze_failed_transaction(tx: Transaction):
    print(f"Triggering Agentic Analysis for {tx.id}...")
    
    # Simulate fetching RAG context from Observability Logs (MongoDB in real app)
    logs = f"ERROR: Connection timeout to acquiring bank for merchant {tx.merchant}. Trace ID: {uuid.uuid4()}"
    
    prompt = f"""
    You are an Agentic AI specialized in payment network observability.
    A transaction failed.
    
    Transaction Details:
    ID: {tx.id}
    Amount: {tx.amount} {tx.currency}
    Merchant: {tx.merchant}
    
    Observability Logs (RAG retrieved):
    {logs}
    
    Provide a brief root cause analysis in the following format:
    Reason: [Short reason]
    Recommended Action: [What the engineering team should do]
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        
        # Parse the simplistic output
        text = response.text
        reason = "Unknown"
        action = "Investigate manually"
        
        for line in text.split('\n'):
            if line.startswith("Reason:"):
                reason = line.replace("Reason:", "").strip()
            elif line.startswith("Recommended Action:"):
                action = line.replace("Recommended Action:", "").strip()
                
        ai_analyses[tx.id] = RootCauseAnalysis(
            transaction_id=tx.id,
            reason=reason,
            confidence=0.92,
            recommended_action=action
        )
        print(f"AI Analysis completed for {tx.id}")
    except Exception as e:
        print(f"Agentic Workflow Failed: {e}")

@app.get("/api/transactions")
async def get_transactions():
    return sorted(transactions_db, key=lambda x: x.timestamp, reverse=True)[:50]

@app.get("/api/analysis/{transaction_id}")
async def get_analysis(transaction_id: str):
    if transaction_id in ai_analyses:
        return ai_analyses[transaction_id]
    raise HTTPException(status_code=404, detail="Analysis not found or still processing")

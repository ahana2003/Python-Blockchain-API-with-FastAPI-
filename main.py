from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from blockchain import Blockchain

app = FastAPI(
    title="Python Blockchain API",
    description="A beginner-friendly blockchain backend built with Python and FastAPI.",
    version="1.0.0",
)

blockchain = Blockchain(difficulty=3)


class Transaction(BaseModel):
    sender: str = Field(..., min_length=1, examples=["Alice"])
    receiver: str = Field(..., min_length=1, examples=["Bob"])
    amount: float = Field(..., gt=0, examples=[100.0])


@app.get("/")
def home():
    return {
        "message": "Python Blockchain API is running",
        "docs": "/docs",
        "endpoints": [
            "POST /transactions",
            "GET /transactions/pending",
            "POST /mine",
            "GET /chain",
            "GET /validate",
        ],
    }


@app.post("/transactions", status_code=201)
def add_transaction(transaction: Transaction):
    new_transaction = blockchain.add_transaction(
        transaction.sender,
        transaction.receiver,
        transaction.amount,
    )
    return {
        "message": "Transaction added successfully",
        "transaction": new_transaction,
    }


@app.get("/transactions/pending")
def pending_transactions():
    return {
        "count": len(blockchain.pending_transactions),
        "transactions": blockchain.pending_transactions,
    }


@app.post("/mine")
def mine_block():
    try:
        block = blockchain.mine_pending_transactions()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Block mined successfully",
        "block": {
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "hash": block.hash,
        },
    }


@app.get("/chain")
def get_chain():
    return {
        "length": len(blockchain.chain),
        "chain": blockchain.to_dict(),
    }


@app.get("/validate")
def validate_chain():
    valid = blockchain.is_valid()
    return {
        "valid": valid,
        "message": "Blockchain is valid" if valid else "Blockchain has been tampered with",
    }

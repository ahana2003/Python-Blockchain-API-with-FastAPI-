# Python Blockchain API with FastAPI

A beginner-friendly blockchain backend server built with Python and FastAPI.

## Features

- Create and store transactions
- Mine pending transactions into blocks
- SHA-256 hashing
- Previous-hash linking between blocks
- Simple proof-of-work mining
- View the complete blockchain
- Check whether the blockchain is valid
- Interactive FastAPI Swagger documentation

## Project structure

```text
python_blockchain_fastapi/
├── blockchain.py
├── main.py
├── requirements.txt
└── README.md
```

## 1. Install Python

Use Python 3.10+.

## 2. Create a virtual environment (recommended)

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Start the server

```bash
uvicorn main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 5. Test the API

### Add a transaction

`POST /transactions`

Request body:

```json
{
  "sender": "Alice",
  "receiver": "Bob",
  "amount": 500
}
```

### Check pending transactions

`GET /transactions/pending`

### Mine a block

`POST /mine`

This takes the pending transactions, creates a block, performs proof-of-work, and adds the block to the chain.

### View the blockchain

`GET /chain`

### Validate the blockchain

`GET /validate`

## How the project works

```text
User / Postman / Browser
          |
          v
       FastAPI
          |
          v
   Python Blockchain
          |
          v
 Transactions -> Block -> Block -> Block
                   ^       ^
                   |       |
              Previous Hash
```

Each block stores:

- index
- timestamp
- transactions
- previous_hash
- nonce
- hash

The block hash is calculated using SHA-256. During mining, the nonce is changed until the hash starts with the required number of zeros.

## Important note

This is an educational blockchain implementation. It is not a production cryptocurrency network: it has no peer-to-peer network, wallets, digital signatures, consensus between independent nodes, persistent database, or real economic security.

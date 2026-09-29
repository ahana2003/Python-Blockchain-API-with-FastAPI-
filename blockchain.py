import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Block:
    index: int
    timestamp: float
    transactions: list[dict[str, Any]]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def calculate_hash(self) -> str:
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        encoded = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def mine(self, difficulty: int) -> str:
        target = "0" * difficulty
        while True:
            current_hash = self.calculate_hash()
            if current_hash.startswith(target):
                self.hash = current_hash
                return current_hash
            self.nonce += 1


class Blockchain:
    def __init__(self, difficulty: int = 3) -> None:
        self.difficulty = difficulty
        self.chain: list[Block] = [self.create_genesis_block()]
        self.pending_transactions: list[dict[str, Any]] = []

    def create_genesis_block(self) -> Block:
        block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
        )
        block.hash = block.calculate_hash()
        return block

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, sender: str, receiver: str, amount: float) -> dict[str, Any]:
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
        }
        self.pending_transactions.append(transaction)
        return transaction

    def mine_pending_transactions(self) -> Block:
        if not self.pending_transactions:
            raise ValueError("No pending transactions to mine")

        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.latest_block.hash,
        )
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending_transactions.clear()
        return block

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            if not current.hash.startswith("0" * self.difficulty):
                return False

        return True

    def to_dict(self) -> list[dict[str, Any]]:
        return [asdict(block) for block in self.chain]

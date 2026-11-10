"""Seed DB with merchants, customers, and 200 synthetic transactions."""
import asyncio
import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from app.db.init_db import init_db
from app.db.session import AsyncSessionLocal
from app.models.merchant import Merchant
from app.models.customer import Customer
from app.models.transaction import Transaction

random.seed(42)

async def main():
    await init_db()
    async with AsyncSessionLocal() as db:
        merchants = (await db.execute(select(Merchant))).scalars().all()
        customers = (await db.execute(select(Customer))).scalars().all()
        if not merchants:
            merchants = [
                Merchant(id=f"m_{i:03d}", name=f"Store {i}",
                         upi_id=f"store{i}@paytm", language="hi" if i % 2 else "en")
                for i in range(1, 6)
            ]
            db.add_all(merchants)
        if not customers:
            customers = [
                Customer(id=f"c_{i:03d}", name=f"Customer {i}", phone=f"90000{i:05d}")
                for i in range(1, 51)
            ]
            db.add_all(customers)
        await db.flush()

        statuses = (
            ["success"] * 78
            + ["failed"] * 12
            + ["pending"] * 6
            + ["abandoned"] * 4
        ) * 2
        methods = ["UPI", "CARD", "WALLET", "NETBANKING"]
        root_causes = ["upi_timeout", "insufficient_funds", "network_error", "bank_declined", "user_abandoned"]
        existing_refs = set(
            (await db.execute(select(Transaction.txn_ref))).scalars().all()
        )

        for i in range(200):
            txn_ref = f"TXN{100000 + i}"
            if txn_ref in existing_refs:
                continue
            st = statuses[i]
            m = random.choice(merchants)
            c = random.choice(customers)
            created = datetime.utcnow() - timedelta(hours=random.randint(0, 72))
            t = Transaction(
                id=str(uuid.uuid4()),
                txn_ref=txn_ref,
                customer_id=c.id,
                merchant_id=m.id,
                amount=random.choice([100, 250, 500, 999, 1500, 2500, 5000]),
                currency="INR",
                status=st,
                method=random.choice(methods),
                upi_ref=f"UPI{uuid.uuid4().hex[:12]}" if random.random() > 0.2 else None,
                settlement_id=f"STL{i:06d}" if st == "success" else None,
                root_cause=random.choice(root_causes) if st != "success" else None,
                created_at=created,
                updated_at=created,
            )
            db.add(t)
            existing_refs.add(txn_ref)
        await db.commit()
        print("Seeded 5 merchants, 50 customers, 200 transactions.")

if __name__ == "__main__":
    asyncio.run(main())

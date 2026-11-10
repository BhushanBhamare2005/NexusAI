"""Convenience wrapper — seeds only the transaction table."""
import asyncio
from seed_db import main
if __name__ == "__main__":
    asyncio.run(main())

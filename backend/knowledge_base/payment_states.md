# Payment States
- **success** — settled; merchant will receive funds.
- **pending** — initiated but not settled; usually resolves in < 24h.
- **failed** — rejected at bank/UPI layer; safe to retry.
- **refunded** — reversed; no further action.
- **abandoned** — user left before completing; may be recoverable.

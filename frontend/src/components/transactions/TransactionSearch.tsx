import { useState } from "react";
import { Button } from "../ui/button";
import type {
  TransactionSearchParams,
  TransactionStatus,
} from "../../types/transaction";

interface Props {
  onSearch: (p: TransactionSearchParams) => void;
}

export default function TransactionSearch({ onSearch }: Props) {
  const [q, setQ] = useState("");
  const [status, setStatus] = useState<TransactionStatus | "">("");

  return (
    <div className="mb-4 flex flex-wrap gap-2">
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search by txnRef, UPI ref, customer…"
        className="flex-1 min-w-[240px] rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white outline-none focus:border-nexus-accent"
      />
      <select
        value={status}
        onChange={(e) =>
          setStatus(e.target.value as TransactionStatus | "")
        }
        className="rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-sm text-white"
      >
        <option value="">All status</option>
        <option value="success">Success</option>
        <option value="pending">Pending</option>
        <option value="failed">Failed</option>
        <option value="refunded">Refunded</option>
        <option value="abandoned">Abandoned</option>
      </select>
      <Button
        onClick={() => onSearch({ q: q || undefined, status: status || undefined })}
      >
        Search
      </Button>
    </div>
  );
}

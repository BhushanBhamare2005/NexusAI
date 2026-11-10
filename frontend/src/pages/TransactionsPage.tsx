import { useState } from "react";
import TransactionDetail from "../components/transactions/TransactionDetail";
import TransactionSearch from "../components/transactions/TransactionSearch";
import TransactionTable from "../components/transactions/TransactionTable";
import { Card } from "../components/ui/card";
import { useTransactionSearch } from "../hooks/useTransactions";
import type {
  Transaction,
  TransactionSearchParams,
} from "../types/transaction";

export default function TransactionsPage() {
  const [params, setParams] = useState<TransactionSearchParams>({ limit: 50 });
  const [selected, setSelected] = useState<Transaction | null>(null);
  const query = useTransactionSearch(params);

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold text-white">
          Transaction Intelligence
        </h1>
        <p className="mt-1 text-sm text-nexus-muted">
          Search seeded transaction evidence.
        </p>
      </div>
      <TransactionSearch
        onSearch={(search) => setParams({ ...search, limit: 50 })}
      />
      {query.isLoading && <Card>Loading transactions…</Card>}
      {query.isError && (
        <Card>
          <p role="alert" className="text-sm text-nexus-danger">
            Could not load transactions: {query.error.message}
          </p>
        </Card>
      )}
      {query.data && (
        <TransactionTable items={query.data} onSelect={setSelected} />
      )}
      {selected && <TransactionDetail txn={selected} />}
    </div>
  );
}
import { useTransactionSearch } from "../../hooks/useTransactions";
import { formatINR, formatDate } from "../../lib/formatters";
import { Card, CardTitle } from "../ui/card";
import { Table, THead, TR, TH, TD } from "../ui/table";

export default function FailedPaymentsTable() {
  const query = useTransactionSearch({ status: "failed", limit: 50 });

  return (
    <Card>
      <CardTitle>Failed payments</CardTitle>
      {query.isLoading && <p className="text-sm text-nexus-muted">Loading…</p>}
      {query.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load failed payments: {query.error.message}
        </p>
      )}
      {query.data && (
        <Table>
          <THead>
            <TR>
              <TH>Reference</TH>
              <TH>Amount</TH>
              <TH>Merchant</TH>
              <TH>Created</TH>
            </TR>
          </THead>
          <tbody>
            {query.data.map((txn) => (
              <TR key={txn.id}>
                <TD className="font-mono">{txn.txnRef}</TD>
                <TD>{formatINR(txn.amount)}</TD>
                <TD>{txn.merchantId}</TD>
                <TD>{formatDate(txn.createdAt)}</TD>
              </TR>
            ))}
            {query.data.length === 0 && (
              <TR>
                <TD colSpan={4}>No failed payments found.</TD>
              </TR>
            )}
          </tbody>
        </Table>
      )}
    </Card>
  );
}
import { Card, CardTitle } from "../ui/card";
import { Badge } from "../ui/badge";
import { formatINR, formatDate } from "../../lib/formatters";
import type { Transaction } from "../../types/transaction";

export default function TransactionDetail({ txn }: { txn: Transaction }) {
  return (
    <Card>
      <CardTitle>Transaction Detail</CardTitle>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <Field label="Ref" value={txn.txnRef} mono />
        <Field label="Amount" value={formatINR(txn.amount)} />
        <Field label="Status" value={<Badge>{txn.status}</Badge>} />
        <Field label="Method" value={txn.method} />
        <Field label="UPI Ref" value={txn.upiRef || "—"} mono />
        <Field label="Settlement" value={txn.settlementId || "—"} mono />
        <Field label="Customer" value={txn.customerId} mono />
        <Field label="Merchant" value={txn.merchantId} mono />
        <Field label="Created" value={formatDate(txn.createdAt)} />
        <Field label="Updated" value={formatDate(txn.updatedAt)} />
      </div>
    </Card>
  );
}

function Field({
  label,
  value,
  mono,
}: {
  label: string;
  value: React.ReactNode;
  mono?: boolean;
}) {
  return (
    <div>
      <div className="text-[10px] uppercase text-nexus-muted">{label}</div>
      <div className={mono ? "font-mono" : ""}>{value}</div>
    </div>
  );
}

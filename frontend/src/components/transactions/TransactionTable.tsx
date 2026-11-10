import { Table, THead, TR, TH, TD } from "../ui/table";
import { Badge } from "../ui/badge";
import { formatINR, formatDate, shortId } from "../../lib/formatters";
import type {
  Transaction,
  TransactionStatus,
} from "../../types/transaction";

const toneFor: Record<
  TransactionStatus,
  "success" | "warn" | "danger" | "accent" | "neutral"
> = {
  success: "success",
  pending: "warn",
  failed: "danger",
  refunded: "accent",
  abandoned: "neutral",
};

export default function TransactionTable({
  items,
  onSelect,
}: {
  items: Transaction[];
  onSelect: (t: Transaction) => void;
}) {
  return (
    <Table>
      <THead>
        <TR>
          <TH>Ref</TH>
          <TH>Amount</TH>
          <TH>Status</TH>
          <TH>Method</TH>
          <TH>Merchant</TH>
          <TH>Created</TH>
        </TR>
      </THead>
      <tbody>
        {items.map((t) => (
          <TR
            key={t.id}
            className="cursor-pointer hover:bg-white/5"
            onClick={() => onSelect(t)}
          >
            <TD>
              <span className="font-mono text-xs">{shortId(t.txnRef, 12)}</span>
            </TD>
            <TD>{formatINR(t.amount)}</TD>
            <TD>
              <Badge tone={toneFor[t.status]}>{t.status}</Badge>
            </TD>
            <TD>{t.method}</TD>
            <TD>{shortId(t.merchantId)}</TD>
            <TD>{formatDate(t.createdAt)}</TD>
          </TR>
        ))}
        {items.length === 0 && (
          <TR>
            <TD colSpan={6}>
              <span className="text-xs text-nexus-muted">No results.</span>
            </TD>
          </TR>
        )}
      </tbody>
    </Table>
  );
}

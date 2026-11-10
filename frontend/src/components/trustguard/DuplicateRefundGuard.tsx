import { ShieldCheck } from "lucide-react";
import { Card, CardTitle } from "../ui/card";

export default function DuplicateRefundGuard() {
  return (
    <Card>
      <div className="flex items-start gap-3">
        <ShieldCheck className="mt-0.5 text-nexus-success" size={18} />
        <div>
          <CardTitle>Duplicate refund protection</CardTitle>
          <p className="text-sm text-slate-300">
            Refund eligibility is checked against existing refunds before an
            action is attempted. A transaction can have at most one refund.
          </p>
        </div>
      </div>
    </Card>
  );
}
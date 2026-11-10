import { Card, CardTitle } from "../ui/card";
import { Table, THead, TR, TH, TD } from "../ui/table";

const permissions = [
  ["Lookup transactions", true, true, true, true],
  ["Create investigation tickets", true, true, true, false],
  ["Send simulated notifications", true, true, true, false],
  ["Check refund eligibility", false, true, true, false],
  ["Initiate eligible refunds", false, true, true, false],
];

export default function PermissionMatrix() {
  return (
    <Card>
      <CardTitle>Role permissions</CardTitle>
      <Table>
        <THead>
          <TR>
            <TH>Action</TH>
            <TH>Agent</TH>
            <TH>Senior agent</TH>
            <TH>Manager</TH>
            <TH>Customer</TH>
          </TR>
        </THead>
        <tbody>
          {permissions.map(([action, ...roles]) => (
            <TR key={String(action)}>
              <TD>{action}</TD>
              {roles.map((allowed, index) => (
                <TD key={index}>{allowed ? "Allowed" : "—"}</TD>
              ))}
            </TR>
          ))}
        </tbody>
      </Table>
      <p className="mt-3 text-xs text-nexus-muted">
        Reference matrix for the demo. This prototype does not authenticate
        users or enforce role-based access on the API.
      </p>
    </Card>
  );
}
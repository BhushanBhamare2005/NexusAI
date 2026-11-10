import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../../services/api";
import { Button } from "../ui/button";
import { Card, CardTitle } from "../ui/card";

interface CustomerConsent {
  id: string;
  name: string;
  phone: string;
  smsOptIn: boolean;
  consentSource?: string | null;
}

export default function CustomerConsentManager() {
  const queryClient = useQueryClient();
  const [sources, setSources] = useState<Record<string, string>>({});
  const customers = useQuery({
    queryKey: ["customer-consent"],
    queryFn: async () =>
      (await api.get<CustomerConsent[]>("/customers")).data,
  });
  const update = useMutation({
    mutationFn: async ({
      customer,
      smsOptIn,
    }: {
      customer: CustomerConsent;
      smsOptIn: boolean;
    }) =>
      api.put(`/customers/${customer.id}/sms-consent`, {
        sms_opt_in: smsOptIn,
        consent_source:
          sources[customer.id]?.trim() ||
          customer.consentSource ||
          "Imported, verified customer consent",
      }),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["customer-consent"] }),
  });

  return (
    <Card>
      <CardTitle>Customer SMS consent</CardTitle>
      <p className="mb-3 text-xs text-nexus-muted">
        Twilio delivery is blocked unless opt-in is recorded. Record a verified
        consent source before enabling SMS for a customer.
      </p>
      {customers.isLoading && <p className="text-sm text-nexus-muted">Loading customers…</p>}
      {customers.isError && (
        <p role="alert" className="text-sm text-nexus-danger">
          Could not load customers: {customers.error.message}
        </p>
      )}
      {update.isError && (
        <p role="alert" className="mb-2 text-sm text-nexus-danger">
          Could not update consent: {update.error.message}
        </p>
      )}
      <div className="space-y-2">
        {customers.data?.map((customer) => (
          <div
            key={customer.id}
            className="flex flex-wrap items-center gap-2 rounded-lg border border-nexus-border p-3"
          >
            <div className="min-w-[140px] flex-1">
              <div className="text-sm text-white">
                {customer.name} · {customer.id}
              </div>
              <div className="text-xs text-nexus-muted">{customer.phone}</div>
              <div className="text-[11px] text-nexus-muted">
                Current: {customer.smsOptIn ? "Opted in" : "No recorded opt-in"}
              </div>
            </div>
            <input
              value={sources[customer.id] ?? ""}
              onChange={(event) =>
                setSources((current) => ({
                  ...current,
                  [customer.id]: event.target.value,
                }))
              }
              placeholder={customer.consentSource || "Verified consent source"}
              aria-label={`Consent source for ${customer.id}`}
              className="min-w-[190px] flex-1 rounded-lg border border-nexus-border bg-nexus-bg px-3 py-2 text-xs text-white"
            />
            <Button
              variant={customer.smsOptIn ? "danger" : "outline"}
              disabled={
                update.isPending ||
                (!customer.smsOptIn && !(sources[customer.id] || customer.consentSource))
              }
              onClick={() =>
                update.mutate({ customer, smsOptIn: !customer.smsOptIn })
              }
            >
              {customer.smsOptIn ? "Revoke opt-in" : "Record opt-in"}
            </Button>
          </div>
        ))}
      </div>
    </Card>
  );
}

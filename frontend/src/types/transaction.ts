export type TransactionStatus =
  | "success"
  | "pending"
  | "failed"
  | "refunded"
  | "abandoned";

export interface Transaction {
  id: string;
  txnRef: string;
  customerId: string;
  merchantId: string;
  amount: number;
  currency: string;
  status: TransactionStatus;
  method: "UPI" | "CARD" | "WALLET" | "NETBANKING";
  upiRef?: string;
  settlementId?: string;
  rootCause?: string;
  createdAt: string;
  updatedAt: string;
}

export interface TransactionSearchParams {
  q?: string;
  status?: TransactionStatus;
  merchantId?: string;
  customerId?: string;
  limit?: number;
}

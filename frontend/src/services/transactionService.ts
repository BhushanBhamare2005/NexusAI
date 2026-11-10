import { api } from "./api";
import type { Transaction, TransactionSearchParams } from "../types/transaction";

export async function searchTransactions(
  params: TransactionSearchParams
): Promise<Transaction[]> {
  const { data } = await api.get<Transaction[]>("/transactions", { params });
  return data;
}

export async function getTransaction(id: string): Promise<Transaction> {
  const { data } = await api.get<Transaction>(`/transactions/${id}`);
  return data;
}

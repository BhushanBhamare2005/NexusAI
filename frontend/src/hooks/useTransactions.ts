import { useQuery } from "@tanstack/react-query";
import { searchTransactions, getTransaction } from "../services/transactionService";
import type { TransactionSearchParams } from "../types/transaction";

export function useTransactionSearch(params: TransactionSearchParams) {
  return useQuery({
    queryKey: ["transactions", params],
    queryFn: () => searchTransactions(params),
  });
}

export function useTransaction(id?: string) {
  return useQuery({
    queryKey: ["transaction", id],
    queryFn: () => getTransaction(id!),
    enabled: !!id,
  });
}

import { getToken } from "./auth";

const API_PREFIX = "/api/v1";

export type RaffleBranch = {
  id: number;
  name: string;
  slug: string;
  image_url: string | null;
  number_start: number;
  number_end: number;
};

export type RaffleStatus = {
  raffle_id: number;
  title: string;
  prize_title: string | null;
  status: string;
  total_numbers: number;
  numbers_per_branch: number;
  branches: RaffleBranch[];
};

export type RaffleNumber = {
  id: number;
  number: number;
  status: string;
};

export type TicketValidationResult = {
  ticket_code_id: number | null;
  code_last4: string;
  status: string;
  reason: string | null;
};

export type TicketBatchValidation = {
  batch_id: number;
  submitted_count: number;
  accepted_count: number;
  rejected_count: number;
  results: TicketValidationResult[];
};

export type RaffleEntry = {
  id: number;
  branch_id: number;
  selected_number: number;
  created_at: string;
};

function apiUrl(path: string) {
  const configuredBaseUrl =
    import.meta.env.PUBLIC_API_BASE_URL?.trim() ||
    import.meta.env.PUBLIC_API_URL?.trim();

  const baseUrl =
    configuredBaseUrl && configuredBaseUrl.length > 0
      ? configuredBaseUrl
      : `http://${window.location.hostname}:8000`;

  return `${baseUrl.replace(/\/+$/, "")}${path}`;
}

async function raffleRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const token = getToken();

  if (!token) {
    window.location.href = "/inscribete?redirect=/hub";
    throw new Error("Sesión no encontrada.");
  }

  const response = await fetch(apiUrl(`${API_PREFIX}${path}`), {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail ?? "Ocurrió un error.");
  }

  return data as T;
}

export function getRaffleStatus() {
  return raffleRequest<RaffleStatus>("/raffle/status");
}

export function getBranchNumbers(branchId: number) {
  return raffleRequest<RaffleNumber[]>(`/raffle/branches/${branchId}/numbers`);
}

export function validateTicketCodes(branchId: number, codes: string[]) {
  return raffleRequest<TicketBatchValidation>("/raffle/tickets/validate", {
    method: "POST",
    body: JSON.stringify({
      branch_id: branchId,
      codes,
    }),
  });
}

export function confirmNumbers(
  batchId: number,
  selections: { ticket_code_id: number; raffle_number_id: number }[],
) {
  return raffleRequest<RaffleEntry[]>("/raffle/numbers/confirm", {
    method: "POST",
    body: JSON.stringify({
      batch_id: batchId,
      selections,
    }),
  });
}

export function getMyRaffleEntries() {
  return raffleRequest<RaffleEntry[]>("/raffle/me/entries");
}

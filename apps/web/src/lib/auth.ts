const API_PREFIX = "/api/v1";

const TOKEN_KEY = "starcolors_access_token";
const USER_KEY = "starcolors_user";
const SESSION_EXPIRES_AT_KEY = "starcolors_session_expires_at";
const SESSION_DURATION_MS = 24 * 60 * 60 * 1000;

export type AuthUser = {
  id: number;
  full_name: string;
  email: string;
  phone: string | null;
  is_active: boolean;
  is_admin: boolean;
};

type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  user: AuthUser;
};

type RegisterPayload = {
  full_name: string;
  email: string;
  password: string;
  phone?: string;
};

type LoginPayload = {
  email: string;
  password: string;
};

type ApiError = {
  detail?: string | Array<{ msg?: string }>;
};

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(apiUrl(path), {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const data = (await response.json().catch(() => null)) as T | ApiError | null;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return data as T;
}

function apiUrl(path: string) {
  const configuredBaseUrl =
    import.meta.env.PUBLIC_API_BASE_URL?.trim() ||
    import.meta.env.PUBLIC_API_URL?.trim();
  const baseUrl =
    configuredBaseUrl && configuredBaseUrl.length > 0
      ? configuredBaseUrl
      : `http://${window.location.hostname}:8000`;

  const normalizedBaseUrl = baseUrl.replace(/\/+$/, "");
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;

  if (
    normalizedBaseUrl.endsWith(API_PREFIX) &&
    normalizedPath.startsWith(API_PREFIX)
  ) {
    return `${normalizedBaseUrl}${normalizedPath.slice(API_PREFIX.length)}`;
  }

  return `${normalizedBaseUrl}${normalizedPath}`;
}

function getErrorMessage(data: unknown): string {
  if (!data || typeof data !== "object") {
    return "Ocurrió un error.";
  }

  const detail = (data as ApiError).detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail[0]?.msg ?? "Revisa los campos del formulario.";
  }

  return "Ocurrió un error.";
}

export async function registerUser(payload: RegisterPayload) {
  const data = await request<AuthResponse>("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  saveSession(data);

  return data;
}

export async function loginUser(payload: LoginPayload) {
  const data = await request<AuthResponse>("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  saveSession(data);

  return data;
}

export async function getCurrentUser() {
  const token = getToken();

  if (!token) {
    return null;
  }

  return request<AuthUser>("/api/v1/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function saveSession(data: AuthResponse) {
  localStorage.setItem(TOKEN_KEY, data.access_token);
  localStorage.setItem(USER_KEY, JSON.stringify(data.user));
  localStorage.setItem(
    SESSION_EXPIRES_AT_KEY,
    String(Date.now() + SESSION_DURATION_MS),
  );
}

export function getToken() {
  if (isSessionExpired()) {
    logoutUser();
    return null;
  }

  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser(): AuthUser | null {
  if (isSessionExpired()) {
    logoutUser();
    return null;
  }

  const user = localStorage.getItem(USER_KEY);

  if (!user) {
    return null;
  }

  return JSON.parse(user) as AuthUser;
}

function isSessionExpired() {
  const expiresAt = Number(localStorage.getItem(SESSION_EXPIRES_AT_KEY));

  if (!expiresAt) {
    return false;
  }

  return Date.now() > expiresAt;
}

export function logoutUser() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(SESSION_EXPIRES_AT_KEY);
}

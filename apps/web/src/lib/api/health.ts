const backendUrl =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${backendUrl}/health`, {
    next: { revalidate: 0 },
  });

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

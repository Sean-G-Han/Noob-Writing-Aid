const BASE_URL = "http://127.0.0.1:8000";
import type {Result} from ".././Result";
import {Success, Failure} from ".././Result";

export async function apiRequest<T>(
    path: string,
    method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH" = "GET",
    body?: unknown
): Promise<Result<T>> {
    const res = await fetch(`${BASE_URL}${path}`, {
        method,
        headers: {
            "Content-Type": "application/json",
        },
        body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) {
        console.error(`API request failed: ${res.status} ${res.statusText}`);
        return Failure(`API request failed with status ${res.status}: ${res.statusText}`);
    }

    const data = await res.json() as T;
    
    console.log(`API request successful: ${res.status} ${res.statusText}: ${JSON.stringify(data)}`);
    return Success(data);
}
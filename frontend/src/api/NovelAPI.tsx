import type { Novel } from "../types";
import { apiRequest } from "./Client";

export type CreateNovelRequest = {
    title: string;
};

export type BooleanResponse = {
    ok: boolean;
};

export function createNovel(data: CreateNovelRequest) {
    return apiRequest<Novel>(
        "/novels/",
        "POST",
        data
    );
}

export function getNovels() {
    return apiRequest<Novel[]>(
        "/novels/",
        "GET"
    );
}

export function updateNovel(id: number, data: CreateNovelRequest) {
    return apiRequest<Novel>(
        `/novels/${id}`,
        "PUT",
        data
    );
}

export function deleteNovel(id: number) {
    return apiRequest<BooleanResponse>(
        `/novels/${id}`,
        "DELETE"
    );
}
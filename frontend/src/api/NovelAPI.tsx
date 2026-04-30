import { apiRequest } from "./Client";

export type CreateNovelRequest = {
    title: string;
};

export type BooleanResponse = {
    ok: boolean;
};

export type NovelResponse = {
    id: number;
    title: string;
};

export function createNovel(data: CreateNovelRequest) {
    return apiRequest<NovelResponse>(
        "/novels/",
        "POST",
        data
    );
}

export function getNovels() {
    return apiRequest<NovelResponse[]>(
        "/novels/",
        "GET"
    );
}

export function updateNovel(id: number, data: Partial<CreateNovelRequest>) {
    return apiRequest<NovelResponse>(
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
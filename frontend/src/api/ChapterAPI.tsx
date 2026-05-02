import type { Chapter } from "../types";
import { apiRequest } from "./Client";

// REVIEW Inconsidency as chapter uses the same type
// for create and update. Consider refactoring
export type CreateChapterRequest = {
    novel_id: number
    title: string
};

export type EditChapterRequest = {
    title: string
    chapter_number: number
};

export function getChapters(novelId: number) {
    return apiRequest<Chapter[]>(
        `/chapters/novel/${novelId}`,
        "GET"
    );
}

export function createChapter(data: CreateChapterRequest) {
    return apiRequest<Chapter>(
        `/chapters/append`,
        "POST",
        data
    );
}

export function editChapter(id: number, data: Partial<EditChapterRequest>) {
    return apiRequest<Chapter>(
        `/chapters/${id}`,
        "PUT",
        data
    );
}

export function deleteChapter(id: number) {
    return apiRequest<{ ok: boolean }>(
        `/chapters/${id}`,
        "DELETE"
    );
}
import { apiRequest } from "./Client";

export type ChapterResponse = {
    id: number
    novel_id: number
    chapter_number: number
    title: string
    raw_file_path: number | null
    annotated_file_path: string | null
    hash: string | null
};

// REVIEW Inconsidency as chapter uses the same type
// for create and update. Consider refactoring
export type CreateChapterRequest = {
    novel_id: number
    title: string
};

export type UpdateChapterRequest = {
    title: string
    chapter_number: number
};

export function getChapters(novelId: number) {
    return apiRequest<ChapterResponse[]>(
        `/chapters/novel/${novelId}`,
        "GET"
    );
}

export function createChapter(data: CreateChapterRequest) {
    return apiRequest<ChapterResponse>(
        `/chapters/append`,
        "POST",
        data
    );
}

export function updateChapter(id: number, data: Partial<UpdateChapterRequest>) {
    return apiRequest<ChapterResponse>(
        `/chapters/${id}`,
        "PUT",
        data
    );
}
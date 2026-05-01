import { apiRequest } from "./Client";

export type ChapterResponse = {
    id: number
    novel_id: number
    chapter_number: number
    title: number
    raw_file_path: number | null
    annotated_file_path: string | null
    hash: string | null
};

export function getChapters(novelId: number) {
    return apiRequest<Partial<ChapterResponse>[]>(
        `/chapters/novel/${novelId}`,
        "GET"
    );
}
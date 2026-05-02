import { apiRequest } from "./Client";

export type ChapterSaveRequest = {
    content: string;
    base_dir?: string;
};

export type ChapterSaveResponse = {
    file_path: string;
    hash: string;
};

export type ChapterLoadResponse = {
    content: string;
};

export type GradeResponse = {
    annotatedText: string;
};

export function saveChapterContent(chapterId: number,  data: ChapterSaveRequest) {
    return apiRequest<ChapterSaveResponse>(
        `/content/save/${chapterId}`,
        "POST",
        data
    );
}

export function loadChapterContent(chapterId: number) {
    return apiRequest<ChapterLoadResponse>(
        `/content/load/${chapterId}`,
        "GET"
    );
}

export function gradeChapterContent(chapterId: number) {
    return apiRequest<GradeResponse>(
        `/content/grade/${chapterId}`,
        "POST"
    );
}
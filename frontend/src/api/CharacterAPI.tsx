import type { Character } from "../types";
import { apiRequest } from "./Client";
import type { BooleanResponse } from "./NovelAPI";

export type CreateCharacterRequest = {
    novel_id: number,
    common_name: string, 
    adjectives: string[], 
    description: string, 
    pronouns: string[], 
    alternative_names: string[], 
    chapters: number[]
}

export function createCharacter(data: CreateCharacterRequest) {
    return apiRequest<Character>(
        `/characters/`,
        "POST",
        data
    );
}

export function getCharacters(chapter_id: number) {
    return apiRequest<Character[]>(
        `/characters/chapter/${chapter_id}`,
        "GET"
    );
}

export function getAllCharacters(novel_id: number) {
    return apiRequest<Character[]>(
        `/characters/novels/${novel_id}`,
        "GET"
    )
}

export function editCharacter(id: number, data: Partial<CreateCharacterRequest>) {
    return apiRequest<Character>(
        `/characters/${id}`,
        "PUT",
        data
    );
}

export function linkCharacter(chapter_id: number, character_id: number) {
    return apiRequest<BooleanResponse>(
        `/characters/link`,
        "PATCH",
        {chapter_id: chapter_id, character_id: character_id}
    )
}

export function unlinkCharacter(chapter_id: number, character_id: number) {
    return apiRequest<BooleanResponse>(
        `/characters/unlink`,
        "PATCH",
        {chapter_id: chapter_id, character_id: character_id}
    )
}

export function deleteCharacter(id: number) {
    return apiRequest<{ ok: boolean }>(
        `/characters/${id}`,
        "DELETE"
    );
}

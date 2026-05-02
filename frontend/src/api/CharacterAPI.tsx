import type { Character } from "../types";
import { apiRequest } from "./Client";

export type CreateCharacterRequest = {
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

export function editCharacter(id: number, data: Partial<CreateCharacterRequest>) {
    return apiRequest<Character>(
        `/characters/${id}`,
        "PUT",
        data
    );
}

export function deleteCharacter(id: number) {
    return apiRequest<{ ok: boolean }>(
        `/characters/${id}`,
        "DELETE"
    );
}

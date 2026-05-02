export type Novel = {
    id: number;
    title: string;
};

export type Chapter = {
    id: number
    novel_id: number
    chapter_number: number
    title: string
    raw_file_path: number | null
    annotated_file_path: string | null
    hash: string | null
};

export type Character = {
    id: number;
    common_name: string;
    adjectives: string[];
    description: string;
    pronouns: string[];
    alternative_names: string[];
}
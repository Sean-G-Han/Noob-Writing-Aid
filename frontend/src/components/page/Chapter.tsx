import { useContext, useEffect, useState } from "react";
import { AppContext } from "../../AppContext";
import type { Character, Chapter } from "../../types";
import { deleteChapter, getChapters } from "../../api/ChapterAPI";
import { deleteCharacter, getCharacters } from "../../api/CharacterAPI";
import { CreateChapterModal } from "../modal/chapter/CreateChapterModal";
import { EditChapterModal } from "../modal/chapter/EditChapterModal";
import { CreateCharacterModal } from "../modal/character/CreateCharacterModal";
import { EditCharacterModal } from "../modal/character/EditCharacterModal";
import { LinkCharacterModal } from "../modal/character/LinkCharacterModal";

export function ChapterPage() {
    return (
        <div className="row w-100 h-100 align-items-start m-0 p-0">
            <div className="col-6 flex-column d-flex" style={{ height: "100%" }}>
                <ChapterView />
            </div>
            <div className="col-6 flex-column d-flex" style={{ height: "100%" }}>
                <CharacterView />
            </div>
        </div>
    );
}

export function ChapterView() {
    const { selectedNovel, setSelectedChapter, setModalContent } =
        useContext(AppContext);

    const [chapters, setChapters] = useState<Chapter[]>([]);

    useEffect(() => {
        if (!selectedNovel) return;

        getChapters(selectedNovel.id).then((res) => {
            if (res.ok) setChapters(res.result);
            else alert("Failed to fetch chapters: " + res.error);
        });
    }, [selectedNovel]);

    async function refreshChapters() {
        if (!selectedNovel) return;

        const res = await getChapters(selectedNovel.id);

        if (res.ok) setChapters(res.result);
        else alert("Failed to refresh chapters: " + res.error);
    }

    function handleCreateChapter() {
        setModalContent(
            <CreateChapterModal
                onCreate={async () => {
                    await refreshChapters();
                }}
            />
        );
    }

    function handleEditChapter(chapter: Chapter) {
        setModalContent(
            <EditChapterModal
                chapter={chapter}
                onUpdate={async () => {
                    await refreshChapters();
                }}
            />
        );
    }

    return (
        <div className="w-100 h-100 d-flex flex-column">
            <div className="d-flex justify-content-between align-items-center bg-dark text-white p-2 my-2">
                <div className="fw-bold">
                    {!selectedNovel
                        ? "No Novel Selected"
                        : `${selectedNovel.title} - Chapters`}
                </div>

                <button
                    className="btn btn-sm btn-success"
                    onClick={handleCreateChapter}
                    disabled={!selectedNovel}
                >
                    Create
                </button>
            </div>

            <div className="flex-grow-1 overflow-auto p-3">
                {[...chapters]
                    .sort((a, b) => a.chapter_number - b.chapter_number)
                    .map((chapter) => (
                        <Item
                            key={chapter.id}
                            title={chapter.title}
                            onClick={() => setSelectedChapter(chapter)}
                            onEdit={() => handleEditChapter(chapter)}
                            onDelete={() =>
                                deleteChapter(chapter.id).then((res) => {
                                    if (res.ok) refreshChapters();
                                    else alert("Failed to delete chapter: " + res.error);
                                })
                            }
                        />
                    ))}
            </div>
        </div>
    );
}

export function CharacterView() {
    const { selectedNovel, selectedChapter, setModalContent } = useContext(AppContext);
    const [characters, setCharacters] = useState<Character[]>([]);

    useEffect(() => {
        if (!selectedNovel || !selectedChapter) return;

        getCharacters(selectedChapter.id).then((res) => {
            if (res.ok) setCharacters(res.result);
            else alert("Failed to fetch characters: " + res.error);
        });
    }, [selectedNovel, selectedChapter]);

    async function refreshCharacters() {
        if (!selectedNovel || !selectedChapter) return;

        const res = await getCharacters(selectedChapter.id);

        if (res.ok) setCharacters(res.result);
        else alert("Failed to refresh chars: " + res.error);
    }

    function handleLinkCharacter() {
        setModalContent(
            <LinkCharacterModal onUpdate={
                async () => await refreshCharacters()
            }/>
        )
    }

    function handleCreateCharacter() {
        setModalContent(
            <CreateCharacterModal onCreate={
                async () => await refreshCharacters()
            }/>
        )
    }

    function handleEditCharacter(character: Character) {
        setModalContent(
            <EditCharacterModal character={character} onUpdate={
                async () => await refreshCharacters()
            }/>
        )
    }

    return (
        <div className="w-100 h-100 d-flex flex-column">
            <div className="d-flex justify-content-between align-items-center bg-dark text-white p-2 my-2">
                <div className="fw-bold">
                    {!selectedNovel || !selectedChapter
                        ? "No Chapter Selected"
                        : `${selectedNovel.title}: ${selectedChapter.title} - Characters`}
                </div>
                <div className="d-flex gap-2">
                    <button
                        className="btn btn-sm btn-secondary"
                        onClick={handleLinkCharacter}
                        disabled={!selectedNovel || !selectedChapter}
                    >
                        Link
                    </button>

                    <button
                        className="btn btn-sm btn-success"
                        onClick={handleCreateCharacter}
                        disabled={!selectedNovel || !selectedChapter}
                    >
                        Create
                    </button>
                </div>
            </div>

            <div className="flex-grow-1 overflow-auto p-3">
                {characters.map((character) => (
                    <Item
                        key={character.id}
                        title={character.common_name}
                        onClick={() => alert(`Selected ${character.common_name}`)}
                        onEdit={() => handleEditCharacter(character)}
                        onDelete={() => 
                            deleteCharacter(character.id).then((res) => {
                                if (res.ok) refreshCharacters();
                                else alert("Failed to delete character: " + res.error);
                            })
                        }
                    />
                ))}
            </div>
        </div>
    );
}

type ItemProps = {
    title: string;
    onClick: () => void;
    onEdit: () => void;
    onDelete: () => void;
};

function Item({ title, onClick, onEdit, onDelete }: ItemProps) {
    return (
        <div
            className="border rounded p-2 mb-2 d-flex justify-content-between align-items-center"
            onClick={onClick}
            style={{ cursor: "pointer" }}
        >
            <div className="fw-bold">
                {title}
            </div>

            <div className="d-flex gap-2">
                <button
                    className="btn btn-sm btn-primary"
                    onClick={(e) => {
                        e.stopPropagation();
                        onEdit();
                    }}
                >
                    Edit
                </button>

                <button
                    className="btn btn-sm btn-danger"
                    onClick={(e) => {
                        e.stopPropagation();
                        onDelete();
                    }}
                >
                    Delete
                </button>
            </div>
        </div>
    );
}
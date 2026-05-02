import { useContext, useEffect, useState } from "react";
import { AppContext } from "../../AppContext";
import type { Chapter } from "../../types";
import { getChapters } from "../../api/ChapterAPI";
import { CreateChapterModal, EditChapterModal } from "../modal/ChapterModal";

export function Chapter() {
    return (
        <div className="row w-100 h-100 align-items-start m-0 p-0">
            <div className="col-6 flex-column d-flex" style={{ height: "100%" }}>
                <ChapterView />
            </div>
            <div className="col-6 flex-column d-flex" style={{ height: "100%" }}>
            </div>
        </div>
    );
}

export function ChapterView() {
    const { selectedNovel, setModalContent } = useContext(AppContext);
    const [chapters, setChapters] = useState<Chapter[]>([]);

    useEffect(() => {
        if (!selectedNovel) return;

        getChapters(selectedNovel.id).then((res) => {
            if (res.ok) {
                setChapters(res.result);
            } else {
                alert("Failed to fetch chapters: " + res.error);
            }
        });
    }, [selectedNovel]);

    async function refreshChapters() {
        if (!selectedNovel) return;

        const res = await getChapters(selectedNovel.id);

        if (res.ok) {
            setChapters(res.result);
        } else {
            alert("Failed to refresh chapters: " + res.error);
        }
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
                        : selectedNovel.title + " - Chapters"}
                </div>

                <button
                    className="btn btn-sm btn-success"
                    onClick={handleCreateChapter}
                    disabled={!selectedNovel}
                >
                    +
                </button>
            </div>

            <div className="flex-grow-1 overflow-auto p-3">
                {[...chapters]
                    .sort((a, b) => a.chapter_number - b.chapter_number)
                    .map((chapter) => (
                        <ChapterItem
                            key={chapter.id}
                            chapter={chapter}
                            onClick={() =>
                                alert("Clicked " + chapter.title)
                            }
                            onEdit={() => handleEditChapter(chapter)}
                            onDelete={() =>
                                alert("Delete " + chapter.title)
                            }
                        />
                    ))}
            </div>
        </div>
    );
}

type ChapterItemProps = {
  chapter: Chapter;
  onClick: () => void;
  onEdit: () => void;
  onDelete: () => void;
};

function ChapterItem({ chapter, onClick, onEdit, onDelete }: ChapterItemProps) {
    return (
        <div
            className="border rounded p-2 mb-2 d-flex justify-content-between align-items-center"
            onClick={onClick}
            style={{ cursor: "pointer" }}
        >
            <div>
                <div className="fw-bold">
                    {chapter.chapter_number}. {chapter.title}
                </div>
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
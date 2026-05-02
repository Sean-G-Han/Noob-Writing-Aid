import { useState, useContext } from "react";
import { editChapter } from "../../../api/ChapterAPI";
import { AppContext } from "../../../AppContext";
import type { Chapter } from "../../../types";

type EditChapterModalProps = {
    chapter: Chapter;
    onUpdate: (updated: Chapter) => void;
};

export function EditChapterModal({ chapter, onUpdate }: EditChapterModalProps) {
    const { closeModal } = useContext(AppContext);
    const [error, setError] = useState("");

    const [updatedChapter, setUpdatedChapter] = useState<Chapter>({
        ...chapter
    });

    function handleEditChapter() {
        editChapter(chapter.id, {
            title: updatedChapter.title,
            chapter_number: updatedChapter.chapter_number
        }).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                onUpdate(res.result);
                closeModal();
            }
        });
    }

    return (
        <>
            <h5 className="mb-0">Update Chapter</h5>

            <input
                className="form-control my-3"
                value={updatedChapter.title}
                onChange={(e) =>
                    setUpdatedChapter((prev) => ({
                        ...prev,
                        title: e.target.value
                    }))
                }
            />

            <input
                className="form-control my-3"
                type="number"
                value={updatedChapter.chapter_number}
                onChange={(e) =>
                    setUpdatedChapter((prev) => ({
                        ...prev,
                        chapter_number: Number(e.target.value)
                    }))
                }
            />

            {error && <div className="alert alert-danger">{error}</div>}

            <button
                className="btn btn-primary w-100 my-3"
                onClick={handleEditChapter}
            >
                Update
            </button>
        </>
    );
}
import { useState, useContext } from "react";
import { createChapter, type CreateChapterRequest } from "../../../api/ChapterAPI";
import { AppContext } from "../../../AppContext";
import type { Chapter } from "../../../types";

type CreateChapterModalProps = {
    onCreate: (created: Chapter) => void;
};

export function CreateChapterModal({ onCreate }: CreateChapterModalProps) {
    const [chapterName, setChapterName] = useState("");
    const [error, setError] = useState("");
    const { closeModal, selectedNovel } = useContext(AppContext);

    function handleCreateChapter(data: CreateChapterRequest): void {
        createChapter(data).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                onCreate(res.result);
                closeModal();
            }
        });
    }

    return (
        <>
            <div className="row align-items-center">
                <div className="col-4">
                    <h5 className="mb-0">Create Chapter</h5>
                </div>

                <div className="col-8">
                    <input
                        className="form-control my-3"
                        placeholder="Enter chapter name"
                        value={chapterName}
                        onChange={(e) => setChapterName(e.target.value)}
                    />
                </div>
            </div>

            {error && <div className="alert alert-danger">{error}</div>}

            <button
                className="btn btn-primary w-100 my-3"
                onClick={() => {
                    if (!selectedNovel) return;

                    handleCreateChapter({
                        novel_id: selectedNovel.id,
                        title: chapterName
                    });
                }}
            >
                Create
            </button>
        </>
    );
}
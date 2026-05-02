import { useState, useContext } from "react";
import type { CreateNovelRequest } from "../../../api/NovelAPI";
import { createNovel } from "../../../api/NovelAPI";
import { AppContext } from "../../../AppContext";

export function CreateNovelModal() {
    const [novelName, setNovelName] = useState("");
    const [error, setError] = useState("");
    const { closeModal } = useContext(AppContext);

    function handleCreateNovel(data: CreateNovelRequest): void {
        createNovel(data).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                closeModal();
            }
        });
    }

    return (
        <>
            <div className="row align-items-center">
                <div className="col-4">
                    <h5 className="mb-0">Create Novel</h5>
                </div>

                <div className="col-8">
                    <input
                        className="form-control my-3"
                        placeholder="Enter novel name"
                        value={novelName}
                        onChange={(e) => setNovelName(e.target.value)}
                    />
                </div>
            </div>

            {error && <div className="alert alert-danger">{error}</div>}

            <button
                className="btn btn-primary w-100 my-3"
                onClick={() => handleCreateNovel({ title: novelName })}
            >
                Create
            </button>
        </>
    );
}
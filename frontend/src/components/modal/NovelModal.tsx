import { useState, useContext } from "react";
import type { CreateNovelRequest } from "../../api/NovelAPI";
import { createNovel } from "../../api/NovelAPI";
import { ModalContext } from "./ModalContext";

export function CreateNovelModal() {
    const [novelName, setNovelName] = useState("");
    const [error, setError] = useState("");
    const { onClose } = useContext(ModalContext);

    function handleCreateNovel(data: CreateNovelRequest): void {
        createNovel(data).then((res) => {
            console.log(res);
            if (!res.ok) {
                setError(res.error);
            } else {
                onClose();
            }
        })
    }

    return (
        <>
            <h5>Create New Novel</h5>

            <input
                className="form-control my-3"
                placeholder="Enter novel name"
                value={novelName}
                onChange={(e) => setNovelName(e.target.value)}
            />

            {error != "" && <div className="alert alert-danger">{error}</div>}

            <button className="btn btn-primary w-100 my-3"
                onClick={async () => handleCreateNovel({ title: novelName })}
            >
                Create
            </button>
        </>
    );
}

export function LoadNovelModal() {
    return (
        <>
            <h5>Load Novel</h5>
        </>
    );
}
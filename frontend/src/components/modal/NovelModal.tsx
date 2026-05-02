import { useState, useContext, useEffect } from "react";
import type { CreateNovelRequest, NovelResponse } from "../../api/NovelAPI";
import { createNovel, deleteNovel, getNovels, updateNovel } from "../../api/NovelAPI";
import { AppContext } from "../../AppContext";
import type { Novel } from "../../types";

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

export function LoadNovelModal() {
    const [novels, setNovels] = useState<NovelResponse[]>([]);
    const [error, setError] = useState("");
    const [searchTerm, setSearchTerm] = useState("");
    const { closeModal, setSelectedNovel } = useContext(AppContext);

    useEffect(() => {
        getNovels().then((res) => {
            if (res.ok) {
                setNovels(res.result);
            } else {
                setError(res.error);
            }
        });
    }, []);

    function handleSelectNovel(novel: NovelResponse) {
        setSelectedNovel(novel);
        closeModal();
    }

    const filteredNovels = novels.filter((novel) =>
        novel.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <>
            <div className="row align-items-center">
                <div className="col-4">
                    <h5 className="mb-0">Load Novel</h5>
                </div>

                <div className="col-8">
                    <input
                        className="form-control"
                        placeholder="Search novels..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {error && <div className="alert alert-danger">{error}</div>}

            <div className="list-group my-3 overflow-auto" style={{ maxHeight: "250px" }}>
                {filteredNovels.length === 0 ? (
                    <div className="text-center text-muted my-3">
                        No novels found
                    </div>
                ) : (
                    filteredNovels.map((novel) => (
                        <LoadNovelItem
                            key={novel.id}
                            novel={novel}
                            onSelect={handleSelectNovel}
                        />
                    ))
                )}
            </div>
        </>
    );
}

type LoadNovelItemProps = {
    novel: NovelResponse;
    onSelect: (novel: NovelResponse) => void;
};

function LoadNovelItem({ novel, onSelect }: LoadNovelItemProps) {
    return (
        <div
            className="d-flex align-items-center justify-content-between py-2 border-bottom"
            style={{ cursor: "pointer" }}
            onClick={() => onSelect(novel)}
        >
            <div className="flex-grow-1 me-2 text-truncate">
                {novel.title}
            </div>
        </div>
    );
}

export function EditNovelModal() {
    const [novels, setNovels] = useState<NovelResponse[]>([]);
    const [error, setError] = useState("");
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        getNovels().then((res) => {
            if (res.ok) {
                setNovels(res.result);
            } else {
                setError(res.error);
            }
        });
    }, []);

    function handleEditNovel(id: number, title: string) {
        updateNovel(id, { title }).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                setNovels((prev) =>
                    prev.map((n) => (n.id === id ? res.result : n))
                );
                setError("");
            }
        });
    }

    function handleDeleteNovel(id: number) {
        deleteNovel(id).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                setNovels((prev) => prev.filter((n) => n.id !== id));
                setError("");
            }
        });
    }

    const filteredNovels = novels.filter((novel) =>
        novel.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <>
            <div className="row align-items-center">
                <div className="col-4">
                    <h5 className="mb-0">Edit Novel</h5>
                </div>

                <div className="col-8">
                    <input
                        className="form-control"
                        placeholder="Search novels..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {error && <div className="alert alert-danger">{error}</div>}

            <div className="list-group my-3 overflow-auto" style={{ maxHeight: "250px" }}>
                {filteredNovels.length === 0 ? (
                    <div className="text-center text-muted my-3">
                        No novels found
                    </div>
                ) : (
                    filteredNovels.map((novel) => (
                        <EditNovelItem
                            key={novel.id}
                            novel={novel}
                            onEdit={handleEditNovel}
                            onDelete={handleDeleteNovel}
                        />
                    ))
                )}
            </div>
        </>
    );
}

type EditNovelItemProps = {
    novel: Novel;
    onEdit: (id: number, title: string) => void;
    onDelete: (id: number) => void;
};

function EditNovelItem({ novel, onEdit, onDelete }: EditNovelItemProps) {
    const [title, setTitle] = useState(novel.title);

    // Ignore warning for now
    // Wont cause cascading effect
    useEffect(() => {
        setTitle(novel.title);
    }, [novel.title]);

    return (
        <div className="d-flex align-items-center justify-content-between py-2 border-bottom">
            <div className="flex-grow-1 me-2">
                <input
                    className="form-control"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
            </div>

            <div className="d-flex gap-2">
                <button
                    className="btn btn-sm btn-primary"
                    onClick={() => onEdit(novel.id, title)}
                >
                    Edit
                </button>

                <button
                    className="btn btn-sm btn-danger"
                    onClick={() => onDelete(novel.id)}
                >
                    Delete
                </button>
            </div>
        </div>
    );
}
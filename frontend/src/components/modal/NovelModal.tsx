import { useState, useContext, useEffect } from "react";
import type { CreateNovelRequest, NovelResponse } from "../../api/NovelAPI";
import { createNovel, getNovels } from "../../api/NovelAPI";
import { AppContext } from "../../AppContext";

export function CreateNovelModal() {
    const [novelName, setNovelName] = useState("");
    const [error, setError] = useState("");
    const { closeModal } = useContext(AppContext);

    function handleCreateNovel(data: CreateNovelRequest): void {
        createNovel(data).then((res) => {
            console.log(res);
            if (!res.ok) {
                setError(res.error);
            } else {
                closeModal();
            }
        })
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

            <div
                className="list-group my-3 overflow-auto"
                style={{ maxHeight: "250px" }}
            >
                {filteredNovels.length === 0 ? (
                    <div className="text-center text-muted my-3">
                        No novels found
                    </div>
                ) : (
                    filteredNovels.map((novel) => (
                        <LoadNovelItem key={novel.id} novel={novel} />
                    ))
                )}
            </div>
        </>
    );
}

export function LoadNovelItem({novel}: {novel: NovelResponse}) {
    const { closeModal, setSelectedNovel } = useContext(AppContext);
    return (
        <button 
            className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
            onClick={() => {
                setSelectedNovel(novel);
                closeModal();
            }}

        >
            <span className="text-truncate">{novel.title}</span>
            <span className="text-muted">›</span>
        </button>
    );
}
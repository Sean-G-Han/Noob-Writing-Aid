import { useState, useContext, useEffect } from "react";
import type { NovelResponse } from "../../../api/NovelAPI";
import { getNovels } from "../../../api/NovelAPI";
import { AppContext } from "../../../AppContext";

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

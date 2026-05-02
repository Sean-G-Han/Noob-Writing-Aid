import { Link } from "react-router-dom";
import { useContext, useRef, useState } from "react";
import { AppContext } from "../../AppContext";
import { useOutsideClick } from "../../hooks/useOutsideClick";
import { CreateNovelModal } from "../modal/novel/CreateNovelModal";
import { LoadNovelModal } from "../modal/novel/LoadNovelModal";
import { EditNovelModal } from "../modal/novel/EditNovelModal";

export function NovelMenu({ open, onNew, onOpen, onEdit}: { open: boolean, onNew: () => void, onOpen: () => void, onEdit: () => void }) {
  if (!open) return null;

  return (
        <div
            className="position-absolute bg-white text-dark border rounded shadow"
            style={{ top: "100%", left: 0, marginTop: "5px", minWidth: "150px", padding: "5px 5px", zIndex: 1000 }}>
            <div className="dropdown-item" style={{ cursor: "pointer" }} onClick={onNew}>Create New Novel</div>
            <div className="dropdown-item" style={{ cursor: "pointer" }} onClick={onOpen}>Load Novel</div>
            <div className="dropdown-item" style={{ cursor: "pointer" }} onClick={onEdit}>Edit Novel</div>
        </div>
  );
}

export function Navbar() {
    const [NovelActive, setNovelActive] = useState(false);
    const { setModalContent, selectedNovel } = useContext(AppContext);

    function handleNovelClick() {
        setNovelActive(true);
    }

    const menuRef = useRef<HTMLDivElement>(null);

    useOutsideClick(menuRef, () => {
        setNovelActive(false);
    });

    return (
        <nav className="navbar navbar-dark bg-dark py-2">
            <div className="container-fluid">
                <div className="d-flex gap-5 align-items-center">
                    <div className="position-relative" ref={menuRef}>
                        <button
                            className="btn btn-outline-light btn-sm"
                            onClick={handleNovelClick}
                        >
                            {!selectedNovel
                            ? "Novel"
                            : selectedNovel.title.length > 10
                                ? "Novel: " + selectedNovel.title.slice(0, 7) + "..."
                                : "Novel: " + selectedNovel.title
                            }
                        </button>

                        <NovelMenu
                            open={NovelActive}
                            onNew={() => setModalContent(<CreateNovelModal />)}
                            onOpen={() => setModalContent(<LoadNovelModal />)}
                            onEdit={() => setModalContent(<EditNovelModal />)}
                        />
                    </div>

                    <Link className="nav-link text-white" to="/chapter">Chapter</Link>
                    <Link className="nav-link text-white" to="/character">Character</Link>
                    <Link className="nav-link text-white" to="/editor">Editor</Link>
                </div>

                <span className="navbar-brand">
                    Noob Writing Aid
                </span>

            </div>
        </nav>
    );
}

// import { Link } from "react-router-dom";
import { useState } from "react";
import { CreateNovelModal, LoadNovelModal } from "../modal/NovelModal";

export function NovelMenu({ open, onNew, onOpen }: { open: boolean, onNew: () => void, onOpen: () => void }) {
  if (!open) return null;

  return (
        <div
            className="position-absolute bg-white text-dark border rounded shadow"
            style={{ top: "100%", left: 0, marginTop: "5px", minWidth: "150px", padding: "5px 5px", zIndex: 1000 }}>
            <div className="dropdown-item" style={{ cursor: "pointer" }} onClick={onNew}>Create New Novel</div>
            <div className="dropdown-item" style={{ cursor: "pointer" }} onClick={() => alert("Feature not implemented yet")}>Load Novel</div>
            <div className="dropdown-item" style={{ cursor: "pointer" }} onClick={() => alert("Feature not implemented yet")}>Delete Novel</div>
        </div>
  );
}

export function Navbar({openModal}: { openModal: (content: React.ReactNode) => void }) {
    const [NovelActive, setNovelActive] = useState(false);

    function handleNovelClick() {
        setNovelActive(prev => !prev);
    }

    return (
        <nav className="navbar navbar-dark bg-dark p-2">
            <div className="container-fluid">
                <div className="d-flex gap-5 align-items-center">
                    <div className="position-relative">
                        <button
                            className="btn btn-outline-light btn-sm px-3"
                            onClick={handleNovelClick}
                        >
                            Novel
                        </button>

                        <NovelMenu
                            open={NovelActive}
                            onNew={() => openModal(<CreateNovelModal />)}
                            onOpen={() => openModal(<LoadNovelModal />)}
                        />
                    </div>

                    {/* <Link className="nav-link text-white" to="/chapter">Chapter</Link>
                    <Link className="nav-link text-white" to="/character">Character</Link>
                    <Link className="nav-link text-white" to="/editor">Editor</Link> */}
                </div>

                <span className="navbar-brand">
                    Noob Writing Aid
                </span>

            </div>
        </nav>
    );
}

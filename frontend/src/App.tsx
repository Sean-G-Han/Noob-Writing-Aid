import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/navbar/Navbar";
import { useState } from "react";
import { Modal } from "./components/modal/Modal";
import { AppContext } from "./AppContext";
import type { Chapter, Novel } from "./types";
import { ChapterPage } from "./components/page/Chapter";
import { WritingEditor } from "./components/page/Editor";

function App() {
    const [modalContent, setModalContent] = useState<React.ReactNode>(null);
    const [selectedNovel, setSelectedNovel] = useState<Novel | null>(null);
    const [selectedChapter, setSelectedChapter] = useState<Chapter | null>(null);

    const closeModal = () => setModalContent(null);

    return (
        <AppContext.Provider
            value={{
                selectedNovel,
                setSelectedNovel,
                selectedChapter,
                setSelectedChapter,
                modalContent,
                setModalContent,
                closeModal,
            }}
        >
            <Router>
                <div className="d-flex flex-column vh-100">
                    <Navbar/>

                    <div className="flex-grow-1">
                        <Routes>
                            <Route path="/" element={<ChapterPage />} />
                            <Route path="/chapter" element={<ChapterPage />} />
                            <Route path="/editor" element={<WritingEditor />} />
                        </Routes>
                    </div>
                    <Modal />
                </div>
            </Router>
        </AppContext.Provider>
    );
}

export default App;
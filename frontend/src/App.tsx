import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/navbar/Navbar";
import { useState } from "react";
import { Modal } from "./components/modal/Modal";
import { AppContext } from "./AppContext";
import type { Chapter, Novel } from "./types";
import { ChapterPage } from "./components/page/Chapter";

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
                            <Route path="/character" element={<CharacterPage />} />
                            <Route path="/editor" element={<EditorPage />} />
                        </Routes>
                    </div>
                    <Modal />
                </div>
            </Router>
        </AppContext.Provider>
    );
}

function CharacterPage() {
  return (
        <div className="w-100 h-100 p-3">
            <h1>Character Page</h1>
        </div>
  );
}

function EditorPage() {
  return (
        <div className="w-100 h-100 p-3">
            <h1>Editor Page</h1>
        </div>
  );
}
export default App;
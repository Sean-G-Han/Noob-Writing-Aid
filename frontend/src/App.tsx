import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/navbar/Navbar";
import { useContext, useState } from "react";
import { Modal } from "./components/modal/Modal";
import { AppContext } from "./AppContext";
import { Chapter } from "./components/page/Chapter";
import type { Novel } from "./types";

function App() {
    const [modalContent, setModalContent] = useState<React.ReactNode>(null);
    const [selectedNovel, setSelectedNovel] = useState<Novel | null>(null);

    const closeModal = () => setModalContent(null);

    return (
        <AppContext.Provider
            value={{
                selectedNovel,
                setSelectedNovel,
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
                            <Route path="/" element={<Main />} />
                            <Route path="/chapter" element={<Chapter />} />
                            <Route path="/character" element={<Character />} />
                            <Route path="/editor" element={<Editor />} />
                        </Routes>
                    </div>
                    <Modal />
                </div>
            </Router>
        </AppContext.Provider>
    );
}



function Main() {
    const {selectedNovel} = useContext(AppContext);
    return (
        <div className="w-100 h-100 p-3">
            <h1>Novel {selectedNovel?.title} </h1>
        </div>
    );
}

function Character() {
  return (
        <div className="w-100 h-100 p-3">
            <h1>Character Page</h1>
        </div>
  );
}

function Editor() {
  return (
        <div className="w-100 h-100 p-3">
            <h1>Editor Page</h1>
        </div>
  );
}
export default App;
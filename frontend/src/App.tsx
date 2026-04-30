import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/navbar/Navbar";
import { useState } from "react";
import { Modal } from "./components/modal/Modal";

function App() {
    const [modalContent, setModalContent] = useState<React.ReactNode>(null);

    function openModal(content: React.ReactNode) {
        setModalContent(content);
    }

    function closeModal() {
        setModalContent(null);
    }

    return (
        <Router>
            <div className="d-flex flex-column vh-100">
                <Navbar openModal={openModal} />

                <div className="flex-grow-1">
                    <Routes>
                        <Route path="/" element={<File />} />
                        <Route path="/file" element={<File />} />
                        <Route path="/chapter" element={<Chapter />} />
                        <Route path="/character" element={<Character />} />
                        <Route path="/editor" element={<Editor />} />
                    </Routes>
                </div>

                <Modal open={!!modalContent} onClose={closeModal}>
                    {modalContent}
                </Modal>
            </div>
        </Router>
    );
}



function File() {
    return (
        <div className="w-100 h-100 p-3">
            <h1>File Page</h1>
        </div>
    );
}

function Chapter() {
    return (
        <div className="w-100 h-100 p-3">
            <h1>Chapter Page</h1>
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
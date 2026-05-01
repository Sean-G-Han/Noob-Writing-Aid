import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/navbar/Navbar";
import { useContext, useState } from "react";
import { Modal } from "./components/modal/Modal";
import { AppContext } from "./AppContext";

function App() {
    const [modalContent, setModalContent] = useState<React.ReactNode>(null);
    const [selectedNovelId, setSelectedNovelId] = useState<number | null>(null);

    const closeModal = () => setModalContent(null);

    return (
        <AppContext.Provider
            value={{
                selectedNovelId,
                setSelectedNovelId,
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
    const {selectedNovelId} = useContext(AppContext);
    return (
        <div className="w-100 h-100 p-3">
            <h1>Novel {selectedNovelId} </h1>
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
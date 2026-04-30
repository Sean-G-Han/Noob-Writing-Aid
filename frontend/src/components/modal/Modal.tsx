import { ModalContext } from "./ModalContext";

export function Modal({ open, onClose, children }: { open: boolean, onClose: () => void, children: React.ReactNode }) {
    if (!open) return null;

    return (
        <>
            <div
                className="position-fixed top-0 start-0 w-100 h-100 bg-dark"
                style={{ opacity: 0.5, zIndex: 1040 }}
                onClick={onClose}
            />

            <div
                className="position-fixed top-50 start-50 translate-middle bg-white rounded shadow p-4"
                style={{ zIndex: 1050, minWidth: "500px" }}
            >
                <div className="d-flex justify-content-end">
                <button className="btn-close" onClick={onClose}></button>
                </div>

                <ModalContext.Provider value={{ onClose }}>
                    {children}
                </ModalContext.Provider>
            </div>
        </>
    );
}
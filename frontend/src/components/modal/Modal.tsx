import { useContext, useRef } from "react";
import { AppContext } from "../../AppContext";
import { useOutsideClick } from "../../hooks/useOutsideClick";

export function Modal() {
    const { modalContent, closeModal } = useContext(AppContext);

    const menuRef = useRef<HTMLDivElement>(null);

    useOutsideClick(menuRef, () => {
        closeModal();
    });

    if (!modalContent) return null;

    return (
        <>
            <div
                className="position-fixed top-0 start-0 w-100 h-100 bg-dark"
                style={{ opacity: 0.5, zIndex: 1040 }}
            />

            <div
                className="position-fixed top-50 start-50 translate-middle bg-white rounded shadow p-4"
                style={{ zIndex: 1050, minWidth: "550px" }}
                ref={menuRef}
            >
                <div className="d-flex justify-content-end my-2">
                    <button className="btn-close" onClick={closeModal}></button>
                </div>

                {modalContent}
            </div>
        </>
    );
}
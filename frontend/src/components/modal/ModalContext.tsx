import { createContext } from "react";

export const ModalContext = createContext<{ onClose: () => void }>({ 
    onClose: () => {}
});

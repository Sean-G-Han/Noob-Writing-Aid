import { createContext } from "react";

type AppContextType = {
    selectedNovelId: number | null;
    setSelectedNovelId: (id: number | null) => void;

    modalContent: React.ReactNode | null;
    setModalContent: (content: React.ReactNode | null) => void;
    closeModal: () => void;
};

export const AppContext = createContext<AppContextType>({
    selectedNovelId: null,
    setSelectedNovelId: () => {},

    modalContent: null,
    setModalContent: () => {},
    closeModal: () => {},
});
// export const AppContext = createContext<AppContextType>({
//     selectedNovelId: null,
//     // YH Note: This value is ONLY a fallback/default. 
//     // This does NOT make the variable live or reactive.
//     // Without pairing this with a useState hook in a Provider, 
//     // the value is essentially a global constant that cannot trigger UI updates.
//     // This is because React only triggers a re-render when state (useState) 
//     // or props change; modifying this object directly updates the memory 
//     // address but fails to notify React to repaint the UI.
// });
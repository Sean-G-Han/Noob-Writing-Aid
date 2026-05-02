import { useEffect, useState, useContext } from "react";
import { AppContext } from "../../../AppContext";
import type { Character } from "../../../types";
import { getAllCharacters, getCharacters, linkCharacter, unlinkCharacter } from "../../../api/CharacterAPI";


type LinkCharacterModalProps = {
    onUpdate: () => void;
};

export function LinkCharacterModal({ onUpdate }: LinkCharacterModalProps) {
    const { selectedChapter, selectedNovel } = useContext(AppContext);

    const [linked, setLinked] = useState<Character[]>([]);
    const [allCharacters, setAllCharacters] = useState<Character[]>([]);
    const [error, setError] = useState("");

    async function refreshData() {
        if (!selectedChapter || !selectedNovel) return;

        getCharacters(selectedChapter.id).then((res) => {
            if (res.ok) setLinked(res.result);
            else setError(res.error);
        });

        getAllCharacters(selectedNovel.id).then((res) => {
            if (res.ok) setAllCharacters(res.result);
            else setError(res.error);
        });
    }

    useEffect(() => {
        refreshData()
    }, [selectedChapter, selectedNovel]);

    if (!selectedChapter) {
        return <div>No chapter selected</div>;
    }

    const linkedIds = new Set(linked.map((c) => c.id));
    const available = allCharacters.filter((c) => !linkedIds.has(c.id));

    function handleLink(character: Character) {
        if (!selectedChapter)
            return 
        linkCharacter(selectedChapter.id, character.id)
        .then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                onUpdate();
                refreshData()
            }
        })
    }

    function handleUnlink(character: Character) {
        if (!selectedChapter)
            return 
        unlinkCharacter(selectedChapter.id, character.id)
        .then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                onUpdate();
                refreshData()
            }
        })
    }

    return (
        <div>
            <h5 className="mb-3">Manage Character Links</h5>

            {error && <div className="alert alert-danger">{error}</div>}

            <div className="mb-4">
                <h6>Current</h6>
                {linked.length === 0 && (
                    <div className="text-muted">No characters linked</div>
                )}

                {linked.map((character) => (
                    <div
                        key={character.id}
                        className="d-flex justify-content-between align-items-center border rounded p-2 mb-2"
                    >
                        <div>{character.common_name}</div>

                        <button
                            className="btn btn-sm btn-danger"
                            onClick={() => handleUnlink(character)}
                        >
                            Unlink
                        </button>
                    </div>
                ))}
            </div>

            <div>
                <h6>Available</h6>
                {available.length === 0 && (
                    <div className="text-muted">No available characters</div>
                )}

                {available.map((character) => (
                    <div
                        key={character.id}
                        className="d-flex justify-content-between align-items-center border rounded p-2 mb-2"
                    >
                        <div>{character.common_name}</div>

                        <button
                            className="btn btn-sm btn-success"
                            onClick={() => handleLink(character)}
                        >
                            Link
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
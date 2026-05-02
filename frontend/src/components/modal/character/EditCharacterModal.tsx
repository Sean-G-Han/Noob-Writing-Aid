import { useState, useContext } from "react";
import { AppContext } from "../../../AppContext";
import type { Character } from "../../../types";
import { editCharacter } from "../../../api/CharacterAPI";

type EditCharacterModalProps = {
    character: Character;
    onUpdate: (updated: Character) => void;
};

export function EditCharacterModal({
    character,
    onUpdate,
}: EditCharacterModalProps) {
    const { closeModal } = useContext(AppContext);
    const [error, setError] = useState("");

    const [commonName, setCommonName] = useState(character.common_name);
    const [description, setDescription] = useState(character.description ?? "");

    const [adjectives, setAdjectives] = useState(
        character.adjectives?.join(", ") ?? ""
    );

    const [pronouns, setPronouns] = useState(
        character.pronouns?.join(", ") ?? ""
    );

    const [alternativeNames, setAlternativeNames] = useState(
        character.alternative_names?.join(", ") ?? ""
    );

    function handleEditCharacter() {
        editCharacter(character.id, {
            common_name: commonName,
            description: description,
            adjectives: adjectives
                ? adjectives.split(",").map((s) => s.trim())
                : [],
            pronouns: pronouns
                ? pronouns.split(",").map((s) => s.trim())
                : [],
            alternative_names: alternativeNames
                ? alternativeNames.split(",").map((s) => s.trim())
                : [],
        }).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                onUpdate(res.result);
                closeModal();
            }
        });
    }

    return (
        <>
            <h5 className="mb-0">Update Character</h5>

            <input
                className="form-control my-2"
                value={commonName}
                placeholder="Common name"
                onChange={(e) => setCommonName(e.target.value)}
            />

            <textarea
                className="form-control my-2"
                value={description}
                placeholder="Description"
                onChange={(e) => setDescription(e.target.value)}
            />

            <input
                className="form-control my-2"
                value={adjectives}
                placeholder="Adjectives (comma separated)"
                onChange={(e) => setAdjectives(e.target.value)}
            />

            <input
                className="form-control my-2"
                value={pronouns}
                placeholder="Pronouns (comma separated)"
                onChange={(e) => setPronouns(e.target.value)}
            />

            <input
                className="form-control my-2"
                value={alternativeNames}
                placeholder="Alternative names (comma separated)"
                onChange={(e) => setAlternativeNames(e.target.value)}
            />

            {error && <div className="alert alert-danger">{error}</div>}

            <button
                className="btn btn-primary w-100 my-3"
                onClick={handleEditCharacter}
            >
                Update
            </button>
        </>
    );
}
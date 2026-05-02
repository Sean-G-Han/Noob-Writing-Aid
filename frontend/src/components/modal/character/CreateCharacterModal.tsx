import { useState, useContext } from "react";
import { AppContext } from "../../../AppContext";
import type { Character } from "../../../types";
import {
    createCharacter,
    type CreateCharacterRequest,
} from "../../../api/CharacterAPI";

type CreateCharacterModalProps = {
    onCreate: (created: Character) => void;
};

export function CreateCharacterModal({ onCreate }: CreateCharacterModalProps) {
    const [commonName, setCommonName] = useState("");
    const [description, setDescription] = useState("");
    const [adjectives, setAdjectives] = useState("");
    const [pronouns, setPronouns] = useState("");
    const [alternativeNames, setAlternativeNames] = useState("");
    const [error, setError] = useState("");

    const { closeModal, selectedNovel, selectedChapter } =
        useContext(AppContext);

    function handleCreateCharacter() {
        if (!selectedNovel || !selectedChapter) {
            alert("No novel or chapter selected");
            return;
        }

        const data: CreateCharacterRequest = {
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
            chapters: [selectedChapter.id],
        };

        createCharacter(data).then((res) => {
            if (!res.ok) {
                setError(res.error);
            } else {
                onCreate(res.result);
                closeModal();
            }
        });
    }

    return (
        <>
            <div className="row align-items-center">
                <div className="col-4">
                    <h5 className="mb-0">Create Character</h5>
                </div>
            </div>

            <input
                className="form-control my-2"
                placeholder="Common name"
                value={commonName}
                onChange={(e) => setCommonName(e.target.value)}
            />

            <textarea
                className="form-control my-2"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />

            <input
                className="form-control my-2"
                placeholder="Adjectives (comma separated)"
                value={adjectives}
                onChange={(e) => setAdjectives(e.target.value)}
            />

            <input
                className="form-control my-2"
                placeholder="Pronouns (comma separated)"
                value={pronouns}
                onChange={(e) => setPronouns(e.target.value)}
            />

            <input
                className="form-control my-2"
                placeholder="Alternative names (comma separated)"
                value={alternativeNames}
                onChange={(e) => setAlternativeNames(e.target.value)}
            />

            {error && <div className="alert alert-danger">{error}</div>}

            <button
                className="btn btn-primary w-100 my-3"
                onClick={handleCreateCharacter}
            >
                Create
            </button>
        </>
    );
}
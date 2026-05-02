import { useContext, useState } from "react";
import { gradeChapterContent, loadChapterContent, saveChapterContent } from "../../api/ContentAPI";
import { AppContext } from "../../AppContext";


/* =========================
    TOP BAR
========================= */

function TopBar({
    onSave,
    onLoad,
    onAnalyze,
}: {
    onSave: () => void;
    onLoad: () => void;
    onAnalyze: () => void;
}) {
    return (
        <div className="card bg-dark text-white mb-3">
            <div className="card-body d-flex justify-content-between align-items-center">
                <h5 className="mb-0">Noob Writing Assistant</h5>

                <div className="d-flex gap-2">
                    <button
                        className="btn btn-outline-light btn-sm"
                        onClick={onLoad}
                    >
                        Load
                    </button>

                    <button
                        className="btn btn-outline-light btn-sm"
                        onClick={onSave}
                    >
                        Save
                    </button>

                    <button
                        className="btn btn-success btn-sm"
                        onClick={onAnalyze}
                    >
                        Analyze
                    </button>
                </div>
            </div>
        </div>
    );
}

/* =========================
    INPUT
========================= */

function InputPanel({
    text,
    setText,
}: {
    text: string;
    setText: (v: string) => void;
}) {
    return (
        <div className="col-md-6">
            <div className="card h-100">
                <div className="card-header">Input</div>

                <div className="card-body p-0">
                    <textarea
                        className="form-control border-0"
                        style={{
                            minHeight: "70vh",
                            resize: "none",
                        }}
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Start writing here..."
                    />
                </div>
            </div>
        </div>
    );
}

/* =========================
    OUTPUT
========================= */

function OutputPanel({ analysis }: { analysis: string }) {
    return (
        <div className="col-md-6">
            <div className="card h-100">
                <div className="card-header">Analysis</div>

                <div className="card-body">
                    {analysis ? (
                        <pre style={{ whiteSpace: "pre-wrap" }}>
                            {analysis}
                        </pre>
                    ) : (
                        <span className="text-muted">
                            No analysis yet
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
}

/* =========================
    MAIN
========================= */

export function WritingEditor() {
    const [text, setText] = useState("");
    const [analysis, setAnalysis] = useState("");
    const { selectedChapter } = useContext(AppContext)

    async function handleSave() {
        if (!selectedChapter)
            return
        const res = await saveChapterContent(selectedChapter.id, {
            content: text,
        });

        if (res.ok) {
            alert("Saved successfully");
        } else {
            alert("Save failed: " + res.error);
        }
    }

    async function handleLoad() {
        if (!selectedChapter)
            return
        const res = await loadChapterContent(selectedChapter.id);

        if (res.ok) {
            setText(res.result.content);
        } else {
            alert("Load failed: " + res.error);
        }
    }

    async function handleAnalyze() {
        if (!selectedChapter)
            return
        const res = await gradeChapterContent(selectedChapter.id);

        if (res.ok) {
            setAnalysis(res.result.annotatedText);
        } else {
            alert("Analyze failed: " + res.error);
        }
    }

    return (
        <div className="container-fluid py-3">

            <TopBar
                onSave={handleSave}
                onLoad={handleLoad}
                onAnalyze={handleAnalyze}
            />

            <div className="row g-3">
                <InputPanel text={text} setText={setText} />
                <OutputPanel analysis={analysis} />
            </div>

        </div>
    );
}
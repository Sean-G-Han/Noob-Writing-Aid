import { useContext, useState } from "react";
import { gradeChapterContent, loadChapterContent, saveChapterContent } from "../../api/ContentAPI";
import { AppContext } from "../../AppContext";
import { NodeParser } from "../components/NodeParser";

type TopBarProps = {
    onSave: () => void;
    onLoad: () => void;
    onAnalyze: () => void;
};

function TopBar({ onSave, onLoad, onAnalyze }: TopBarProps) {
    return (
        <div className="d-flex justify-content-between align-items-center bg-dark text-white px-3 py-2 rounded mb-2 shadow-sm">
            <div className="fw-semibold">Noob Writing Assistant</div>

            <div className="d-flex gap-2">
                <button className="btn btn-outline-light btn-sm" onClick={onLoad}>
                    Load
                </button>

                <button className="btn btn-outline-light btn-sm" onClick={onSave}>
                    Save
                </button>

                <button className="btn btn-success btn-sm" onClick={onAnalyze}>
                    Analyze
                </button>
            </div>
        </div>
    );
}

type InputPanelProps = {
    text: string;
    setText: (text: string) => void;
};

function InputPanel({ text, setText }: InputPanelProps) {
    return (
        <div className="col-md-6 h-100">
            <div className="bg-white rounded shadow-sm h-100 d-flex flex-column overflow-hidden">
                
                <div className="px-3 py-2 border-bottom fw-semibold">
                    Input
                </div>

                <textarea
                    className="form-control border-0 flex-grow-1 p-3"
                    style={{
                        resize: "none",
                        outline: "none",
                        boxShadow: "none",
                        fontFamily: "inherit",
                    }}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Start writing here..."
                />
            </div>
        </div>
    );
}

type OutputPanelProps = {
    analysis: string;
};

function OutputPanel({ analysis }: OutputPanelProps) {
    return (
        <div className="col-md-6 h-100">
            <div className="bg-white rounded shadow-sm h-100 d-flex flex-column overflow-hidden">

                <div className="px-3 py-2 border-bottom fw-semibold">
                    Analysis
                </div>

                <div className="flex-grow-1 overflow-auto p-3">
                    {analysis ? (
                        <NodeParser text={analysis} />
                    ) : (
                        <div className="text-muted">
                            No analysis yet
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}

export function WritingEditor() {
    const [text, setText] = useState("");
    const [analysis, setAnalysis] = useState("");
    const { selectedChapter } = useContext(AppContext);

    async function handleSave() {
        if (!selectedChapter) return;

        const res = await saveChapterContent(selectedChapter.id, { content: text });
        alert(res.ok ? "Saved" : res.error);
    }

    async function handleLoad() {
        if (!selectedChapter) return;

        const res = await loadChapterContent(selectedChapter.id);
        if (res.ok) setText(res.result.content);
        else alert(res.error);
    }

    async function handleAnalyze() {
        if (!selectedChapter) return;

        const res = await gradeChapterContent(selectedChapter.id);
        if (res.ok) setAnalysis(res.result.annotatedText);
        else alert(res.error);
    }

    return (
        <div
            className="d-flex flex-column px-3 py-2"
            style={{ height: "calc(100vh - 78px)", background: "#f5f6f8" }}
        >
            <TopBar
                onSave={handleSave}
                onLoad={handleLoad}
                onAnalyze={handleAnalyze}
            />

            <div className="row flex-grow-1 g-3" style={{ minHeight: 0 }}>
                <InputPanel text={text} setText={setText} />
                <OutputPanel analysis={analysis} />
            </div>
        </div>
    );
}
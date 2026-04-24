import React, { useState } from "react";
import "./panel.css";
import "./tooltip.css";
import type { Node, Severity } from "./types";
import { NodeFactory } from "./types";

const SEVERITY_COLORS: Record<Severity, { bg: string; border: string }> = {
    "3": { bg: "rgba(255, 69, 58, 0.25)", border: "#ff453a" },
    "2": { bg: "rgba(255, 159, 10, 0.25)", border: "#ff9f0a" },
    "1": { bg: "rgba(255, 214, 10, 0.35)", border: "#ffd60a" },
    "default": { bg: "rgba(0, 0, 0, 0.05)", border: "#999" },
};

function parseRecursive(input: string): Node[] { 
    let charIndex = 0;

    function flushTextBuffer(buffer: string, nodes: Node[]) {
        if (buffer) {
            nodes.push(NodeFactory.text(buffer));
            buffer = "";
        }
        return buffer;
    }
    
    function parse(): Node[] { 
        const nodes: Node[] = []; 
        let textBuffer = ""; 

        while (charIndex < input.length) {
            if (input[charIndex] === "]") {
                textBuffer = flushTextBuffer(textBuffer, nodes);
                charIndex++;
                return nodes;
            }

            if (input[charIndex] === "[") { 
                textBuffer = flushTextBuffer(textBuffer, nodes);

                const severityEnd = input.indexOf(")", charIndex); 
                const annotationEnd = input.indexOf(")", severityEnd + 1); 

                const sevMatch = input.slice(charIndex + 1, severityEnd).match(/Severity:\s*(\d)/);
                const severityStr: Severity = sevMatch ? (sevMatch[1] as Severity) : "default";
                const content = input.slice(severityEnd + 1, annotationEnd);
                const errorType = [...content.matchAll(/([A-Z]+):/g)].map(m => m[1]);

                charIndex = annotationEnd + 1;

                const children = parse(); 

                console.log("Content:", content);
                console.log("Severity:", severityStr);
                console.log("Error Type:", errorType);
                nodes.push(NodeFactory.annotation(content, severityStr, errorType, children)); 

            } else { 
                textBuffer += input[charIndex]; 
                charIndex++; 
            }
        }

        if (textBuffer) 
            nodes.push({ type: "text", content: textBuffer }); 

        return nodes; 
        
    } 
    return parse(); 
}

const TooltipPortal: React.FC<{tooltip: { text: string; x: number; y: number } | null;}> = ({ tooltip }) => {
    if (!tooltip) return null;

    function cleanTooltipText(text: string): string {
        return text.replace(")(", "")
                   .replace(/^[ \t]*[, (]+|[, \t)]+[ \t]*$/g, "")
                   .trim();
    }

    return (
        <div
            className="tooltip"
            style={{
                left: tooltip.x,
                top: tooltip.y,
            }}
        >
            {cleanTooltipText(tooltip.text)}
        </div>
    );
};

const NodeRenderer: React.FC<{
    node: Node; 
    setTooltip: (t: { text: string; x: number; y: number } | null) => void;
    activeTypes: string[] 
}> = ({ node, setTooltip, activeTypes }) => {
    if (node.type === "text") return <span>{node.content}</span>;

    const normalizedTypes = node.errorType.map(t => t.trim().toLowerCase());

    const isActive = normalizedTypes.some(t =>
        activeTypes.map(a => a.toLowerCase()).includes(t)
    );

    if (!isActive) {
        return (
            <>
                {node.children.map((child, i) => (
                    <NodeRenderer key={i} node={child} setTooltip={setTooltip} activeTypes={activeTypes} />
                ))}
            </>
        );
    }

    const colors = SEVERITY_COLORS[node.severity] || SEVERITY_COLORS.default;

    return (
        <span 
            className={["hl-node", ...normalizedTypes.map(t => `hl-node-${t}`)].join(" ")}
            style={{
                backgroundColor: colors.bg,
                borderBottom: `2px solid ${colors.border}`,
            }}
            onMouseEnter={(e) => {
                e.stopPropagation();
                const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
                setTooltip({ text: node.content, x: rect.left + rect.width / 2, y: rect.top });
            }}
            onMouseLeave={() => setTooltip(null)}
        >
            {node.children.map((child, i) => (
                <NodeRenderer key={i} node={child} setTooltip={setTooltip} activeTypes={activeTypes} />
            ))}
        </span>
    );
};
function WritingAnalyzerApp() {
    const [text, setText] = useState<string>("");
    const [analysis, setAnalysis] = useState<string>("");
    const ERROR_TYPES = ["Grammar", "Style", "Clarity", "Spelling"];
    const [activeTypes, setActiveTypes] = useState<string[]>(ERROR_TYPES);

    const [tooltip, setTooltip] = useState<{
        text: string;
        x: number;
        y: number;
    } | null>(null);

    const runAnalysis = async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/grade", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text }),
            });
            const data: { annotatedText?: string } = await res.json();
            console.log("Received annotated text:", data.annotatedText);
            setAnalysis(data.annotatedText || "");
        } catch (err) {
            console.error("Fetch failed", err);
        }
    };

    const toggleType = (type: string) => {
        setActiveTypes(prev => 
            prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
        );
    };

    return (
        <div style={{ padding: "20px" }}>
            <div className="header-container">
                <h2 style={{ color: "white" }}>Noob Writing Assistant</h2>
                
                <div className="button-group">
                    {ERROR_TYPES.map(type => (
                        <button 
                            key={type}
                            className={`toggle-btn ${activeTypes.includes(type) ? 'active' : ''}`}
                            onClick={() => toggleType(type)}
                        >
                            {type}
                        </button>
                    ))}
                </div>

                <button className="analyze-button" onClick={runAnalysis}>Analyze</button>
            </div>

            <div className="grid-container">
                <div className="panel">
                    <textarea
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        placeholder="Start writing here..."
                        className="panel-textarea"
                    />
                </div>
                <div className="panel">
                    <div className="output-panel">
                        {!analysis ? (
                                <span style={{ color: "#aaa" }}>Suggestions...</span>
                            ) : (
                                parseRecursive(analysis).map((node, i) => (
                                    <NodeRenderer
                                        key={i}
                                        node={node}
                                        setTooltip={setTooltip}
                                        activeTypes={activeTypes}
                                    />
                                ))
                            )
                        }
                    </div>
                </div>
            </div>

            <TooltipPortal tooltip={tooltip} />
        </div>
    );
}

export default WritingAnalyzerApp;
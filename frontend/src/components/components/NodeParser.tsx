import React, { useState } from "react";

type Correct = { type: "text"; value: string };

type Wrong = {
    type: "span";
    severity: number;
    critics: { type: string; message: string }[];
    children: Node[];
};

type Node = Correct | Wrong;

function parse(text: string, i = 0): { node: Node[]; next: number } {
    const nodes: Node[] = [];
    let buffer = "";

    while (i < text.length) {
        const char = text[i];

        if (char === "\n") {
            if (buffer) {
                nodes.push({ type: "text", value: buffer });
                buffer = "";
            }
            nodes.push({ type: "text", value: "\n" });
            i++;
            continue;
        }

        if (char === "[") {
            if (buffer) {
                nodes.push({ type: "text", value: buffer });
                buffer = "";
            }

            i++;

            const sevStart = text.indexOf("<", i);
            const sevEnd = text.indexOf(">", sevStart);
            const severity = Number(text.slice(sevStart + 1, sevEnd));

            i = sevEnd + 1;

            const errStart = text.indexOf("(", i);
            const errEnd = text.indexOf(")", errStart);

            const rawErrors = text
                .slice(errStart + 1, errEnd)
                .split("|")
                .map((e) => {
                    const [type, message] = e.split(":");
                    return {
                        type: type.trim(),
                        message: message?.trim() ?? "",
                    };
                });

            i = errEnd + 1;

            const childStart = i;
            let depth = 1;

            while (i < text.length && depth > 0) {
                if (text[i] === "[") depth++;
                if (text[i] === "]") depth--;
                i++;
            }

            const childText = text.slice(childStart, i - 1);
            const children = parse(childText).node;

            nodes.push({
                type: "span",
                severity,
                critics: rawErrors,
                children,
            });

            continue;
        }

        if (char === "]") {
            break;
        }

        buffer += char;
        i++;
    }

    if (buffer) {
        nodes.push({ type: "text", value: buffer });
    }

    return { node: nodes, next: i };
}

function getSeverityStyle(severity: number): string {
    switch (severity) {
        case 1:
            return "border-warning text-dark bg-warning bg-opacity-10";
        case 2:
            return "border-warning text-dark bg-warning bg-opacity-25";
        case 3:
            return "border-danger text-dark bg-danger bg-opacity-25";
        default:
            return "";
    }
}

function Tooltip({
    tooltip,
}: {
    tooltip: { text: string; x: number; y: number } | null;
}) {
    if (!tooltip) return null;

    return (
        <div
            className="position-fixed bg-dark text-white p-2 rounded shadow"
            style={{
                left: tooltip.x + 10,
                top: tooltip.y + 10,
                zIndex: 9999,
                maxWidth: "300px",
                whiteSpace: "pre-wrap",
                pointerEvents: "none",
                fontSize: "10px",
            }}
        >
            {tooltip.text}
        </div>
    );
}

function render(nodes: Node[], setTooltip: any): React.ReactNode {
    return nodes.map((n, i) => {
        if (n.type === "text") {
            if (n.value === "\n") return <div key={i} style={{ height: "0.75rem" }} />;
            return <span key={i}>{n.value}</span>;
        }

        const tooltipText = n.critics
            .map((e) => `${e.type}: ${e.message}`)
            .join("\n");

        return (
            <span
                key={i}
                className={`border-bottom px-1 rounded ${getSeverityStyle(n.severity)}`}
                onMouseEnter={(e) => {
                    const rect = (e.target as HTMLElement).getBoundingClientRect();

                    setTooltip({
                        text: tooltipText,
                        x: rect.left,
                        y: rect.bottom,
                    });
                }}
                onMouseLeave={() => setTooltip(null)}
            >
                {render(n.children, setTooltip)}
            </span>
        );
    });
}

export function NodeParser({ text }: { text: string }) {
    const parsed = parse(text).node;

    const [tooltip, setTooltip] = useState<{
        text: string;
        x: number;
        y: number;
    } | null>(null);

    return (
        <div className="p-2">
            {render(parsed, setTooltip)}
            <Tooltip tooltip={tooltip} />
        </div>
    );
}
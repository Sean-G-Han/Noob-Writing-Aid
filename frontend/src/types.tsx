export type Severity = "1" | "2" | "3" | "default";

export interface TextNode {
  type: "text";
  content: string;
}

export interface AnnotationNode {
  type: "annotation";
  errorType: string[];
  severity: Severity;
  content: string;
  children: Node[];
}

export type Node = TextNode | AnnotationNode;

export const NodeFactory = {
    text(content: string): TextNode {
        return { type: "text", content };
    },

    annotation(content: string, severity: Severity, errorType: string[], children: Node[] = []): AnnotationNode {
        return { type: "annotation", severity, errorType, content, children };
    }
};

export type Novel = {
    id: number;
    title: string;
};

export type Chapter = {
    id: number
    novel_id: number
    chapter_number: number
    title: string
    raw_file_path: number | null
    annotated_file_path: string | null
    hash: string | null
};
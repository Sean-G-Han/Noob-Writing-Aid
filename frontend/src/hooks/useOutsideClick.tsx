import { useEffect } from "react";

export function useOutsideClick(
    ref: React.RefObject<HTMLElement | null>,
    handler: () => void
) {
    useEffect(() => {
        function handleMouseDown(event: MouseEvent) {
            const el = ref.current;
            if (!el) return;

            if (!el.contains(event.target as Node)) {
                handler();
            }
        }

        document.addEventListener("mousedown", handleMouseDown);

        return () => {
            document.removeEventListener("mousedown", handleMouseDown);
        };
    }, [ref, handler]);
}
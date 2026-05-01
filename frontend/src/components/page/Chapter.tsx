import { useContext } from "react";
import { AppContext } from "../../AppContext";

export function Chapter() {
    return (
        <div className="row w-100 h-100 align-items-start m-0 p-0">
            <div className="col-6 flex-column d-flex" style={{ height: "100%" }}>
                <ChapterView />
            </div>
            <div className="col-6 flex-column d-flex" style={{ height: "100%" }}>
            </div>
        </div>
    );
}

export function ChapterView() {
    const { selectedNovel } = useContext(AppContext);

    return (
        <div className="w-100 h-100 d-flex flex-column">
            <div className="d-flex justify-content-between align-items-center bg-dark text-white p-2 my-2">
                <div className="fw-bold">
                    {!selectedNovel ? "No Novel Selected" : selectedNovel.title + " - Chapters"}
                </div>

                <button className="btn btn-sm btn-success">
                    +
                </button>
            </div>

            <div className="flex-grow-1 overflow-auto p-3">
                {/* Example items */}
                <div className="border rounded p-2 mb-2">
                    Chapter 1
                </div>
                <div className="border rounded p-2 mb-2">
                    Chapter 2
                </div>
            </div>

        </div>
    );
}
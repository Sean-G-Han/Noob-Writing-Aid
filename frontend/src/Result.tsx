export type Failure = {
    ok: false;
    error: string;
};

export type Success<T> = {
    ok: true;
    result: T;
};

export type Result<T> = Failure | Success<T>;

export function Success<T>(result: T): Success<T> {
    return {ok: true, result};
}

export function Failure(error: string): Failure {   
    return {ok: false, error};
}
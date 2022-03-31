export const getBySelector = (query: string): HTMLElement => {
    const el = document.querySelector<HTMLElement>(query);
    if (!el) {
        throw new Error(`Element with query ${query} was not found`);
    }
    return el;
}

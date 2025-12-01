export function normalizePageText(page: string): string {
  return page.replace(/\s+/g, " ").trim();
}

export function pagesToSingleString(pages: string[]): string {
  return pages
    .map(normalizePageText)
    .filter((p) => p.length > 0)
    .join("\n\n--- PAGE BREAK ---\n\n");
}

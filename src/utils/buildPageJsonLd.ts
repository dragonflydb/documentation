const SITE_URL = "https://www.dragonflydb.io";

// Builds a WebPage JSON-LD node with dateModified for a single doc/category
// page. dateModified prefers the real git-based lastUpdatedAt Docusaurus
// already computes for doc files (ms epoch); category index pages have no
// underlying file, so callers pass a fallback (build time) instead.
//
// Note: BreadcrumbList JSON-LD is intentionally NOT built here -- Docusaurus
// 3.x's DocBreadcrumbs component already emits an accurate one (real sidebar
// titles, not URL-segment guesses) on every doc and category page out of the
// box. Adding a second one here would just create conflicting duplicate
// structured data.
export const buildPageJsonLd = (permalink: string, dateModifiedMs?: number) => {
  const dateModified = new Date(dateModifiedMs ?? Date.now()).toISOString();

  return {
    "@context": "https://schema.org",
    "@type": "WebPage",
    url: `${SITE_URL}${permalink}`,
    dateModified,
  };
};

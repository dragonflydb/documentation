// Builds a WebPage JSON-LD node with dateModified for a single doc/category
// page. dateModified prefers the real git-based lastUpdatedAt Docusaurus
// already computes for doc files (ms epoch); category index pages have no
// underlying file, so callers pass a stable per-build fallback instead (see
// siteConfig.customFields.buildTimeIso) rather than Date.now(), which would
// make the JSON-LD output drift on every rebuild even with no content change.
//
// siteUrl is passed in (from useDocusaurusContext().siteConfig.url) rather
// than hardcoded, so it stays in sync with docusaurus.config.mjs.
//
// Note: BreadcrumbList JSON-LD is intentionally NOT built here -- Docusaurus
// 3.x's DocBreadcrumbs component already emits an accurate one (real sidebar
// titles, not URL-segment guesses) on every doc and category page out of the
// box. Adding a second one here would just create conflicting duplicate
// structured data.
export const buildPageJsonLd = (siteUrl: string, permalink: string, dateModifiedMs: number) => {
  const dateModified = new Date(dateModifiedMs).toISOString();

  return {
    "@context": "https://schema.org",
    "@type": "WebPage",
    url: `${siteUrl}${permalink}`,
    dateModified,
  };
};

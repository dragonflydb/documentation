import Head from "@docusaurus/Head";
import type { WrapperProps } from "@docusaurus/types";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import React from "react";

import { buildPageJsonLd } from "@site/src/utils/buildPageJsonLd";

import CategoryGeneratedIndexPage from "@theme-original/DocCategoryGeneratedIndexPage";
import type CategoryGeneratedIndexPageType from "@theme/DocCategoryGeneratedIndexPage";

type Props = WrapperProps<typeof CategoryGeneratedIndexPageType>;

// Adds per-page JSON-LD (WebPage dateModified) to auto-generated category
// index pages. These have no underlying file, so dateModified uses a single
// timestamp captured once per build (siteConfig.customFields.buildTimeIso)
// rather than Date.now(), so the output doesn't drift across rebuilds that
// don't touch this category.
export default function CategoryGeneratedIndexPageWrapper(props: Props): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const buildTimeMs = Date.parse(String(siteConfig.customFields?.buildTimeIso));
  const jsonLd = buildPageJsonLd(siteConfig.url, props.categoryGeneratedIndex.permalink, buildTimeMs);

  return (
    <>
      <Head>
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Head>
      <CategoryGeneratedIndexPage {...props} />
    </>
  );
}

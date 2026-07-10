import Head from "@docusaurus/Head";
import type { WrapperProps } from "@docusaurus/types";
import React from "react";

import { buildPageJsonLd } from "@site/src/utils/buildPageJsonLd";

import CategoryGeneratedIndexPage from "@theme-original/DocCategoryGeneratedIndexPage";
import type CategoryGeneratedIndexPageType from "@theme/DocCategoryGeneratedIndexPage";

type Props = WrapperProps<typeof CategoryGeneratedIndexPageType>;

// Adds per-page JSON-LD (WebPage + BreadcrumbList) to auto-generated category
// index pages. These have no underlying file, so dateModified falls back to
// build time rather than a real git-based date.
export default function CategoryGeneratedIndexPageWrapper(props: Props): JSX.Element {
  const jsonLd = buildPageJsonLd(props.categoryGeneratedIndex.permalink);

  return (
    <>
      <Head>
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Head>
      <CategoryGeneratedIndexPage {...props} />
    </>
  );
}

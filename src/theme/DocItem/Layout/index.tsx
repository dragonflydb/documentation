import Head from "@docusaurus/Head";
import { useDoc } from "@docusaurus/plugin-content-docs/client";
import type { WrapperProps } from "@docusaurus/types";
import React from "react";

import { buildPageJsonLd } from "@site/src/utils/buildPageJsonLd";

import Layout from "@theme-original/DocItem/Layout";
import type LayoutType from "@theme/DocItem/Layout";

type Props = WrapperProps<typeof LayoutType>;

// Adds per-page JSON-LD (WebPage dateModified + BreadcrumbList) to every doc
// page, sourced from Docusaurus's own git-based lastUpdatedAt metadata.
export default function LayoutWrapper(props: Props): JSX.Element {
  const { metadata } = useDoc();
  const jsonLd = buildPageJsonLd(metadata.permalink, metadata.lastUpdatedAt);

  return (
    <>
      <Head>
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Head>
      <Layout {...props} />
    </>
  );
}

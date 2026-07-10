import Head from "@docusaurus/Head";
import { useDoc } from "@docusaurus/plugin-content-docs/client";
import type { WrapperProps } from "@docusaurus/types";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import React from "react";

import { buildPageJsonLd } from "@site/src/utils/buildPageJsonLd";

import Layout from "@theme-original/DocItem/Layout";
import type LayoutType from "@theme/DocItem/Layout";

type Props = WrapperProps<typeof LayoutType>;

// Adds per-page JSON-LD (WebPage dateModified) to every doc page, sourced
// from Docusaurus's own git-based lastUpdatedAt metadata where available.
export default function LayoutWrapper(props: Props): JSX.Element {
  const { metadata } = useDoc();
  const { siteConfig } = useDocusaurusContext();
  const buildTimeMs = Date.parse(String(siteConfig.customFields?.buildTimeIso));
  const jsonLd = buildPageJsonLd(
    siteConfig.url,
    metadata.permalink,
    metadata.lastUpdatedAt ?? buildTimeMs,
  );

  return (
    <>
      <Head>
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Head>
      <Layout {...props} />
    </>
  );
}

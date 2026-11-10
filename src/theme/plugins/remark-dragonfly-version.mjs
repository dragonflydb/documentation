// @ts-check
// https://www.gatsbyjs.com/plugins/gatsby-remark-find-replace/

import { visit } from "unist-util-visit";

const regexp = /\{{DRAGONFLY_VERSION}}/g;
// version.dragonflydb.io names a release the way GitHub does, which may omit the
// patch number ("2.1" for the v2.1.0 image). Image and Helm chart tags always have
// three numbers, so pad the version to MAJOR.MINOR.PATCH.
const version = normalizeVersion(process.env.DRAGONFLY_VERSION);

function normalizeVersion(raw) {
  const parts = (raw || "").trim().split(".").filter(Boolean);
  if (parts.length === 0) return undefined;
  while (parts.length < 3) parts.push("0");
  return parts.join(".");
}

export default function remarkDragonflyVersion() {
  // Go through all text, html, code, inline code, and links.
  return (root) => {
    if (!version) return;

    visit(root, ["text", "html", "code", "inlineCode", "link"], (node) => {
      if (node.type === "link") {
        node.url = node.url.replace(regexp, version);
      } else {
        node.value = node.value.replace(regexp, version);
      }
    });
  };
}

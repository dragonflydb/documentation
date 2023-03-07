// @ts-check
// https://www.gatsbyjs.com/plugins/gatsby-remark-find-replace/

const visit = require("unist-util-visit");

const regexp = /\{{DRAGONFLY_VERSION}}/g;
const version = process.env.DRAGONFLY_VERSION;

module.exports = () => {
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
};

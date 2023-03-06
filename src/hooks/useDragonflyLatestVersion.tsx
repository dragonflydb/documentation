import { useEffect, useState } from "react";
import { useLocation } from "@docusaurus/router";

const VERSION_VARIABLE = "$VERSION";

const replaceTextInElement = (
  element: Node,
  pattern: string,
  replacement: string
) => {
  for (let node of Array.from(element.childNodes)) {
    switch (node.nodeType) {
      case Node.ELEMENT_NODE:
        replaceTextInElement(node, pattern, replacement);
        break;

      case Node.TEXT_NODE:
        node.textContent = node.textContent.replace(pattern, replacement);
        break;

      case Node.DOCUMENT_NODE:
        replaceTextInElement(node, pattern, replacement);
        break;
    }
  }
};

const useDragonflyLatestVersion = () => {
  const location = useLocation();
  const [version, setVersion] = useState<string>(null);

  useEffect(() => {
    requestAnimationFrame(() => {
      const markdownContentElement = document.querySelector(".markdown");
      const contentText = markdownContentElement.textContent;

      if (!contentText.includes(VERSION_VARIABLE)) return;

      if (version) {
        return replaceTextInElement(
          markdownContentElement,
          VERSION_VARIABLE,
          `v${version}`
        );
      }

      fetch("https://version.dragonflydb.io/v1")
        .then((response) => response.json())
        .then((body) => {
          setVersion(body.latest);
        });
    });
  }, [version, location.pathname]);
};

export default useDragonflyLatestVersion;

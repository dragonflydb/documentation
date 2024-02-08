// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const codeTheme = require("prism-react-renderer/themes/palenight");
const isPreviewDeployment = process.env.VERCEL_ENV === "preview";

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Dragonfly",
  tagline: "Ultra-fast, scalable in-memory datastore",
  url: "https://www.dragonflydb.io",
  baseUrl: isPreviewDeployment ? "/" : "/docs",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "website/favicon.ico",
  trailingSlash: false,

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  headTags: [
    {
      attributes: {
        href: "https://fonts.googleapis.com",
        rel: "preconnect",
      },
      tagName: "link",
    },
    {
      attributes: {
        href: "https://fonts.gstatic.com",
        rel: "preconnect",
        crossorigin: "true",
      },
      tagName: "link",
    },
    {
      attributes: {
        href: "https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=Inter:wght@400;500;600;700&display=swap",
        rel: "stylesheet",
      },
      tagName: "link",
    },
  ],

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl: "https://github.com/dragonflydb/documentation/edit/main/",
          routeBasePath: "/",
          remarkPlugins: [
            require("./src/theme/plugins/remark-dragonfly-version.js"),
          ],
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        pages: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
        googleTagManager: {
          containerId: "GTM-M7MX697",
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        disableSwitch: true,
        defaultMode: "dark",
      },
      navbar: {
        logo: {
          alt: "Dragonfly Logo",
          src: "website/logo.svg",
          href: "https://www.dragonflydb.io",
          target: "_self",
        },
        items: [
          {
            href: "https://www.dragonflydb.io/features",
            label: "Features",
            target: "_self",
          },
          {
            href: "/",
            label: "Docs",
          },
          {
            type: "dropdown",
            label: "Community",
            items: [
              {
                href: "https://github.com/dragonflydb/dragonfly",
                label: "GitHub",
              },
              {
                href: "https://discord.gg/HsPjXGVH85",
                label: "Discord",
              },
            ],
          },
          {
            href: "https://www.dragonflydb.io/blog",
            label: "Blog",
            target: "_self",
          },
          {
            href: "https://www.dragonflydb.io/careers",
            label: "Careers",
            target: "_self",
          },
          {
            href: "https://github.com/dragonflydb/dragonfly",
            className: "nav-github-stars",
            position: "right",
          },
          {
            type: "search",
            position: "right",
          },
          {
            href: "https://www.dragonflydb.io/cloud",
            label: "Dragonfly Cloud",
            target: "_self",
            className: "nav-cta",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        logo: {
          alt: "Dragonfly Logo",
          src: "website/logo.svg",
          href: "https://www.dragonflydb.io",
          target: "_self",
          width: 150,
        },
        links: [
          {
            title: "Dragonfly",
            items: [
              {
                label: "Features",
                href: "https://www.dragonflydb.io/features",
                target: "_self",
              },
              {
                label: "Blog",
                href: "https://www.dragonflydb.io/blog",
                target: "_self",
              },
              {
                label: "Dragonfly Cloud",
                href: "https://www.dragonflydb.io/cloud",
                target: "_self",
              },
            ],
          },
          {
            title: "Developers",
            items: [
              {
                label: "Discord",
                href: "https://discord.gg/HsPjXGVH85",
              },
              {
                label: "GitHub",
                href: "https://github.com/dragonflydb/dragonfly",
              },
            ],
          },
          {
            title: "Company",
            items: [
              {
                label: "Careers",
                href: "https://www.dragonflydb.io/careers",
                target: "_self",
              },
              {
                label: "Privacy",
                href: "https://www.dragonflydb.io/privacy",
                target: "_self",
              },
              {
                label: "Terms of Use",
                href: "https://www.dragonflydb.io/terms",
                target: "_self",
              },
            ],
          },
        ],
        copyright: `
          Copyright © ${new Date().getFullYear()} DragonflyDB Ltd. & <a href="https://github.com/redis/redis-doc/blob/master/LICENSE" target="_blank">others</a>
          <br>
          <em>DragonflyDB Docs is Licensed under the <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International Public License</a></em>
        `,
      },
      prism: {
        theme: codeTheme,
      },
      algolia: {
        appId: "ZXLX1PN8SG",
        apiKey: "abad5ee4b6f688bf466290763737a957",
        indexName: "dragonflydb",
        contextualSearch: true,
        replaceSearchResultPathname: isPreviewDeployment
          ? { from: "/docs/", to: "/" }
          : undefined,

        // Optional: path for search page that enabled by default (`false` to disable it)
        searchPagePath: "search",
      },
    }),
};

module.exports = config;

// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Dragonfly",
  tagline: "Ultra-fast, scalable in-memory datastore",
  url: "https://dragonflydb.io",
  baseUrl: process.env.VERCEL_ENV === "preview" ? "/" : "/docs",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",

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
      navbar: {
        title: "Docs",
        logo: {
          alt: "Dragonfly Logo",
          src: "img/logo.svg",
          srcDark: "img/logo-white.svg",
        },
        items: [
          // {
          //   type: "doc",
          //   docId: "introduction",
          //   position: "left",
          //   label: "Tutorial",
          // },
          {
            href: "https://github.com/dragonflydb/documentation/",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          // {
          //   title: "Docs",
          //   items: [
          //     {
          //       label: "Tutorial",
          //       to: "/docs/intro",
          //     },
          //   ],
          // },
          {
            title: "Community",
            items: [
              {
                label: "GitHub",
                href: "https://github.com/dragonflydb/dragonfly",
              },
              {
                label: "Discord",
                href: "https://discord.gg/HsPjXGVH85",
              },
              {
                label: "Twitter",
                href: "https://twitter.com/dragonflydbio",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Attos Technologies Ltd.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;

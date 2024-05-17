const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

const config = {
  title: 'paradrop - Docs',
  tagline: 'Cybersecurity Asset Management',
  url: 'https://demo.paradrop.io',
  baseUrl: '/docs/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/mr_roboto.png',
  organizationName: 'paradrop',
  projectName: 'paradrop',

  presets: [
    [
      'classic',
      ({
        docs: {
          routeBasePath: "/",
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/MetroStar/paradrop/blob/main/README.md',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    ({
      navbar: {
        title: 'paradrop',
        logo: {
          alt: 'paradrop Logo',
          src: 'img/mr_roboto.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'Setup/Quick Start',
            position: 'left',
            label: 'Quick Start',
          },
          {
            href: 'https://github.com/Metrostar/paradrop',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Quick Start',
                to: '/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Perlogix. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;

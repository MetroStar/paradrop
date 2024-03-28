const sidebars = {
  paradropSidebar: [
    'What\'s paradrop?',
    {
      type: 'category',
      label: 'Setup',
      items: [
        'Setup/Quick Start',
        'Setup/Detailed Setup',
        {
          type: 'category',
          label: 'Integrations',
          items: [
            {
              type: 'category',
              label: 'Alerts',
              items: [
                'Setup/Integrations/Alerts/Email Setup',
                'Setup/Integrations/Alerts/Slack Setup',
                'Setup/Integrations/Alerts/Teams Setup',
                'Setup/Integrations/Alerts/Mattermost Setup'
              ]
            },
            'Setup/Integrations/Trivy Setup',
            'Setup/Integrations/OpenScap Setup',
          ]
        },
        'Setup/Event Trigger Setup'
      ]
    },
    {
      type: 'category',
      label: 'Manual',
      items: [
        'Manual/Getting Started',
        'Manual/Architecture',
        'Manual/User Management',
        'Manual/Search View',
        'Manual/Reports View',
        'Manual/Event Triggers View'
      ]
    },
    {
      type: 'category',
      label: 'FAQs',
      items: [
        'FAQs/How do I set up live data?'
      ]
    }
  ],
};

module.exports = sidebars;

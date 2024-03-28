// Instantiate Slim Select
export const select = new SlimSelect({
  select: '#fields',
  placeholder: ' '
})

// Updating design of slim-select input fields
const fieldSelectorElement = document.querySelector('.ss-multi-selected')
fieldSelectorElement.className = 'ss-multi-selected py-2 border border-secondary'

const fieldSelectorValues = document.querySelector('.ss-values')
fieldSelectorValues.className = 'ss-values px-1'

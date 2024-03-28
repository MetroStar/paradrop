import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

async function updateConfigurations () {
  const newConfigurations = {}
  const formData = new FormData(document.querySelector('#updateConfigurationsForm'))

  // For loop to add new config settings details as k:v pair to obj newConfigurations
  for (const pair of formData.entries()) {
    if (pair[0] && pair[1]) {
      newConfigurations[pair[0]] = pair[1]
    }
  }

  // Making POST fetch request with new config settings data stored as a body of the request
  const response = await fetchRequest(`${URL}/v1/update-configurations`, 'POST', JSON.stringify(newConfigurations))

  if (response.status === 200) {
    window.location.replace('/ui/configuration-settings')
  } else {
    window.alert(`Updating configurations settings was unsuccessful. Status code: ${response.status} Please try again..`)
  }
}

async function prefillConfigs () {
  // Fetch request to get current configurations data
  // so we can pre-fill them into the input fields
  const response = await fetchRequest(`${URL}/v1/list-configurations`)
  const jsonResponse = JSON.parse(await response.json())

  // Selecting input field elements
  const cleanHostsDaysInterval = document.querySelector('#clean_hosts_days_interval')
  const cleanEventsCount = document.querySelector('#clean_events_count')

  // Pre-filling current value into them
  cleanHostsDaysInterval.value = jsonResponse.clean_hosts_days_interval
  cleanEventsCount.value = jsonResponse.clean_events_count
}

// Loading configuration values into the input fields
prefillConfigs()

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

// On form submit, update configurations
const updateConfigurationsForm = document.querySelector('#updateConfigurationsForm')
updateConfigurationsForm.onsubmit = updateConfigurations

import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

async function updateAgentToken () {
  if (window.confirm('To generate new token, agent data have to be updated. Do you want to continue?')) {
    // Making POST fetch request to generate new agent token
    const response = await fetchRequest(`${URL}/v1/update-agent-token`, 'POST', JSON.stringify({ custom_agent_token: '' }))

    if (response.status === 200) {
      window.location.replace('/ui/agent-auth-token')
    } else {
      window.alert(`Updating agent token was unsuccessful. Status code: ${response.status} Please try again..`)
    }
  } else {
    // If user decide to not generate new token, stop request from sending
    return false
  }
}

async function prefillConfigs () {
  // Fetch request to get current agent token
  // so we can pre-fill it into the disabled input field
  const response = await fetchRequest(`${URL}/v1/get-agent-token`)
  const jsonResponse = JSON.parse(await response.json())

  // Selecting input field elements
  const currentAgentToken = document.querySelector('#agent_auth_token')

  // Pre-filling current value into them
  currentAgentToken.value = jsonResponse.agent_auth_token
}

// Loading agent token into the input field
prefillConfigs()

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

// On form submit, update configurations
const updateAgentTokenForm = document.querySelector('#updateAgentTokenForm')
updateAgentTokenForm.onsubmit = updateAgentToken

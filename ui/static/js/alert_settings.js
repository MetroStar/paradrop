import { URL } from './config.min.js'
import { fetchRequest, removeAllChildNodes } from './functions.min.js'

// Variable that keeps track of what platform is currently selected
let currentlyChosenPlatform = 'email'

// Row that we use to generate and display new inputs
const alertSettingsInputs = document.querySelector('#alertSettingsInputs')

// Function to update Alert Settings with new data
async function updateAlertSettings () {
  // Object to store data for the API
  const newAlertSettings = {}

  // Variable that stores data from the Alert Settings form
  const formData = new FormData(document.querySelector('#alertSettingsForm'))

  // For loop to add the alert settings details as k:v pair to obj the newAlertSettings
  for (const pair of formData.entries()) {
    // If data aren't empty or undefined, add them to the newAlertSettings object
    if (pair[0] && pair[1]) {
      newAlertSettings[pair[0]] = pair[1]
    }

    // Setting current state of enable alert checkbox based on currently selected platform
    const enableAlertCheckbox = document.querySelector('#enableAlertCheckbox')
    newAlertSettings[currentlyChosenPlatform + '_enable'] = enableAlertCheckbox.checked
  }

  // Making POST fetch request with new alert settings data stored as a body of the request
  const res = await fetchRequest(`${URL}/v1/update-configurations`, 'POST', JSON.stringify(newAlertSettings))
  if (res.status === 200) {
    // If request was successful, refresh the page
    window.location.replace('/ui/alert-settings')
  } else {
    // If request status code wasn't 200, pop up alert with error message and status code we got
    window.alert(`Updating alert settings was unsuccessful. Status code: ${res.status} Please try again..`)
  }
}

// Function to add building data to buildInputs function
async function addBuildingData (platform, inputs) {
  // Fetch request to get current configurations data
  // so we can pre-fill them into the input fields
  let currentConfig = await fetchRequest(`${URL}/v1/list-configurations`)
  currentConfig = JSON.parse(await currentConfig.json())

  // Set currently chosen alert to email
  currentlyChosenPlatform = platform

  // Every object in this dictionary is one input field
  // Running buildInputs function to delete old inputs and create new ones
  buildInputs(inputs, currentConfig)

  // Adding enable state of current alert to the enable alert checkbox
  const enableAlertCheckbox = document.querySelector('#enableAlertCheckbox')
  enableAlertCheckbox.checked = currentConfig[currentlyChosenPlatform + '_enable']
}

// Function to delete old input fields and generate new ones
function buildInputs (buildingData, config) {
  // Delete old data
  removeAllChildNodes(alertSettingsInputs)

  // For loop that iterates over specified building data
  for (const inputField in buildingData) {
    const inputDetails = buildingData[inputField]

    // Col div tag that wraps around every input field
    const inputColumn = document.createElement('div')
    inputColumn.className = 'col-12 mt-4 me-2'

    // Label of the input
    const inputLabel = document.createElement('label')
    inputLabel.for = inputDetails.inputId
    inputLabel.textContent = inputDetails.labelTextContent
    inputColumn.appendChild(inputLabel)

    // The input field that user fills
    const inputElement = document.createElement('input')
    inputElement.type = inputDetails.inputType
    inputElement.id = inputDetails.inputId
    inputElement.name = inputDetails.inputId

    // If input type isn't password, pre-fill current settings
    // into the input fields
    if (inputDetails.inputType !== 'password') {
      inputElement.value = config[inputDetails.inputId]
    }
    inputElement.className = 'form-control'
    inputColumn.appendChild(inputElement)

    // Appending input column to the Alert settings row
    alertSettingsInputs.appendChild(inputColumn)
  }
}

// Specifying building data for buildInputs function
// Data for email alerts
const emailAlerts = document.querySelector('#emailAlert')
emailAlerts.addEventListener('click', async function () {
  // Every object in this dictionary is one input field
  const emailInputs = {
    alertEmail: {
      // Label of the input field
      labelTextContent: 'Email address to send alerts to',
      // Type of the input field
      inputType: 'email',
      // Id/name of the input field
      inputId: 'alert_email'
    },

    emailServer: {
      labelTextContent: 'Address of the email server',
      inputType: 'text',
      inputId: 'email_server'
    },

    emailServerPassword: {
      labelTextContent: 'Password to the email server',
      inputType: 'password',
      inputId: 'email_password'
    }
  }

  // Adding building data to build new inputs
  addBuildingData('email', emailInputs)
})

const slackAlerts = document.querySelector('#slackAlert')
slackAlerts.addEventListener('click', async function () {
  const slackInputs = {
    slackWebhookUrl: {
      labelTextContent: 'Slack Webhook URL',
      inputType: 'url',
      inputId: 'slack_url'
    }
  }
  addBuildingData('slack', slackInputs)
})

const teamsAlerts = document.querySelector('#teamsAlert')
teamsAlerts.addEventListener('click', async function () {
  const teamsInputs = {
    teamsWebhookUrl: {
      labelTextContent: 'MS Teams Webhook URL',
      inputType: 'url',
      inputId: 'ms_teams_url'
    }
  }
  addBuildingData('ms_teams', teamsInputs)
})

const mattermostAlerts = document.querySelector('#mattermostAlert')
mattermostAlerts.addEventListener('click', async function () {
  const mattermostInputs = {
    mattermostWebhookUrl: {
      labelTextContent: 'Mattermost Webhook URL',
      inputType: 'url',
      inputId: 'mattermost_url'
    }
  }
  addBuildingData('mattermost', mattermostInputs)
})

// Function that runs onclick function that creates default inputs(Email)
function createDefaultInputFields () {
  emailAlerts.click()
}

// Create default input fields
createDefaultInputFields()

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

// On form submit, update alert settings with new data
const alertSettingsForm = document.querySelector('#alertSettingsForm')
alertSettingsForm.onsubmit = updateAlertSettings

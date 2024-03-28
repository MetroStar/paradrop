import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

async function updateUserToken () {
  if (window.confirm('Are you sure you want to update the current user token?')) {
    // Making POST fetch request to generate new agent token
    const response = await fetchRequest(`${URL}/v1/update-user-token`, 'POST')

    if (response.status === 200) {
      window.location.replace('/ui/profile-settings')
    } else {
      window.alert(`Updating user token was unsuccessful. Status code: ${response.status} Please try again..`)
    }
  } else {
    // If user decide to not generate new token, stop request from sending
    return false
  }
}

async function prefillConfigs () {
  // Fetch request to get current user token
  // so we can pre-fill it into the disabled input field
  const response = await fetchRequest(`${URL}/v1/get-user-token`)
  const jsonResponse = JSON.parse(await response.json())

  // Selecting input field elements
  const currentUserToken = document.querySelector('#userToken')

  // Pre-filling current value into them
  if (jsonResponse.user_auth_token) {
    currentUserToken.value = jsonResponse.user_auth_token
  } else {
    currentUserToken.value = 'There is currently no user token binded to your account.'
  }
}

// Function to update user's email
function updateUser () {
  const userData = {}
  const formData = new FormData(document.querySelector('#updateUserForm'))

  // For loop to add user data as k:v pair to userData object
  for (const pair of formData.entries()) {
    userData[pair[0]] = pair[1]
  }

  // Fetch request to update user data
  fetchRequest(`${URL}/v1/update-user`, 'PUT', JSON.stringify(userData))

  // Wait before changes apply, then refresh the page
  setTimeout(() => { window.location.replace('/ui/users-settings') }, 1200)

  // Stop page from refreshing automatically before changes apply
  return false
}

// Loading user token into the input field
prefillConfigs()

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

// On click, update user token
const updateUserTokenButton = document.querySelector('#updateUserToken')
updateUserTokenButton.onclick = updateUserToken

// On form submit, update configurations
const updateUserForm = document.querySelector('#updateUserForm')
updateUserForm.onsubmit = updateUser

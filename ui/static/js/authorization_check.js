import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

// Function to check if user has authorization and redirect him to login page if he doesn't
async function authorizationCheck () {
  let response = await fetchRequest(`${URL}/v1/authorization-check`)
  if (response.status === 200) {
    response = JSON.parse(await response.json())
    if (response.user_role === 'read-only') {
      const adminElements = document.getElementsByClassName('admin')
      for (const adminElement of adminElements) {
        adminElement.hidden = true
      }
    }
  } else {
    window.location.replace('/ui/login')
  }
}

authorizationCheck()

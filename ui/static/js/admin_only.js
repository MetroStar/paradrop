import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

// Function to allow only admin users to access certain views
async function checkIfUserIsAdmin () {
  let response = await fetchRequest(`${URL}/v1/authorization-check`)
  if (response.status === 200) {
    response = JSON.parse(await response.json())
    if (response.user_role !== 'admin') {
      window.location.replace('/ui')
    }
  } else {
    window.location.replace('/ui')
  }
}

checkIfUserIsAdmin()

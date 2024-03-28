import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

// Function to make fetch request to logout user and delete his session cookies
async function logoutUser () {
  await fetchRequest(`${URL}/v1/logout`)
  window.location.replace('/ui/login')
}
// On click make fetch request to logout user and delete his session cookies
const logoutButton = document.querySelector('#logout')
logoutButton.onclick = logoutUser

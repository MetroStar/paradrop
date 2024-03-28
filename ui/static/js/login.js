import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

async function fetchUserLogin () {
  const userData = {}
  const formData = new FormData(document.querySelector('#userLoginForm'))

  // For loop to add user data as k:v pair to obj userData
  for (const pair of formData.entries()) {
    userData[pair[0]] = pair[1]
  }
  const response = await fetchRequest(`${URL}/v1/user-login`, 'POST', JSON.stringify(userData))

  if (response.status === 200) {
    window.location.replace('/ui')
  } else {
    window.alert('Wrong email and password combination..')
  }
}

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

const userLogin = document.querySelector('#userLoginForm')
userLogin.onsubmit = fetchUserLogin

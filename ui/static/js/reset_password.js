import { URL } from './config.min.js'
import { fetchRequest } from './functions.min.js'

async function resetUserPassword () {
  const userData = {}
  const formData = new FormData(document.querySelector('#resetPasswordForm'))
  const strongPassword = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{12,})/
  // For loop to add user data as k:v pair to obj usrData
  for (const pair of formData.entries()) {
    if (pair[0] === 'pwd1') {
      if (!strongPassword.test(pair[1])) {
        window.alert('Password is not strong enough. It must be atleast 12 characters long and contain atleast 1 uppercase letter, 1 lowercase letter, 1 special character and 1 digit..')
        return false
      }
    } else if (pair[0] === 'pwd2') {
      if (userData.pwd1 !== pair[1]) {
        window.alert('Passwords do not match..')
        return false
      } else if (!strongPassword.test(pair[1])) {
        window.alert('Password is not strong enough. It must be atleast 12 characters long and contain atleast 1 uppercase letter, 1 lowercase letter, 1 special character and 1 digit..')
        return false
      }
    }
    userData[pair[0]] = pair[1]
  }

  // Making POST fetch request with user data stored as a body of the request
  const response = await fetchRequest(`${URL}/v1/reset-pwd`, 'PUT', JSON.stringify(userData))

  if (response.status === 200) {
    window.location.replace('/ui/login')
  } else {
    window.alert('You are not allowed to reset your password. Please contact your administrator.')
  }
}

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

const resetPassword = document.querySelector('#resetPasswordForm')
resetPassword.onsubmit = resetUserPassword

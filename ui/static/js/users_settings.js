import { URL } from './config.min.js'
import { fetchRequest, removeAllChildNodes, delayRequest } from './functions.min.js'

// ========== GLOBAL VARIABLES ==========

// Keeping track of what part of data we want to load
// searchSize specifies how many results we want to retrieve
const searchSize = 20

// ES will return results starting from value of fetchDataFrom
let fetchDataFrom = 0

// Variable that keeps track of number of all results we found in the database
let numberOfResults = 0

// Variable that keeps track of the role that current user has
let currentUserRole

// Variable to keep track of by what field we want to sort
let sortField = 'none'

// Variable to keep track of order of sorting
let sortOrder = false

function addUserAccount () {
  const userData = {}
  const formData = new FormData(document.querySelector('#createAccountForm'))
  const strongPassword = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{12,})/
  // For loop to add user data as k:v pair to userData object
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

  // Fetch request to create user account
  fetchRequest(`${URL}/v1/create-user`, 'POST', JSON.stringify(userData))

  // Wait before changes apply, then refresh the page
  setTimeout(() => { window.location.replace('/ui/users-settings') }, 1000)

  // Stop page from refreshing automatically before changes apply
  return false
}

// Anytime user searches for data, delete current data and display new one
function userSearch () {
  const tableBody = document.querySelector('#table-body')

  // Deleting all displayed results
  removeAllChildNodes(tableBody)

  // On search, reset fetchDataFrom variable
  // So we get our new data from the start again
  fetchDataFrom = 0
  updateTable()
}

// Function to add sorting functionality to the table headers
function addSorting () {
  const tableHeaders = document.getElementById('headerRow')
  for (let i = 0; i < tableHeaders.children.length; i++) {
    // We don't want to add sorting to delete user and reset password icons
    if (!['', 'resetPasswordTag', 'deleteUserTag'].includes(tableHeaders.children[i].id)) {
      tableHeaders.children[i].onclick = delayRequest(function () {
        sortField = tableHeaders.children[i].id
        sortOrder = !sortOrder
        updateTable()
      }, 300)
    }
  }
}

async function updateTable () {
  // This variable stores phrase searched by the user
  let searchInputBarValue = document.querySelector('#searchBar').value

  // Select element that shows how many results we found in what time
  const searchStatistics = document.querySelector('#results')

  // If no search is specified, search for all results
  if (searchInputBarValue === '') {
    searchInputBarValue = '*'
  }

  try {
    // Time before fetch
    const currentTime = Date.now()

    // Fetching data about all users
    const response = await fetchRequest(`${URL}/v1/list-users/${searchInputBarValue}/${fetchDataFrom + '-' + searchSize}/${sortField + '-' + sortOrder}`)

    if (response.status === 200) {
      const jsonResponse = JSON.parse(await response.json())

      // Deleting previously displayed content
      const tableBody = document.querySelector('#table-body')
      removeAllChildNodes(tableBody)

      // Update number of results on every fetch request
      numberOfResults = jsonResponse.number_of_results

      const paginationNextButtonWrapper = document.querySelector('#paginationNextButtonWrapper')
      const paginationNextButton = document.querySelector('#paginationNextButton')

      // If we reached the last part of the data, disable pagination next button
      if ((fetchDataFrom + searchSize) > numberOfResults) {
        paginationNextButtonWrapper.className = 'page-item disabled'
        paginationNextButton.className = 'page-link text-dark bg-light shadow-none'
      } else {
        paginationNextButtonWrapper.className = 'page-item'
        paginationNextButton.className = 'page-link text-dark shadow-none'
      }

      // Time after fetch
      const timeAfterFetch = Date.now() - currentTime

      // Display the search statistics only when we find some results
      if (numberOfResults > 0 && fetchDataFrom === 0) {
        // Displaying new search statistics
        searchStatistics.textContent = `Found ${numberOfResults} results in ${(timeAfterFetch) / 1000} seconds..`
      }

      // We have to check if current user has admin rights
      // So we can display only part of the content if he doesn't
      if (searchInputBarValue === '*' && fetchDataFrom === 0) {
        currentUserRole = jsonResponse.current_user_role
      }

      // If current user isn't admin, delete Reset password
      // and Delete user icons from the table
      if (currentUserRole === 'read-only') {
        const resetPasswordTag = document.querySelector('#resetPasswordTag')
        const deleteUserTag = document.querySelector('#deleteUserTag')
        if (resetPasswordTag && deleteUserTag) {
          resetPasswordTag.remove()
          deleteUserTag.remove()
        }
      } else {
        // If admin is logged in, show Add User button
        const addUserButton = document.querySelector('#addUserButton')
        addUserButton.hidden = false
      }

      for (const user of jsonResponse.user_data) {
        // Creating new table row elements
        const newRow = document.createElement('tr')
        const email = document.createElement('td')
        const name = document.createElement('td')
        const role = document.createElement('td')
        const lastSignin = document.createElement('td')
        const createdDate = document.createElement('td')
        const userExpire = document.createElement('td')

        // Adding data to table headers
        tableBody.appendChild(newRow)
        newRow.appendChild(email)
        email.textContent = user.email

        newRow.appendChild(name)
        name.textContent = user.name

        newRow.appendChild(role)
        role.textContent = user.role

        newRow.appendChild(lastSignin)
        lastSignin.textContent = user.last_signin

        newRow.appendChild(createdDate)
        createdDate.textContent = user.created_at

        newRow.appendChild(userExpire)
        userExpire.textContent = user.expire_at

        // If current user is admin, add delete user and
        // allow password reset functions into the table
        if (currentUserRole === 'admin') {
          // Creating new table row elements
          const resetPassword = document.createElement('td')
          const deleteUser = document.createElement('td')
          // Adding Reset password link
          newRow.appendChild(resetPassword)
          const resetPasswordLink = document.createElement('a')
          resetPasswordLink.href = ''
          resetPasswordLink.value = user.email
          resetPasswordLink.textContent = 'Reset'
          resetPasswordLink.className = 'text-decoration-none'

          // Adding onclick function that sends a request to api to delete user from database
          resetPasswordLink.onclick = function () {
            if (window.confirm(`Are you sure you want to allow password reset to user ${resetPasswordLink.value}?`)) {
              // Fetch request to allow user to reset his password
              fetchRequest(`${URL}/v1/allow-pwd-reset`, 'PUT', JSON.stringify({ email: resetPasswordLink.value }))
              return false
            } else {
              // If user decide to not reset password, stop request from sending
              return false
            }
          }
          resetPassword.appendChild(resetPasswordLink)

          // Delete user icon
          newRow.appendChild(deleteUser)
          const deleteUserIcon = document.createElement('a')
          deleteUserIcon.href = ''

          if (!user.current_user) {
            deleteUserIcon.value = user.email
            deleteUserIcon.className = 'fas fa-trash-alt text-danger'

            // Adding onclick function that sends a request to api to delete user from database
            deleteUserIcon.onclick = function () {
              if (window.confirm(`Are you sure you want to delete user ${deleteUserIcon.value}?`)) {
                // Fetch request to delete selected user account
                fetchRequest(`${URL}/v1/delete-user`, 'DELETE', JSON.stringify({ email: deleteUserIcon.value }))

                // Delete user from the table
                this.parentNode.parentNode.remove()

                // Stop page from refreshing automatically before changes apply
                return false
              } else {
                // If user decide to not delete user, stop request from sending
                return false
              }
            }
            deleteUser.appendChild(deleteUserIcon)

          // If user is the current user, delete icon is disabled
          } else {
            deleteUserIcon.className = 'fas fa-trash-alt text-secondary'
            deleteUser.appendChild(deleteUserIcon)
          }
        }
      }
    } else {
      const paginationNextButtonWrapper = document.querySelector('#paginationNextButtonWrapper')
      const paginationNextButton = document.querySelector('#paginationNextButton')
      const paginationPreviousButton = document.querySelector('#paginationPreviousButton')
      const paginationPreviousButtonWrapper = document.querySelector('#paginationPreviousButtonWrapper')

      // Disable the pagination buttons
      paginationNextButtonWrapper.className = 'page-item disabled'
      paginationNextButton.className = 'page-link text-dark bg-light shadow-none'
      paginationPreviousButtonWrapper.className = 'page-item disabled'
      paginationPreviousButton.className = 'page-link text-dark bg-light shadow-none rounded-start'

      // Deleting displayed search statistics
      searchStatistics.textContent = ''

      // Delete everything from table header and body
      const tableBody = document.querySelector('#table-body')
      removeAllChildNodes(tableBody)
      const noDataMessage = document.createElement('h4')
      noDataMessage.className = 'p-2'
      noDataMessage.textContent = 'No data available..'
      tableBody.appendChild(noDataMessage)
    }
  } catch {
    const paginationNextButtonWrapper = document.querySelector('#paginationNextButtonWrapper')
    const paginationNextButton = document.querySelector('#paginationNextButton')
    const paginationPreviousButton = document.querySelector('#paginationPreviousButton')
    const paginationPreviousButtonWrapper = document.querySelector('#paginationPreviousButtonWrapper')

    // Disable the pagination buttons
    paginationNextButtonWrapper.className = 'page-item disabled'
    paginationNextButton.className = 'page-link text-dark bg-light shadow-none'
    paginationPreviousButtonWrapper.className = 'page-item disabled'
    paginationPreviousButton.className = 'page-link text-dark bg-light shadow-none rounded-start'

    // On error, delete search statistics
    searchStatistics.textContent = ''
  }
}

// Selecting pagination buttons elements
const paginationPreviousButton = document.querySelector('#paginationPreviousButton')
const paginationPreviousButtonWrapper = document.querySelector('#paginationPreviousButtonWrapper')
const paginationNextButton = document.querySelector('#paginationNextButton')

// Setting function to "previous" pagination button
// Delaying request to prevent creating a chain of requests anytime
// user clicks the button multiple times in a short amount of time
paginationPreviousButton.onclick = delayRequest(function () {
  // Deduct value of searchSize variable from fetchDataFrom to get previous part of the data
  fetchDataFrom -= searchSize
  updateTable()

  // Disable pagination previous button when we get to the start of the data
  if (fetchDataFrom === 0) {
    paginationPreviousButtonWrapper.className = 'page-item disabled'
    paginationPreviousButton.className = 'page-link text-dark bg-light shadow-none rounded-start'
  }
}, 250)

// Setting function to "next" pagination button
// Delaying request to prevent creating a chain of requests anytime
// user clicks the button multiple times in a short amount of time
paginationNextButton.onclick = delayRequest(function () {
  // Make pagination previous button clickable
  paginationPreviousButtonWrapper.className = 'page-item'
  paginationPreviousButton.className = 'page-link text-dark rounded-start shadow-none'

  // Add the value of searchSize variable to fetchDataFrom to get next part of the data
  fetchDataFrom += searchSize
  updateTable()
}, 250)

// Adding data into the table on window load
updateTable()
addSorting()

// Event listener to listen for search bar input
// On input run userSearch function to fetch data matching the searched word
const searchInputBar = document.querySelector('#searchBar')
searchInputBar.oninput = delayRequest(function () {
  userSearch()
}, 1000)

// Stop site from refreshing automatically before changes apply
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

const createAccount = document.querySelector('#createAccountForm')
createAccount.onsubmit = addUserAccount

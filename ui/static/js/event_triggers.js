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

// Variable that checks if user wants to update or create Event Trigger
let updateTrigger = false

// Variables that keeps track of when event trigger that we want to update was created
// This data is required for event trigger update requests
let eventTriggerCreatedBy = ''
let eventTriggerCreatedAt = ''

// When updating event trigger, eventTriggerId variable will be reffering to
// the id of the trigger that we want to update
let eventTriggerId = ''

// Variable to keep track of by what field we want to sort
let sortField = 'none'

// Variable to keep track of order of sorting
let sortOrder = false

// Selecting modal title and submit button elements so we can change it's value
// based on if we are updating or creating a new event trigger
const modalTitle = document.querySelector('#modalTitle')
const submitButton = document.querySelector('#modalSubmitButton')

// Function to add or update Event trigger
async function addEventTrigger () {
  const formData = new FormData(document.querySelector('#addEventTriggerForm'))
  const eventTriggerData = {}

  // event_trigger's value is another object, so we need to define it beforehand
  eventTriggerData.event_trigger = {}

  // Iterating over data from the form input fields
  for (const pair of formData.entries()) {
    if (pair[0] === 'eventName') {
      eventTriggerData.event_name = pair[1]
    } else if (pair[0] === 'impact') {
      eventTriggerData.event_impact = pair[1]
    } else if (pair[0] === 'field') {
      eventTriggerData.event_trigger.field = pair[1]
    } else if (pair[0] === 'comparisonOperator') {
      eventTriggerData.event_trigger.operator = pair[1]
    } else if (pair[0] === 'comparisonValue') {
      eventTriggerData.event_trigger.expected_value = pair[1]
    }

    const sendAlert = document.querySelector('#sendAlert')
    eventTriggerData.send_alert = sendAlert.checked

    const enableTrigger = document.querySelector('#enableTrigger')
    eventTriggerData.event_enable = enableTrigger.checked
  }

  if (updateTrigger) {
    eventTriggerData.id = eventTriggerId
    eventTriggerData.created_at = eventTriggerCreatedAt
    eventTriggerData.created_by = eventTriggerCreatedBy
    // Fetch request to update event trigger
    fetchRequest(`${URL}/v1/update-event-triggers`, 'POST', JSON.stringify(eventTriggerData))
  } else {
    // Fetch request to add event trigger
    fetchRequest(`${URL}/v1/add-event-triggers`, 'POST', JSON.stringify(eventTriggerData))
  }

  // Wait before changes apply, then refresh the page
  setTimeout(() => { window.location.replace('/ui/event-triggers') }, 1000)

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
    if (tableHeaders.children[i].id !== '') {
      tableHeaders.children[i].onclick = delayRequest(function () {
        sortField = tableHeaders.children[i].id
        sortOrder = !sortOrder
        updateTable()
      }, 300)
    }
  }
}

// Function to create new headers, add onclick functions and update data in the data table
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

    // Getting data about all event triggers
    const response = await fetchRequest(`${URL}${'/v1/list-event-triggers'}/${searchInputBarValue}/${fetchDataFrom + '-' + searchSize}/${sortField + '-' + sortOrder}`)

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

      for (const data of jsonResponse.data) {
        const newRow = document.createElement('tr')

        // Adding data to table headers
        const eventName = document.createElement('td')
        eventName.innerHTML = data.event_name
        newRow.appendChild(eventName)

        const eventImpact = document.createElement('td')
        eventImpact.innerHTML = data.event_impact
        newRow.appendChild(eventImpact)

        const eventEnable = document.createElement('td')
        eventEnable.innerHTML = data.event_enable
        newRow.appendChild(eventEnable)

        const sendAlert = document.createElement('td')
        sendAlert.innerHTML = data.send_alert
        newRow.appendChild(sendAlert)

        const eventTrigger = document.createElement('td')
        eventTrigger.innerHTML = data.event_trigger.field + ' ' + data.event_trigger.operator + ' ' + data.event_trigger.expected_value
        newRow.appendChild(eventTrigger)

        // Creating table column with actions
        const actions = document.createElement('td')

        // Creating delete event trigger icon
        const deleteEventTrigger = document.createElement('a')
        deleteEventTrigger.href = ''
        deleteEventTrigger.className = 'fas fa-trash-alt text-danger me-4'
        deleteEventTrigger.onclick = function () {
          if (window.confirm(`Are you sure you want to delete ${data.event_name} trigger?`)) {
            // Fetch request to delete event trigger from the database
            fetchRequest(`${URL}/v1/delete-event-triggers`, 'DELETE', JSON.stringify({ id: data.id }))

            // Delete event trigger from the table
            this.parentNode.parentNode.remove()
          }

          // Stop page from refreshing automatically before changes apply
          return false
        }
        // Adding delete event trigger icon to the actions
        actions.appendChild(deleteEventTrigger)

        // Creating update event trigger icon
        const updateEventTrigger = document.createElement('a')
        updateEventTrigger.href = ''
        updateEventTrigger.className = 'fa-solid fa-pen text-decoration-none'

        // Those attributes will add the function to open the modal anytime user clicks on update icon
        updateEventTrigger.setAttribute('data-coreui-toggle', 'modal')
        updateEventTrigger.setAttribute('data-coreui-target', '#addEventTriggerModal')
        updateEventTrigger.onclick = function () {
          // Changing title of the modal to name of the event trigger
          modalTitle.textContent = data.event_name

          // Changing text content of button in the modal
          submitButton.textContent = 'Update Event Trigger'

          // On click change value of eventTriggerId to the id of current event trigger
          eventTriggerId = data.id

          // Set update trigger to true so we send update request instead of add request
          updateTrigger = true

          // Store created_at/_by data into variables so we can use it for update request
          eventTriggerCreatedAt = data.created_at
          eventTriggerCreatedBy = data.created_by

          // On click pre-filling inputs with data from current event trigger
          const eventName = document.querySelector('#eventName')
          const impact = document.querySelector('#impact')
          const field = document.querySelector('#field')
          const comparisonOperator = document.querySelector('#comparisonOperator')
          const comparisonValue = document.querySelector('#comparisonValue')
          const enableTrigger = document.querySelector('#enableTrigger')
          const sendAlert = document.querySelector('#sendAlert')

          eventName.value = data.event_name
          impact.value = data.event_impact
          field.value = data.event_trigger.field
          comparisonOperator.value = data.event_trigger.operator
          comparisonValue.value = data.event_trigger.expected_value
          enableTrigger.checked = data.event_enable
          sendAlert.checked = data.send_alert
        }

        // Adding update event trigger icon to the actions
        actions.appendChild(updateEventTrigger)
        // Adding actions to new row
        newRow.appendChild(actions)
        // Adding row to the table body
        tableBody.appendChild(newRow)
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

// Updating table when page loads
updateTable()
addSorting()

// Event listener to listen for search bar input
// On input run userSearch function to fetch data matching the searched word
const searchInputBar = document.querySelector('#searchBar')
searchInputBar.oninput = delayRequest(function () {
  userSearch()
}, 1000)

// Stop site from refreshing on submit
// Without this, we would get error because site
// would send the POST request itself instead of using fetch request
window.onsubmit = function () { return false }

// On form submit run addEventTrigger function
const addEventTriggerForm = document.querySelector('#addEventTriggerForm')
addEventTriggerForm.onsubmit = addEventTrigger

const addEventTriggerButton = document.querySelector('#addEventTriggerButton')
addEventTriggerButton.onclick = function () {
  modalTitle.textContent = 'Add Event Trigger'
  submitButton.textContent = 'Add Event Trigger'
  updateTrigger = false
  // Clear data in input fields
  addEventTriggerForm.reset()
}

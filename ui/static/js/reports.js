import { URL } from './config.min.js'
import { fetchRequest, removeAllChildNodes, delayRequest, titleCase } from './functions.min.js'
import { select } from './slimselect.min.js'

// ========== GLOBAL VARIABLES ==========

// Keeping track of what part of data we want to load
// searchSize specifies how many results we want to retrieve
const searchSize = 20

// ES will return results starting from value of fetchDataFrom
let fetchDataFrom = 0

// Variable that keeps track of number of all results we found in the database
let numberOfResults = 0

// Variable that checks if user wants to update or create report
let updateReport = false

// Variable that stores updated field names of the existing report we want to update
let updatedFieldNames = ''

// Variable that keeps track of when report that we want to update was created
// This data is required for report update requests
let reportCreatedBy = ''
let reportCreatedAt = ''

// When updating report, reportId variable will be reffering to
// the id of the report we want to update
let reportId = ''

// Variable to keep track of by what field we want to sort
let sortField = 'none'

// Variable to keep track of order of sorting
let sortOrder = false

// Selecting modal title and submit button so we can change it's value
// based on if we are updating or creating a new report
const modalTitle = document.querySelector('#modalTitle')
const submitButton = document.querySelector('#modalSubmitButton')

// Function to add or update Report
async function addReport () {
  const addReportFormData = new FormData(document.querySelector('#addReportForm'))
  const reportData = {}

  // report_mappings's value is another object, so we need to define it beforehand
  reportData.report_mappings = {}

  // Iterating over data from the form input fields
  for (const pair of addReportFormData.entries()) {
    pair[0] === 'reportName' ? reportData.report_name = pair[1] : reportData.report_description = pair[1]
  }

  // Loop over selected fields in rename fields form and add it to the dictionary
  const renameFieldsFormData = new FormData(document.querySelector('#renameFieldsForm'))
  for (const pair of renameFieldsFormData.entries()) {
    if (select.selected().includes(pair[0])) {
      reportData.report_mappings[pair[1]] = pair[0]
    }
  }

  // Loop over selected fields in add report fields form and add it to the dictionary
  // if it's not already in it
  for (const field of select.selected()) {
    if (!Object.values(reportData.report_mappings).includes(field)) {
      reportData.report_mappings[titleCase(field.replace('_', ' '))] = field
    }
  }

  if (updateReport) {
    reportData.id = reportId
    reportData.created_at = reportCreatedAt
    reportData.created_by = reportCreatedBy
    // Fetch request to update report
    fetchRequest(`${URL}/v1/update-reports`, 'POST', JSON.stringify(reportData))
  } else {
    // Fetch request to add report
    fetchRequest(`${URL}/v1/add-reports`, 'POST', JSON.stringify(reportData))
  }

  // Wait before changes apply, then refresh the page
  setTimeout(() => { window.location.replace('/ui/reports') }, 1000)

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
  // This variable holds the word searched by the user
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

    // Getting data about all reports
    const response = await fetchRequest(`${URL}${'/v1/list-reports'}/${searchInputBarValue}/${fetchDataFrom + '-' + searchSize}/${sortField + '-' + sortOrder}`)

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
        const reportName = document.createElement('td')
        reportName.innerHTML = data.report_name
        newRow.appendChild(reportName)

        const reportDescription = document.createElement('td')
        reportDescription.innerHTML = data.report_description
        newRow.appendChild(reportDescription)

        const actions = document.createElement('td')
        const downloadIcon = document.createElement('a')
        downloadIcon.className = 'fa-solid fa-download text-success me-3'

        const reportData = {}
        // List to store data for headers of the csv file
        reportData.table_headers = []

        // List with all selected fields we want to include in csv file
        reportData.selected_fields = []

        // Sorting data and adding them into separate lists
        for (const field in data.report_mappings) {
          reportData.table_headers.push(field)
          reportData.selected_fields.push(data.report_mappings[field])
        }
        downloadIcon.href = '#'
        downloadIcon.onclick = async function () {
          const response = await fetchRequest(`${URL}/v1/download-report/${reportData.table_headers.join('-')}/${reportData.selected_fields.join('-')}/${data.report_name}`)
          if (response.status === 200) {
            const file = await response.blob()
            const reportFileURL = window.URL.createObjectURL(file)
            const fileLink = document.createElement('a')
            fileLink.href = reportFileURL
            fileLink.download = data.report_name
            fileLink.click()
          }
        }
        actions.appendChild(downloadIcon)

        // Creating delete report icon
        const deleteReports = document.createElement('a')
        deleteReports.href = ''
        deleteReports.className = 'fas fa-trash-alt text-danger me-3'
        deleteReports.onclick = function () {
          if (window.confirm(`Are you sure you want to delete ${data.report_name}?`)) {
            // Fetch request to delete report from the database
            fetchRequest(`${URL}/v1/delete-reports`, 'DELETE', JSON.stringify({ id: data.id }))

            // Delete report from the table
            this.parentNode.parentNode.remove()
          }

          // Stop page from refreshing automatically before changes apply
          return false
        }
        // Adding delete report icon to the actions
        actions.appendChild(deleteReports)

        // Creating update report icon
        const updateReports = document.createElement('a')
        updateReports.href = ''
        updateReports.className = 'fa-solid fa-pen text-decoration-none'

        // Those attributes will add the function to open the modal anytime user clicks on update icon
        updateReports.setAttribute('data-coreui-toggle', 'modal')
        updateReports.setAttribute('data-coreui-target', '#addReportModal')
        updateReports.onclick = function () {
          // Changing title of the modal to name of the report
          modalTitle.textContent = data.report_name

          // Changing text content of button in the modal
          submitButton.textContent = 'Update Report'

          // On click change value of reportId to the id of current report
          reportId = data.id

          // Set update report to true so we send update request instead of add request
          updateReport = true

          // Store created_at/_by data into variables so we can use it for update request
          reportCreatedAt = data.created_at
          reportCreatedBy = data.created_by

          // On click pre-filling form inputs with data from the current report
          const reportName = document.querySelector('#reportName')
          const reportDescription = document.querySelector('#reportDescription')
          reportName.value = data.report_name
          reportDescription.value = data.report_description

          // Selecting fields from the report we want to update
          const setFields = []
          const reportMappings = data.report_mappings
          for (const report in reportMappings) {
            setFields.push(reportMappings[report])
          }
          // Setting fields selected by user to set them to selected in a Update Report form
          select.set(setFields)

          // Adding user's custom names to the updatedFieldNames variable so we can display it
          updatedFieldNames = reportMappings
        }
        // Adding update icon into actions
        actions.appendChild(updateReports)

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

// Function to add all Host fields to Add Report Field dropdown
async function updateFields () {
  // Fetching data from specified api endpoint
  let allHostFields = await fetchRequest(`${URL}${'/v1/list-host-fields'}`)
  allHostFields = JSON.parse(await allHostFields.json())
  const selectFields = document.querySelector('#fields')

  // Iterating over all host fields
  for (const hostField in allHostFields) {
    // Creating option element and adding name of the field into it
    const fieldOption = document.createElement('option')
    fieldOption.value = allHostFields[hostField]
    fieldOption.textContent = hostField
    selectFields.appendChild(fieldOption)
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

// Updating table and Add Report form fields when page loads
updateTable()
updateFields()
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

// On form submit run addReport function
const addReportForm = document.querySelector('#addReportForm')
addReportForm.onsubmit = addReport
const addReportButton = document.querySelector('#addReportButton')
addReportButton.onclick = function () {
  modalTitle.textContent = 'Add Report'
  submitButton.textContent = 'Add Report'
  updatedFieldNames = ''
  updateReport = false

  // Delete data in the input fields
  select.set([])
  addReportForm.reset()
}

// Adding onclick function to Rename Fields button
const renameFieldsButton = document.querySelector('#renameFieldsButton')
renameFieldsButton.onclick = function () {
  const renameFieldsRow = document.querySelector('#renameFieldsRow')

  // Remove old data from Rename Fields form
  removeAllChildNodes(renameFieldsRow)

  // Iterate over all selected fields
  for (const field of select.selected()) {
    // Create input tags for every selected field
    const inputColumn = document.createElement('div')
    inputColumn.className = 'col-12 mb-2 me-2'
    const inputLabel = document.createElement('label')
    inputLabel.className = 'ms-1'

    // Variable that stores the field name that will be pre-filled
    // in Rename Fields form input
    let fieldName = ''

    // If user updated the field name,
    // set it as a value of the fieldName variable
    if (Object.values(updatedFieldNames).includes(field)) {
      // Get the key by the value from the updatedFieldNames object
      const key = Object.keys(updatedFieldNames).find(k => updatedFieldNames[k] === field)
      fieldName = key
    } else {
      fieldName = titleCase(field.replaceAll('_', ' '))
    }

    inputLabel.textContent = titleCase(field.replaceAll('_', ' ')) + ':'
    const inputElement = document.createElement('input')
    inputElement.name = field
    inputElement.value = fieldName
    inputElement.className = 'form-control mb-3 border border-secondary'
    inputColumn.appendChild(inputLabel)
    inputColumn.appendChild(inputElement)
    renameFieldsRow.appendChild(inputColumn)
  }
}

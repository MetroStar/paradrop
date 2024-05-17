import { URL } from './config.min.js'
import { fetchRequest, removeAllChildNodes, delayRequest, titleCase } from './functions.min.js'
import { select } from './slimselect.min.js'

// ========== GLOBAL VARIABLES ==========

// Keeping track of what part of data we want to load
// searchSize specifies how many results we want to retrieve
let searchSize = 20

// ES will return results starting from value of fetchDataFrom
let fetchDataFrom = 0

// Variable that keeps track of number of all results we found in the database
let numberOfResults = 0

// Variable that keeps track of what filter is currently selected
let filter = 'hosts'

// Number of string characters that we want to display at once
const modalDataPartSize = 10000

// Variable to keep track of the start index of data we want to retrieve
let modalDataPartFrom = 0

// Variable to keep track of the end index of data we want to retrieve
let modalDataPartTo = modalDataPartSize

// Variable to keep track of the whole length of host data
let modalDataLength = 0

// Variable to keep track of by what field we want to sort
let sortField = 'none'

// Variable to keep track of order of sorting
let sortOrder = false

// Variable to keep track of what field we want to filter by
let dataCardFilterField = 'none'

// Variable to keep track of what card filter is currently selected
let selectedCardFilter = 'none'

// While running the updateModalData function, we also have to re-select previously selected fields
// and that triggers onchange function which leads to infinite loop.
// So anytime we run updateModalData function, this variable is set to false
// and after it finishes running, we set it back to true again.
let onchangeFunctionsAllowed = true

// This variable holds function that is going to be used to fetch the data we need
// This functions is changing, so it must be stored as a global variable
let currentFetchDataFunction = function () {}

function paginationButtonsActions (action) {
  // Select all pagination elements
  let paginationPreviousButton
  let paginationPreviousButtonWrapper
  let paginationNextButtonWrapper
  let paginationNextButton

  if (action.split('-')[0] === 'modal') {
    paginationPreviousButton = document.querySelector('#modalPaginationPreviousButton')
    paginationPreviousButtonWrapper = document.querySelector('#modalPaginationPreviousButtonWrapper')
    paginationNextButtonWrapper = document.querySelector('#modalPaginationNextButtonWrapper')
    paginationNextButton = document.querySelector('#modalPaginationNextButton')
  } else if (action.split('-')[0] === 'view') {
    paginationPreviousButton = document.querySelector('#paginationPreviousButton')
    paginationPreviousButtonWrapper = document.querySelector('#paginationPreviousButtonWrapper')
    paginationNextButtonWrapper = document.querySelector('#paginationNextButtonWrapper')
    paginationNextButton = document.querySelector('#paginationNextButton')
  }

  if (action.split('-')[1] === 'activate') {
    // Make previous pagination button clickable
    if (['both', 'previous'].includes(action.split('-')[2])) {
      paginationPreviousButtonWrapper.className = 'page-item'
      paginationPreviousButton.className = 'page-link text-dark rounded-start shadow-none'
    }
    // Make next pagination button clickable
    if (['both', 'next'].includes(action.split('-')[2])) {
      paginationNextButtonWrapper.className = 'page-item'
      paginationNextButton.className = 'page-link text-dark shadow-none'
    }
  } else if (action.split('-')[1] === 'disable') {
    // Disable previous pagination button
    if (['both', 'previous'].includes(action.split('-')[2])) {
      paginationPreviousButtonWrapper.className = 'page-item disabled'
      paginationPreviousButton.className = 'page-link text-dark bg-light shadow-none rounded-start'
    }
    // Disable next pagination button
    if (['both', 'next'].includes(action.split('-')[2])) {
      paginationNextButtonWrapper.className = 'page-item disabled'
      paginationNextButton.className = 'page-link text-dark bg-light shadow-none'
    }
  }
}

// Anytime user searches for data, delete current data and display new one
function userSearch () {
  const tableBody = document.querySelector('#table-body')

  // Deleting all displayed results
  removeAllChildNodes(tableBody)

  // Deleting old search statistics
  const searchStatistics = document.querySelector('#results')
  searchStatistics.textContent = ''

  // Reset data card filters related variables to default values
  dataCardFilterField = 'none'
  selectedCardFilter = 'none'

  // Reset fetchDataFrom variable
  // so we get our new data from the start again
  fetchDataFrom = 0
  fetchData()
}

// Function that creates and updates data cards
async function updateDataCards (dataCardsData, dataCardsSpecifications) {
  // Delete old data cards
  const dataCards = document.querySelector('#dataCards')
  removeAllChildNodes(dataCards)

  // Variable to keep track of first iteration of for loop below
  // This is used to higlight and add shadow to only first data card
  let firstIteration = true
  for (const currentCard in dataCardsSpecifications) {
    // Creating elements that we need and updating it's attributes
    // to display data cards the way we want
    const outerColDiv = document.createElement('div')

    // If this is the first iteration, add shadow and id to the first data card and set firstIteration to false
    if (firstIteration) {
      outerColDiv.className = 'col border border-2 border-danger rounded me-3 mb-3 bg-white shadow'
      outerColDiv.id = 'firstDataCard'
      firstIteration = false

    // If current card match value of the dataCardFilter variable
    } else if (currentCard === selectedCardFilter) {
      // Add shadow and higlighting to it
      outerColDiv.className = 'col border border-2 border-danger rounded me-3 mb-3 bg-white shadow'

      // And remove shadow and higlighting from the first data card
      const firstDataCard = document.querySelector('#firstDataCard')
      firstDataCard.className = 'col border rounded me-3 mb-3 bg-white'
    } else {
      outerColDiv.className = 'col border rounded me-3 mb-3 bg-white'
    }

    // If data card value is not zero, add onclick function to it
    if (dataCardsData[dataCardsSpecifications[currentCard].fieldName]) {
      // When user clicks on data card, apply specified filter
      outerColDiv.onclick = function () {
        // Setting field that we want to filter by to currently chosen card
        dataCardFilterField = dataCardsSpecifications[currentCard].fieldName

        // Disable previous pagination button
        paginationButtonsActions('view-disable-previous')

        // Keeping track of what card filter is currently selected
        selectedCardFilter = currentCard
        fetchDataFrom = 0
        fetchData()
      }
    } else {
      // If data card value is zero, don't add any onclick function
      // and change the color of that data card to more be transparent
      outerColDiv.className = 'col border rounded me-3 mb-3 bg-white opacity-50'
    }

    dataCards.appendChild(outerColDiv)

    const innerRowDiv = document.createElement('div')
    innerRowDiv.className = 'row m-0'
    outerColDiv.appendChild(innerRowDiv)

    const leftColDiv = document.createElement('div')
    leftColDiv.className = 'col-10'
    innerRowDiv.appendChild(leftColDiv)

    // Setting data card values
    const boxValue = document.createElement('h2')
    boxValue.className = 'mt-1'
    boxValue.textContent = dataCardsData[dataCardsSpecifications[currentCard].fieldName]
    leftColDiv.appendChild(boxValue)

    const boxDescription = document.createElement('h6')
    // Setting description related to displayed value
    boxDescription.textContent = currentCard
    leftColDiv.appendChild(boxDescription)

    const rightColDiv = document.createElement('div')
    rightColDiv.className = 'col-2 d-flex align-items-center justify-content-end'
    innerRowDiv.appendChild(rightColDiv)

    // Setting the icon that we want to display
    const iconContainer = document.createElement('div')
    iconContainer.className = 'container d-none d-xl-block'
    const icon = document.createElement('span')
    icon.className = dataCardsSpecifications[currentCard].icon
    iconContainer.appendChild(icon)
    rightColDiv.appendChild(iconContainer)
  }
}

// Function to update and syntax highlight data displayed in the modal
function updateModalData (modalData) {
  // Block onchange functions before we updating field selector
  onchangeFunctionsAllowed = false

  const fieldSelector = document.querySelector('#fields')
  const modalSearchBar = document.querySelector('#modalSearchBar')

  // Function to delete old options in field selector and add new ones
  function updateFields (fields) {
    // Storing currently selected fields in variable
    // before deleting old ones and adding new ones
    const selectedFields = select.selected()

    // Deleting old fields
    fieldSelector.length = 0

    // Iterating over all host fields to add them into the field selector
    for (const field of fields) {
      // Creating option element and adding name of the field into it
      const fieldOption = document.createElement('option')
      fieldOption.value = field
      fieldOption.textContent = titleCase(field.replaceAll('_', ' '))
      fieldSelector.appendChild(fieldOption)
    }

    // Re-selecting previously selected fields
    select.set(selectedFields)
  }

  if (fieldSelector.value === '' || (fieldSelector.value !== '' && modalSearchBar.value !== '')) {
    updateFields(modalData.current_fields)
  } else if (fieldSelector.value !== '' && modalSearchBar.value === '') {
    // Delete old fields and update field selector with all host fields
    updateFields(modalData.all_host_fields)
  }

  const modalContent = document.querySelector('#modal-content')
  const content = document.querySelector('#contentPreTag')

  // Deleting previously displayed results
  content.textContent = ''
  modalContent.appendChild(content)

  // Set the length of current data to modalDataLength variable
  modalDataLength = modalData.data_length

  // Defining variable to store highlighted data
  let filteredData

  // RegEx expression to search for all occurences of user's search word
  const userSearchWordRegex = new RegExp(modalSearchBar.value, 'ig')

  if (modalSearchBar.value !== '' && modalSearchBar.value.length >= 3) {
    // Adding syntax highlighting
    filteredData = `<span style=color:darkred>${modalData.data_for_modal
          .replace(userSearchWordRegex, '<span style=color:blue>$&</span>')// highlight words that user is searching for
          .replaceAll('\\n', '<br>')// replace newline characters with break elements to display data properly
          .replaceAll('\\"\\"', '""')
          .replaceAll('\\"', ' ')
        }</span>`
  } else {
    // Adding syntax highlighting
    filteredData = `<span style=color:darkred>${modalData.data_for_modal
      .replaceAll('\\n', '<br>')
      .replaceAll('\\"\\"', '""')
      .replaceAll('\\"', ' ')
        }</span>`
  }

  // Select element that shows how many occurrences of the search phrase we found
  const modalSearchStatistics = document.querySelector('#modalResults')

  // Deleting previously displayed results
  modalSearchStatistics.textContent = ''

  // If there was any search phrase occurence, show the message
  if (modalSearchBar.value !== '' && modalData.search_word_occurrences === 0) {
    modalSearchStatistics.textContent = 'No occurrences found..'
    return
  } else if (modalSearchBar.value !== '' && modalData.search_word_occurrences === 1) {
    modalSearchStatistics.textContent = `Found ${modalData.search_word_occurrences} occurrence..`
  } else if (modalSearchBar.value !== '' && modalData.search_word_occurrences > 0) {
    modalSearchStatistics.textContent = `Found ${modalData.search_word_occurrences} occurrences..`
  }

  // If length of the data is smaller or equal to modalDataPartTo variable, disable the next pagination button
  if (modalDataPartTo >= modalDataLength) {
    paginationButtonsActions('modal-disable-next')
  } else {
    paginationButtonsActions('modal-activate-next')
  }

  // If we fetch data from the start, disable previous pagination button
  if (modalDataPartFrom === 0) {
    paginationButtonsActions('modal-disable-previous')
  }

  if (modalData.data_length === 0 || modalData.data_for_modal === '[]' || modalData.data_for_modal === '{}') {
    content.innerHTML = `Field ${fieldSelector.value} is empty..`
  } else {
    content.innerHTML = filteredData
  }

  // After updating modal data, we can allow onchange functions again
  onchangeFunctionsAllowed = true
}

// Function to create new headers, add onclick functions and update data in the data table
async function updateTable (tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields) {
  // This variable stores phrase searched by the user
  let searchInputBarValue = document.querySelector('#searchBar').value

  // Select element that shows how many results we found in what time
  const searchStatistics = document.querySelector('#results')

  // If no search is specified, search for all results
  if (searchInputBarValue === '') {
    searchInputBarValue = '*'
  }

  try {
    // Deleting previously displayed content and displaying "Loading" message
    const tableBody = document.querySelector('#table-body')
    removeAllChildNodes(tableBody)
    searchStatistics.textContent = ''
    const noDataMessage = document.createElement('h4')
    noDataMessage.className = 'p-2'
    noDataMessage.textContent = 'Loading..'
    tableBody.appendChild(noDataMessage)

    // Time before fetch
    const currentTime = Date.now()

    // Fetching data from specified api endpoint
    const response = await fetchRequest(`${URL}${endpoint}/${searchInputBarValue}/${requiredFields}/${fetchDataFrom + '-' + searchSize}/${sortField + '-' + sortOrder}/${dataCardFilterField}`)

    if (response.status === 200) {
      const jsonResponse = JSON.parse(await response.json())

      // Update number of results on every fetch request
      numberOfResults = jsonResponse.number_of_results

      // If we reached the last part of the data, disable pagination next button
      if ((fetchDataFrom + searchSize) > numberOfResults) {
        paginationButtonsActions('view-disable-next')
      } else {
        paginationButtonsActions('view-activate-next')
      }

      // Time after fetch
      const timeAfterFetch = Date.now() - currentTime

      // Display the search statistics only when we find some results
      if (numberOfResults > 0 && fetchDataFrom === 0) {
        // Deleting displayed search statistics before we display the new ones
        searchStatistics.textContent = ''

        // We display different results when containers filter is selected,
        // because we want to display number of containers that we have found
        // instead of number of hosts whose data contain those containers
        if (filter === 'containers') {
          searchStatistics.textContent = `Found ${jsonResponse.number_of_containers} results in ${(timeAfterFetch) / 1000} seconds..`
        } else {
          searchStatistics.textContent = `Found ${numberOfResults} results in ${(timeAfterFetch) / 1000} seconds..`
        }
      }

      // This if statement ensures that we only create headers once
      if (fetchDataFrom === 0) {
        // Run function to update data cards
        // First parameter is data for the data cards that we fetched from API
        // Second parameter is specification of what data cards we want to create
        // and their values
        updateDataCards(jsonResponse.data.data_cards_data, dataCardsSpecifications)

        // Disable previous pagination button
        paginationButtonsActions('view-disable-previous')

        // Delete everything from table head
        const tableHead = document.querySelector('#table-head')
        removeAllChildNodes(tableHead)

        // Creating new header columns
        const tableHeaderRow = document.createElement('tr')
        for (const column in tableColumnsSpecifications) {
          const newColumn = document.createElement('th')
          newColumn.textContent = column
          // Disable sorting functionality in containers view
          if (filter !== 'containers') {
            // Onclick, add sorting into query
            newColumn.onclick = delayRequest(function () {
              sortField = tableColumnsSpecifications[column]
              sortOrder = !sortOrder
              fetchData()
            }, 300)
          }
          tableHeaderRow.appendChild(newColumn)
        }

        // Appending new row of headers to the table
        tableHead.appendChild(tableHeaderRow)
      }

      // Looping over table data and adding it to the table body
      const tableContent = document.querySelector('#table-body')

      // Deleting "Loading" message
      removeAllChildNodes(tableContent)

      for (const tableData of jsonResponse.data.table_data) {
        // Creating new table row element for every part of the data
        const newRow = document.createElement('tr')

        // Set First column variable to true so we can add click icon to the first column
        // This is so we only add it to the first column and not to every single one
        let firstColumn = true

        // Creating columns based on data from tableColumnsSpecifications object that we got as an function argument
        for (const currentColumn in tableColumnsSpecifications) {
          const newColumn = document.createElement('td')

          // We want to add icon to the first column to show that more data are available on click
          // If this is first column, add click icon
          if (firstColumn) {
            if (filter === 'hosts') {
              newColumn.innerHTML = '<span class="fa-solid fa-circle text-success ms-1 me-2 "></span>'
            } else {
              newColumn.innerHTML = '<span class="fa-solid fa-arrow-up-right-from-square ms-1 me-2 "></span>'
            }

            // And then set firstColumn to false to have that icon only in the first column.
            firstColumn = false
          }

          // Data for some views have to be specified further because
          // they might be stored as an object instead of a string

          // Vulnerabilities view specifications
          if (currentColumn === 'Trivy Vulnerabilities') {
            newColumn.innerHTML += tableData.trivy.vulnerabilities_total

          // Host Assessment view specifications
          } else if (currentColumn === 'OpenSCAP Fail Total') {
            newColumn.innerHTML += tableData.openscap.fail_total

          // Every other view specifications
          } else {
            newColumn.innerHTML += tableData[tableColumnsSpecifications[currentColumn]]
          }
          newRow.appendChild(newColumn)
        }

        // Adding ability to open modal on click
        newRow.setAttribute('data-coreui-toggle', 'modal')
        newRow.setAttribute('data-coreui-target', '#searchModal')

        // Selecting modal elements
        const modalSearchBar = document.querySelector('#modalSearchBar')
        const modalTitle = document.querySelector('#modal-title')
        const fieldSelector = document.querySelector('#fields')
        const copyToClipboardButton = document.querySelector('#copyToClipboard')

        async function getModalData (requiredFields) {
          // Set hostname as a modal title if it's not empty
          if (tableData.hostname) {
            modalTitle.textContent = tableData.hostname
          } else {
            modalTitle.textContent = ''
          }

          // Set currently selected field to selectedField variable
          let selectedField = fieldSelector.value

          // Set it to allFields if there is no currently no selected field
          // This way we will retrieve all fields from the database
          if (selectedField === '') {
            selectedField = 'allFields'
          } else {
            // Add all selected fields separated with "-" character
            // into selectedField variable
            // Separating fields with hyphen (-) is required
            selectedField = select.selected().join('-')
          }

          copyToClipboardButton.onclick = delayRequest(async function () {
            // Getting complete data to copy into the clipboard
            let response
            if (modalSearchBar.value !== '' && modalSearchBar.value.length >= 3) {
              response = await fetchRequest(`${URL}/v1/get-modal-data/${elasticsearchIndex}/${tableData.id}/${requiredFields}/${selectedField}/${modalSearchBar.value}/0-0`)
            } else {
              response = await fetchRequest(`${URL}/v1/get-modal-data/${elasticsearchIndex}/${tableData.id}/${requiredFields}/${selectedField}/no_search_word/0-0`)
            }
            const jsonResponse = await response.json()

            // Adding data into the clipboard
            navigator.clipboard.writeText(jsonResponse.data_for_modal)

            // Making alert to let user know that copying was successful
            window.alert('Data succesfully copied to clipboard.')
          }, 1000)

          // Fetching and returning specified part of the data as a function output
          let response
          if (modalSearchBar.value !== '' && modalSearchBar.value.length >= 3) {
            response = await fetchRequest(`${URL}/v1/get-modal-data/${elasticsearchIndex}/${tableData.id}/${requiredFields}/${selectedField}/${modalSearchBar.value}/${modalDataPartFrom + '-' + modalDataPartTo}`)
          } else {
            response = await fetchRequest(`${URL}/v1/get-modal-data/${elasticsearchIndex}/${tableData.id}/${requiredFields}/${selectedField}/no_search_word/${modalDataPartFrom + '-' + modalDataPartTo}`)
          }
          const jsonResponse = await response.json()
          return jsonResponse
        }

        // Function to set different onclick functions for every view
        function addOnClickFunction (requiredFields) {
          newRow.onclick = async function () {
            if (onchangeFunctionsAllowed) {
              // Block the onchange functions before we finish everything
              onchangeFunctionsAllowed = false

              // Deleting previously displayed results
              const content = document.querySelector('#contentPreTag')
              content.textContent = ''

              // Deleting previously displayed results
              const modalSearchStatistics = document.querySelector('#modalResults')
              modalSearchStatistics.textContent = ''

              // Reseting state of the pagination previous button
              paginationButtonsActions('modal-disable-previous')

              // Deleting previously displayed fields
              fieldSelector.length = 0

              // Setting data part variables to default value
              modalDataPartFrom = 0
              modalDataPartTo = modalDataPartSize
              updateModalData(await getModalData(requiredFields))

              // Updating function that we want to use to fetch data
              currentFetchDataFunction = async function () {
                if (onchangeFunctionsAllowed) {
                  // Block the onchange functions before we finish everything
                  onchangeFunctionsAllowed = false
                  updateModalData(await getModalData(requiredFields))
                }
              }
            }

            // Adding new oninput function anytime user clicks on another result
            // Delaying request to prevent creating a chain of requests anytime
            // user clicks the button multiple times in a short amount of time
            modalSearchBar.oninput = delayRequest(async function () {
              if (modalSearchBar.value === '' || modalSearchBar.value.length >= 3) {
                // Setting data part variables to default value
                modalDataPartFrom = 0
                modalDataPartTo = modalDataPartSize
                updateModalData(await getModalData(requiredFields))
              }
            }, 1000)

            // Adding onchange function
            fieldSelector.onchange = async function () {
              // Without this statement, we would get into
              // inifinite loop because when we run
              // updateModalData function, field selector
              // is updated as well which activates this onchange
              // function thus causing the infinite loop.
              if (onchangeFunctionsAllowed) {
                // Setting data part variables to default value
                modalDataPartFrom = 0
                modalDataPartTo = modalDataPartSize
                updateModalData(await getModalData(requiredFields))
              }
            }
          }
        }

        // HOSTS ONCLICK FUNCTION
        if (filter === 'hosts') {
          addOnClickFunction('allFields')

        // CONTAINERS ONCLICK FUNCTION
        } else if (filter === 'containers') {
          addOnClickFunction('docker_*')

        // SOFTWARE ONCLICK FUNCTION
        } else if (filter === 'software') {
          addOnClickFunction('packages-gem-pip-pip3-windows_software-snaps')

        // VULNERABILITIES ONCLICK FUNCTION
        } else if (filter === 'vulnerabilities') {
          addOnClickFunction('trivy')

        // HOST ASSESSMENT ONCLICK FUNCTION
        } else if (filter === 'hostAssessment') {
          addOnClickFunction('openscap')

        // EVENTS ONCLICK FUNCTION
        } else if (filter === 'events') {
          addOnClickFunction('allFields')

        // AUDIT ONCLICK FUNCTION
        } else if (filter === 'audit') {
          addOnClickFunction('allFields')

        // CHANGES ONCLICK FUNCTION
        } else if (filter === 'changes') {
          addOnClickFunction('allFields')
        } else {
          newRow.onclick = function () {}
        }

        // Appending new row to the table body for every part of data
        tableContent.appendChild(newRow)
      }
      // When user inserts search word and clicks on data card that
      // has no results binded to that word, display alert with error message.
    } else {
      searchStatistics.textContent = ''
      paginationButtonsActions('view-disable-both')

      // Delete everything from table header, body and data cards
      const tableHead = document.querySelector('#table-head')
      const tableBody = document.querySelector('#table-body')
      const dataCards = document.querySelector('#dataCards')
      removeAllChildNodes(tableHead)
      removeAllChildNodes(tableBody)
      removeAllChildNodes(dataCards)
      const noDataMessage = document.createElement('h4')
      noDataMessage.className = 'p-2'
      noDataMessage.textContent = 'No data available..'
      tableBody.appendChild(noDataMessage)
    }
  } catch {
    // On error, delete search statistics
    searchStatistics.textContent = ''
    paginationButtonsActions('view-disable-both')
  }
}

// ========== VIEW PAGINATION FUNCTIONALITY ==========

// Selecting pagination buttons elements
const paginationPreviousButton = document.querySelector('#paginationPreviousButton')
const paginationNextButton = document.querySelector('#paginationNextButton')

// Setting function to "previous" pagination button
// Delaying request to prevent creating a chain of requests anytime
// user clicks the button multiple times in a short amount of time
paginationPreviousButton.onclick = delayRequest(function () {
  // Deduct value of searchSize variable from fetchDataFrom to get previous part of the data
  fetchDataFrom -= searchSize
  fetchData()

  // Disable pagination previous button when we get to the start of the data
  if (fetchDataFrom === 0) {
    paginationButtonsActions('view-disable-previous')
  }
}, 1000)

// Setting function to "next" pagination button
// Delaying request to prevent creating a chain of requests anytime
// user clicks the button multiple times in a short amount of time
paginationNextButton.onclick = delayRequest(function () {
  // Make pagination previous button clickable
  paginationButtonsActions('view-activate-previous')

  // Add the value of searchSize variable to fetchDataFrom to get next part of the data
  fetchDataFrom += searchSize
  fetchData()
}, 1000)

// ========== MODAL PAGINATION FUNCTIONALITY ==========

// Selecting pagination buttons elements
const modalPaginationPreviousButton = document.querySelector('#modalPaginationPreviousButton')
const modalPaginationNextButton = document.querySelector('#modalPaginationNextButton')

// Setting function to "previous" pagination button
// Delaying request to prevent creating a chain of requests anytime
// user clicks the button multiple times in a short amount of time
modalPaginationPreviousButton.onclick = delayRequest(function () {
  modalDataPartFrom = modalDataPartFrom - modalDataPartSize
  modalDataPartTo = modalDataPartTo - modalDataPartSize
  if (modalDataPartFrom === 0) {
    paginationButtonsActions('modal-disable-previous')
  }
  currentFetchDataFunction()
}, 1000)

// Setting function to "next" pagination button
// Delaying request to prevent creating a chain of requests anytime
// user clicks the button multiple times in a short amount of time
modalPaginationNextButton.onclick = delayRequest(function () {
  if (modalDataPartFrom === 0) {
    paginationButtonsActions('modal-activate-previous')
  }

  modalDataPartFrom = modalDataPartTo
  modalDataPartTo = modalDataPartTo + modalDataPartSize
  currentFetchDataFunction()
}, 1000)

// Function to specify what data we want to have in the data table
// based on what filter is selected
function fetchData () {
  // Here we specify all the data we want to display
  // Specifying data for HOSTS view
  if (filter === 'hosts') {
    // Data for the datatable
    // Key of the object "tableColumnsSpecifications" is what we want to display in the header of the data table
    // Value of the object "tableColumnsSpecifications" is the data that we want to display for the specified header
    // We make a fetch request to get the data we need as a dictionary and the value
    // of object "tableColumnsSpecifications" is a key of that dictionary and value of that is the data we need.
    const tableColumnsSpecifications = {
      Hostname: 'hostname',
      'IP Address': 'ip_address',
      Platform: 'platform',
      'Asset Type': 'asset_type',
      Cloud: 'cloud',
      Tags: 'tags',
      'Last Check-In': 'last_run'
    }

    // Data to show in the data cards
    const dataCardsSpecifications = {
      Total: { fieldName: 'total', icon: 'fas fa-chart-line fa-2x' },
      Linux: { fieldName: 'linux', icon: 'fab fa-linux fa-2x' },
      Windows: { fieldName: 'windows', icon: 'fab fa-windows fa-2x' }
    }

    // Fields that we want to retrieve
    const requiredFields = 'id-hostname-ip_address-docker_containers-os-platform-asset_type-cloud-tags-last_run'

    // Specifying the endpoint we want to fetch data from
    const endpoint = '/v1/list-hosts'

    // Specifying the elasticsearchIndex to get data from
    const elasticsearchIndex = 'hosts'

    // Call updateTable function with that data
    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for CONTAINERS view
  } else if (filter === 'containers') {
    const tableColumnsSpecifications = {
      Hostname: 'hostname',
      Container: 'container',
      'Image Name': 'image_name',
      State: 'state',
      Status: 'status',
      Size: 'size',
      'Created Date': 'created',
      'Container Image': 'image'
    }

    const dataCardsSpecifications = {
      Containers: { fieldName: 'total_containers', icon: 'fa-solid fa-box fa-2x' },
      Running: { fieldName: 'running_containers', icon: 'fa-solid fa-circle-play fa-2x' },
      Paused: { fieldName: 'paused_containers', icon: 'fa-solid fa-circle-pause fa-2x' },
      Stopped: { fieldName: 'stopped_containers', icon: 'fa-solid fa-circle-stop fa-2x' },
      'Container Images': { fieldName: 'docker_images', icon: 'fa-solid fa-layer-group fa-2x' }
    }

    const requiredFields = 'id-hostname-docker_containers-docker_images-docker_running-docker_paused-docker_stopped'

    const endpoint = '/v1/list-containers'

    const elasticsearchIndex = 'hosts'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for SOFTWARE view
  } else if (filter === 'software') {
    const tableColumnsSpecifications = {
      Hostname: 'hostname',
      'IP Address': 'ip_address',
      Platform: 'platform',
      'Asset Type': 'asset_type',
      Cloud: 'cloud',
      Tags: 'tags',
      'Last Check-In': 'last_run'
    }

    const dataCardsSpecifications = {
      Total: { fieldName: 'total', icon: 'fas fa-chart-line fa-2x' },
      Linux: { fieldName: 'linux', icon: 'fab fa-linux fa-2x' },
      Windows: { fieldName: 'windows', icon: 'fab fa-windows fa-2x' }
    }

    const requiredFields = 'id-hostname-ip_address-docker_containers-os-platform-asset_type-cloud-tags-last_run'

    const endpoint = '/v1/list-software'

    const elasticsearchIndex = 'hosts'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for VULNERABILITIES view
  } else if (filter === 'vulnerabilities') {
    const tableColumnsSpecifications = {
      Hostname: 'hostname',
      'IP Address': 'ip_address',
      Platform: 'platform',
      'Trivy Vulnerabilities': 'trivy.vulnerabilities_total',
      'Last Check-In': 'last_run'
    }

    const dataCardsSpecifications = {
      'Total Vulnerabilities': { fieldName: 'total_vulnerabilities', icon: 'fa-solid fa-lock-open fa-2x' },
      'Critical Vulnerabilities': { fieldName: 'critical_vulnerabilities', icon: 'fa-solid fa-skull-crossbones fa-2x' },
      'High Vulnerabilities': { fieldName: 'high_vulnerabilities', icon: 'fa-solid fa-land-mine-on fa-2x' }
    }

    const requiredFields = 'id-hostname-ip_address-platform-trivy.vulnerabilities_total-last_run'

    const endpoint = '/v1/list-vulnerabilities'

    const elasticsearchIndex = 'hosts'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for HOST ASSESSMENT view
  } else if (filter === 'hostAssessment') {
    const tableColumnsSpecifications = {
      Hostname: 'hostname',
      'IP Address': 'ip_address',
      Platform: 'platform',
      'OpenSCAP Fail Total': 'openscap.fail_total',
      'Last Check-In': 'last_run'
    }

    const dataCardsSpecifications = {
      'OpenScap Checks Total': { fieldName: 'openscap_checks_total', icon: 'fa-solid fa-square-check fa-2x' },
      'OpenScap Pass Total': { fieldName: 'openscap_pass_total', icon: 'fa-solid fa-thumbs-up fa-2x' },
      'OpenScap Fixed Total': { fieldName: 'openscap_fixed_total', icon: 'fa-solid fa-screwdriver-wrench fa-2x' },
      'OpenScap Fail Total': { fieldName: 'openscap_fail_total', icon: 'fa-solid fa-square-xmark fa-2x' }
    }

    const requiredFields = 'id-hostname-ip_address-platform-openscap.fail_total-last_run'

    const endpoint = '/v1/list-host-assessment'

    const elasticsearchIndex = 'hosts'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for EVENTS view
  } else if (filter === 'events') {
    const tableColumnsSpecifications = {
      Hostname: 'hostname',
      'IP Address': 'ip_address',
      Date: 'timestamp',
      Impact: 'event_impact',
      'Event Name': 'event_name',
      Event: 'event_message'
    }

    const dataCardsSpecifications = {
      'Total Events': { fieldName: 'total_events', icon: 'fa-solid fa-paper-plane fa-2x' },
      'High Impact Events': { fieldName: 'high_impact_events', icon: 'fa-solid fa-dumpster-fire fa-2x' },
      'Medium Impact Events': { fieldName: 'medium_impact_events', icon: 'fa-solid fa-triangle-exclamation fa-2x' },
      'Low Impact Events': { fieldName: 'low_impact_events', icon: 'fa-solid fa-circle-exclamation fa-2x' },
      'Info Impact Events': { fieldName: 'info_impact_events', icon: 'fa-solid fa-circle-info fa-2x' }
    }

    const requiredFields = 'id-hostname-ip_address-timestamp-event_impact-event_name-event_message'

    const endpoint = '/v1/list-events'

    const elasticsearchIndex = 'events'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for AUDIT view
  } else if (filter === 'audit') {
    const tableColumnsSpecifications = {
      Event: 'event',
      'Updated By': 'updated_by',
      'Updated At': 'updated_at'
    }
    const dataCardsSpecifications = {}

    const requiredFields = 'allFields'

    const endpoint = '/v1/list-audit'

    const elasticsearchIndex = 'audit'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)

    // Specifying data for CHANGES view
  } else if (filter === 'changes') {
    const tableColumnsSpecifications = {
      'Changes Summary': 'changes_summary',
      'Changes Discovered': 'changes_discovered'
    }
    const dataCardsSpecifications = {}

    const requiredFields = 'id-changes_summary-changes_discovered'

    const endpoint = '/v1/list-changes'

    const elasticsearchIndex = 'changes'

    updateTable(tableColumnsSpecifications, dataCardsSpecifications, endpoint, elasticsearchIndex, requiredFields)
  }
}

// Getting data when page loads
fetchData()

// Event listener to listen for search bar input
// On input run userSearch function to fetch data matching the searched word
const searchInputBar = document.querySelector('#searchBar')
searchInputBar.oninput = delayRequest(function () {
  userSearch()
}, 1000)

// Function to reset variables and run fetchData function anytime filter changes
function filterChange () {
  // Reset search statistics anytime different filter is selected
  const searchStatistics = document.querySelector('#results')
  searchStatistics.textContent = ''

  // Any time filter changes, disable pagination previous button
  paginationButtonsActions('view-disable-previous')

  // Reset fetchDataFrom variable to fetch new data from the beggining
  fetchDataFrom = 0

  // Reset sort related variables to default values
  sortField = 'none'
  sortOrder = false

  // Reset data card filters related variables to default values
  dataCardFilterField = 'none'
  selectedCardFilter = 'none'

  // After updating all variables, fetch new data and display them
  fetchData()
}

// Adding onclick function for every filter
// When user selects new filter, we update variables related to data fetching
// to fetch specific size and part of data and then fetch new data and display them.

// HOSTS FILTER
const hostsFilter = document.querySelector('#hostsFilter')
hostsFilter.addEventListener('click', delayRequest(function () {
  // Change how many results we want to fetch at once for every filter separately
  searchSize = 20

  // Update filter to selected value and fetch and display data accordingly
  filter = 'hosts'

  // Run function to reset variables and run fetchData function
  filterChange()
}, 300))

// CONTAINERS FILTER
const containersFilter = document.querySelector('#containersFilter')
containersFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'containers'
  filterChange()
}, 300)

// SOFTWARE FILTER
const softwareFilter = document.querySelector('#softwareFilter')
softwareFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'software'
  filterChange()
}, 300)

// VULNERABILITIES FILTER
const vulnerabilitiesFilter = document.querySelector('#vulnerabilitiesFilter')
vulnerabilitiesFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'vulnerabilities'
  filterChange()
}, 300)

// HOST ASSESSMENT FILTER
const hostAssessmentFilter = document.querySelector('#hostAssessmentFilter')
hostAssessmentFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'hostAssessment'
  filterChange()
}, 300)

// EVENTS FILTER
const eventsFilter = document.querySelector('#eventsFilter')
eventsFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'events'
  filterChange()
}, 300)

// AUDIT FILTER
const auditFilter = document.querySelector('#auditFilter')
auditFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'audit'
  filterChange()
}, 300)

// CHANGES FILTER
const changesFilter = document.querySelector('#changesFilter')
changesFilter.onclick = delayRequest(function () {
  searchSize = 20
  filter = 'changes'
  filterChange()
}, 300)

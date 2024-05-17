import { CSRFTOKENURL } from './config.min.js'

async function getCsrfToken () {
  let csrfToken = await fetch(CSRFTOKENURL, {
    method: 'GET',
    body: null,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include'
  })

  if (csrfToken.status === 200) {
    csrfToken = JSON.parse(await csrfToken.json())
    return csrfToken.csrf_token
  } else {
    return null
  }
}

// Function to handle all fetch requests
export async function fetchRequest (apiUrl, method = 'GET', body = null, headers = { 'Content-Type': 'application/json' }) {
  // headers['X-CSRFToken'] = await getCsrfToken()
  const res = fetch(apiUrl, {
    method: method,
    body: body,
    headers: headers,
    credentials: 'include'
  })
  return res
}

// Function to remove all child data of parent element
export function removeAllChildNodes (parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild)
  }
}

// Function to transfer all strings to title case
export function titleCase (str) {
  return str.toLowerCase().replace(/\b(\w)/g, s => s.toUpperCase())
}

// Function that is used to make fetch request after user stops typing searched word
// instead on doing fetch request on every input
export function delayRequest (fn, delay) {
  let timer = null
  return function () {
    const context = this; const args = arguments
    clearTimeout(timer)
    timer = setTimeout(function () {
      fn.apply(context, args)
    }, delay)
  }
}

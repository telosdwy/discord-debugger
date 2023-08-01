// https://stackoverflow.com/a/179514
function deleteAllCookies() {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
    }
    location.reload();
}

// https://www.w3schools.com/js/js_cookies.asp
function getCookie(key) {
  key += '=';
  let cookies = decodeURIComponent(document.cookie).split(';');
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i];
    while (cookie.charAt(0) == ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(key) == 0) {
      return cookie.substring(key.length, cookie.length);
    }
  }
  return '';
}

function load() {
  let access_token = getCookie('access_token');
  let scopes = getCookie('scope');
  document.getElementById('access_token').innerHTML += '<code>' + access_token + '</code>';
  document.getElementById('scopes').innerHTML = scopes;
}

function request(route, ipc = false) {
  let href = ipc ? `/ipc/request?route=${route}` : `/request?route=${route}`;
  let inputs = document.getElementsByTagName('input');
  for (let input of inputs) {
    if (input.id.startsWith(route + '/')) {
      href += `&${input.id.replace(route + '/', '')}=${input.value}`;
    }
  }
  if (!window.confirm('Transferring you over to ' + href)) {
    return;
  }
  location.href = href;
}

function change() {
  for (let element of document.getElementsByTagName('div')) {
    element.style.display = 'none';
  }
  document.getElementById(routes_select.value).style.display = 'block';
}

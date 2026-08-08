// Reads the CSRF token Django sets as a cookie, so fetch() POSTs pass CSRF protection.
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const CSRF_TOKEN = getCookie('csrftoken');



const Http = new XMLHttpRequest();
const url='http://localhost:3000/toolkit-result';
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => {
  console.log(Http.responseText)
}
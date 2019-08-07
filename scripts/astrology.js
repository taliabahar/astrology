function hover(element) {
  let sign = element.parentNode.id.toLowerCase();
  let goldStringSign = `../media/gold-png/${sign}-gold.png`;
  element.setAttribute('src', goldStringSign);
  element.previousElementSibling.style.textShadow = "#FFDD20 0px 0px 3px";
}

function unhover(element) {
  let sign = element.parentNode.id.toLowerCase();
  let stringSign = `../media/png/${sign}.png`;
  element.setAttribute('src', stringSign);
  element.previousElementSibling.style.textShadow = "none";
}

$(document).ready(function() {
  $('img.thumbnail').click(function() {
    window.location.href =  "sun_signs/" + this.alt + '.html';
  });
});

$(document).ready(function() {
  $('#cat').click(function() {
    let loc = window.location.pathname;
    let dir = loc.substring(0, loc.lastIndexOf('/'));
    window.location.href =  dir + "/cat";
  });
});

$(document).ready(function() {
  $('#horoscope').click(function() {
    let loc = window.location.pathname;
    let dir = loc.substring(0, loc.lastIndexOf('/'));
    window.location.href =  dir + "/horoscope";
  });
});

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
$(document).ready(function() {
  $('#pickSign').click(function() {
    let loc = window.location.pathname;
    let dir = loc.substring(0, loc.lastIndexOf('/'));
    window.location.href =  dir + "/sign";
  });
});
$(document).ready(function() {
  $('#home').click(function() {
    let loc = window.location.pathname;
    let dir = loc.substring(0, loc.lastIndexOf('/'));
    window.location.href =  dir + "/";
  });
});

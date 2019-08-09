

$(document).ready(function() {
  $('#profile-button').click(function() {
    let loc = window.location.pathname;
    let dir = loc.substring(0, loc.lastIndexOf('/'));
    window.location.href =  dir + "/profile.html";
  });
});

/*
 * main.js
 * Primary javascript functionality for every page in the Kahu app.
 */

(function($) {

// Update the status and the version from the API.
  var statusURL = "/api/status/";
  $.get(statusURL)
    .success(function(data) {
      if (data.status == "ok") {
        $("#footerStatus").addClass("text-success");
      } else {
        $("#footerStatus").addClass("text-warning");
      }
    })
    .fail(function() {
      $("#footerStatus").addClass("text-danger");
    });

    console.log("Kahu App is started and ready");

})(jQuery)

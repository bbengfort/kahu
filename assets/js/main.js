/*
 * main.js
 * Primary javascript functionality for every page in the Kahu app.
 */

(function($) {

  $(document).ready(function() {

    // Update the status and the version from the API.
    $.ajax({
      type: "GET",
      url: "/api/status/",
      success: function(data) {
        if (data.status == "ok") {
          $("#footerStatus").addClass("text-success");
        } else {
          $("#footerStatus").addClass("text-warning");
        }
      },
      fail: function() {
        $("#footerStatus").addClass("text-danger");
      }
    });

    // Toggle the side navigation
    $("#sidenavToggler").click(function(e) {
      e.preventDefault();
      $("body").toggleClass("sidenav-toggled");
      $(".navbar-sidenav .nav-link-collapse").addClass("collapsed");
      $(".navbar-sidenav .sidenav-second-level, .navbar-sidenav .sidenav-third-level").removeClass("show");
    });
  });

})(jQuery)

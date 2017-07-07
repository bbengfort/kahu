/*
 * machines.js
 * Primary javascript functionality for the machines application.
 */

 (function($) {

  $(document).on('turbolinks:load', function() {
      // Register the clickable row handler
      $(".clickable-row").click(function() {
        window.location = $(this).data("href");
      });

      // Register the copy input handler
      $(".pbcopy").click(function() {
        var input = $(this).parents(".input-group").children("input");
        input.select();
        document.execCommand("copy");
        input.blur();
      });

  });

})(jQuery)

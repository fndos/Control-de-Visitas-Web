$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w.]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  $("form").validate({
    rules: {
      username_or_email: {
        required: true,
      }
    },
    messages: {
      username_or_email: {
        required: 'Este campo es obligatorio.',
      },
    }
  });

});

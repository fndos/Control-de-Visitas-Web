$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w.]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  $("form").validate({
    rules: {
      name: {
        required: true
      },
      description: {
        required: true
      }
    },
    messages: {
      name: {
        required: 'Este campo es obligatorio.',
      },
      description: {
        required: 'Este campo es obligatorio.',
      }
    }
  });

});

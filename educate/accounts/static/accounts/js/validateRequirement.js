$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w.]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  $("form").validate({
    rules: {
      reason: {
        required: true
      },
      school: {
        required: true
      },
      type: {
        required: true
      }
    },
    messages: {
      reason: {
        required: 'Este campo es obligatorio.',
      },
      school: {
        required: 'Este campo es obligatorio.',
      },
      type: {
        required: 'Este campo es obligatorio.',
      }
    }
  });

});

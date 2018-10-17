$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w.]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  $("form").validate({
    rules: {
      username: {
        required: true,
        alphanumeric: true,
        minlength: 4,
        maxlength: 30
      },
      password: {
        required: true,
        minlength: 8,
        maxlength: 100
      }
    },
    messages: {
      username: {
        required: 'Este campo es obligatorio.',
        alphanumeric: 'Sólo se permiten letras, números y puntos',
        minlength: 'Este campo debe tener mínimo {0} carácteres.',
        maxlength: 'Este campo debe tener máximo {0} carácteres.'
      },
      password: {
        required: 'Este campo es obligatorio.',
        minlength: 'Este campo debe tener como mínimo {0} carácteres.',
        maxlength: 'Este campo debe tener como máximo {0} carácteres.'
      }
    }
  });

});

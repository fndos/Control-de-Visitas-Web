$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w.]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  $("form").validate({
    rules: {
      dni: {
        required: true,
        minlength: 10,
        maxlength: 10,
        digits: true
      },
      first_name: {
        required: true,
        lettersonly: true,
        normalizer: function(value) {
          return $.trim(value);
        }
      },
      last_name: {
        required: true,
        lettersonly: true,
        normalizer: function(value) {
          return $.trim(value);
        }
      },
      username: {
        required: true,
        alphanumeric: true,
        minlength: 5,
        maxlength: 30
      },
      password: {
        required: true,
        minlength: 8,
        maxlength: 100
      },
      email: {
        required: true,
        email: true
      },
      phone_number: {
        required: true
      },
      user_type: {
        required: true
      }
    },
    messages: {
      dni: {
        required: 'Este campo es obligatorio.',
        minlength: 'Las cédulas poseen ({0}) dígitos.',
        maxlength: 'Las cédulas poseen ({0}) dígitos.',
        digits: 'Sólo se permiten dígitos.'
      },
      first_name: {
        required: 'Este campo es obligatorio.',
        lettersonly: "Sólo se permiten letras."
      },
      last_name: {
        required: 'Este campo es obligatorio.',
        lettersonly: "Sólo se permiten letras."
      },
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
      },
      email: {
        required: 'Este campo es obligatorio',
        email: 'Este campo debe tener un email válida.'
      },
      phone_number: {
        required: 'Este campo es obligatorio.'
      },
      user_type: {
        required: 'Este campo es obligatorio.'
      }
    }
  });

});

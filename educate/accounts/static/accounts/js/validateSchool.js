$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  $("form").validate({
    rules: {
      amie: {
        required: true,
        minlength: 8,
        maxlength: 8,
        alphanumeric: true
      },
      name: {
        required: true
      },
      phone_number: {
        required: true
      },
      address: {
        required: true
      },
      reference: {
        required: true
      },
      parish: {
        required: true,
        lettersonly: true,
        normalizer: function(value) {
          return $.trim(value);
        }
      },
      priority: {
        required: true
      },
      sector: {
        required: true
      },
      ambassador_in: {
        required: true,
        lettersonly: true,
        normalizer: function(value) {
          return $.trim(value);
        }
      },
      work_day: {
        required: true
      }
    },
    messages: {
      amie: {
        required: 'Este campo es obligatorio.',
        minlength: 'El AMIE debe poseer ({0}) dígitos.',
        maxlength: 'El AMIE debe poseer ({0}) dígitos.',
        alphanumeric: 'Sólo se permiten letras y números'
      },
      name: {
        required: 'Este campo es obligatorio.'
      },
      phone_number: {
        required: 'Este campo es obligatorio.'
      },
      address: {
        required: 'Este campo es obligatorio.'
      },
      reference: {
        required: 'Este campo es obligatorio.'
      },
      parish: {
        required: 'Este campo es obligatorio',
        lettersonly: "Sólo se permiten letras."
      },
      priority: {
        required: 'Este campo es obligatorio.'
      },
      sector: {
        required: 'Este campo es obligatorio.'
      },
      ambassador_in: {
        required: 'Este campo es obligatorio',
        lettersonly: "Sólo se permiten letras."
      },
      work_day: {
        required: 'Este campo es obligatorio'
      }
    }
  });

});

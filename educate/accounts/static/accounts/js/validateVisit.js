$(document).ready(function () {

  jQuery.validator.addMethod("lettersonly", function(value, element) {
    return this.optional(element) || /^([abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZáéíóú ])+$/i.test(value);
  }, "Letters only please");

  jQuery.validator.addMethod("alphanumeric", function(value, element) {
    return this.optional(element) || /^[\w.]+$/i.test(value);
  }, "Letters, numbers, and . only please");

  jQuery.validator.addMethod('checkdate', function (value, element) {
    var str = value;
    var fecha_hora = new Array();
    var fecha = new Array();
    var hora = new Array();
    var dd, mm, yyyy, H, MM;
    fecha_hora = str.split(" ");
    fecha = fecha_hora[0].split("-");
    hora = fecha_hora[1].split(":");
    yyyy = fecha[0];
    mm = fecha[1];
    dd = fecha[2];
    H = hora[0];
    MM = hora[1];
    try {
      var current = new Date();
      var date = new Date(yyyy,mm-1,dd,H,MM,current.getSeconds());
      console.log(date);
      console.log(current);
      return date > current;
    }
    catch(er) {
      return false;
    }
  }, 'Please use format DD MM YYYY.');

  $("form").validate({
    rules: {
      date_planned: {
        checkdate: true,
        required: true
      },
      requirement: {
        required: true
      },
      user: {
        required: true
      }
    },
    messages: {
      date_planned: {
        checkdate: 'Asegúrate que la fecha de la visita sea posterior a la fecha actual.',
        required: 'Este campo es obligatorio.',
      },
      requirement: {
        required: 'Este campo es obligatorio.',
      },
      user: {
        required: 'Este campo es obligatorio.',
      }
    }
  });

});

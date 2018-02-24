$(document).ready(function() {
    $('select').material_select();

    $.ajax({
        url: '/ajax/getcompanies',
        success: function(result) {
            var data = {};
            for (var key in eval(result)) {
                data[key] = null;
            }

            $('#id_company').autocomplete({
                data: data,
                limit: 10
            });
        }
    });

    $.ajax({
        url: '/ajax/getsectors',
        success: function(result) {
          var data = {};
          for (var key in eval(result)) {
              data[key] = null;
          }

            $('#id_sector').autocomplete({
                data: data,
                limit: 10
            });
        }
    });
});
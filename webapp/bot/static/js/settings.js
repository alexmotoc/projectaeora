$(document).ready(function() {
    $('select').material_select();

    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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

    $("#preferences-form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            url: "/settings/",
            type: "POST",
            data: $("#preferences-form").serialize(),
            success: function(result) {
                Materialize.toast(result.status, 3000, 'rounded');
            }
        });
    });
});
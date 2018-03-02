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
            var companies = {};
            for (var key in eval(result['companies'])) {
                companies[key] = null;
            }

            var saved_companies = [];

            result["saved_companies"].forEach(function(obj) {
                saved_companies.push({tag: obj.name});
            });

            $("#track-companies").material_chip({
                data: saved_companies,
                placeholder: "Track companies",
                secondaryPlaceholder: "+ Add company",
                autocompleteOptions: {
                    data: companies,
                    limit: Infinity,
                    minLength: 1
                }
            });
        }
    });

    $.ajax({
        url: '/ajax/getsectors',
        success: function(result) {
          var sectors = {};
          for (var key in eval(result['sectors'])) {
              sectors[key] = null;
          }

          var saved_sectors = [];

          result["saved_sectors"].forEach(function(obj) {
              saved_sectors.push({tag: obj.name});
          });

          $("#track-sectors").material_chip({
              data: saved_sectors,
              placeholder: "Track sectors",
              secondaryPlaceholder: "+ Add sector",
              autocompleteOptions: {
                  data: sectors,
                  limit: Infinity,
                  minLength: 1
              }
          });
        }
    });

    $("#track-companies").on("chip.add", function(e, chip) {
        var company_tags = $("#id_companies").val();
        $("#id_companies").val(company_tags + ", " + chip.tag);
    });

    $("#track-sectors").on("chip.add", function(e, chip) {
        var sector_tags = $("#id_sectors").val();
        $("#id_sectors").val(sector_tags + ", " + chip.tag);
    });

    $("#track-companies").on("chip.delete", function(e, chip) {
        var company_tags = $("#id_companies").val();
        $("#id_companies").val(company_tags.replace(chip.tag, "").replace(", ", ""));
    });

    $("#track-sectors").on("chip.delete", function(e, chip) {
        var sector_tags = $("#id_sectors").val();
        $("#id_sectors").val(sector_tags.replace(chip.tag, "").replace(", ", ""));
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
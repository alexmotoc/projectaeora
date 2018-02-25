jQuery(function ($) {
    $.fn.hScroll = function (amount) {
        amount = amount || 120;
        $(this).bind("DOMMouseScroll mousewheel", function (event) {
            var oEvent = event.originalEvent,
                direction = oEvent.detail ? oEvent.detail * -amount : oEvent.wheelDelta,
                position = $(this).scrollLeft();
            position += direction > 0 ? -amount : amount;
            $(this).scrollLeft(position);
            event.preventDefault();
        })
    };
});

$(document).ready(function() {
    $('.scrollable-container').hScroll();

    $('.tooltipped').tooltip({delay: 50});

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

    $('#ask-question').submit(function(e) {
        var form = this;
        e.preventDefault();

        $.ajax({
            url: "/chat/",
            type: "POST",
            data: {
                question: $("#id_question").val()
            },
            success: function(data) {
                var query = "<div class='bubble sent blue lighten-1'><span class='white-text'>" + $('#id_question').val() + "</span></div>";
                var reply = "<div class='bubble received blue lighten-1'><span class='white-text'>" + data["response"]["text"] + "</span></div>";
                $(form).before(query);
                $('#id_question').val('');
                $(form).before(reply);
            },
        });
    });
});

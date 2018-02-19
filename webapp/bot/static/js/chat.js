$(document).ready(function() {
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

    $("#send-text").click(function(e) {
        $("#ask-question").submit();
    });

    $("#ask-question").submit(function(e) {
        e.preventDefault();

        function processingQuery() {
            var query = "<div class='bubble sent blue lighten-1 scale-transition scale-out'><span class='white-text'>" + $('#id_question').val() + "</span></div>";
            $("#chat-history").append(query);
            $(".sent").last().removeClass("scale-out").addClass("scale-in");
            $("html, body").animate({ scrollTop: $(document).height() }, "slow");
            var bufferingCircle = "<div class='preloader-wrapper small active'>" +
                                      "<div class='spinner-layer spinner-blue-only'>" +
                                        "<div class='circle-clipper left'>" +
                                          "<div class='circle'></div>" +
                                        "</div><div class='gap-patch'>" +
                                          "<div class='circle'></div>" +
                                        "</div><div class='circle-clipper right'>" +
                                          "<div class='circle'></div>" +
                                        "</div>" +
                                      "</div>" +
                                    "</div>";
            var bufferingBubble = "<div id='buffering' class='bubble-interactive received'>" + bufferingCircle + "</div>";
            $("#chat-history").append(bufferingBubble);
            $("html, body").animate({ scrollTop: $(document).height() }, "slow");

            return $("#id_question").val();
        }

        var query = processingQuery();
        $("#id_question").val("");

        $.ajax({
            url: "/chat/",
            type: "POST",
            data: {
                question: query
            },
            success: function(data) {
                $("#buffering").remove();
                var reply = "<div class='bubble received blue lighten-1 scale-transition scale-out'><span class='white-text'>" + data["response"]["text"] + "</span></div>";
                $("#chat-history").append(reply);
                $(".received").last().removeClass("scale-out").addClass("scale-in");
                $("html, body").animate({ scrollTop: $(document).height() }, "slow");
            },
        });
    });
});

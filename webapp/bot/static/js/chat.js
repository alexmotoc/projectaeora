$(document).ready(function() {
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

    /* Return a string with the first letter capitalised */
    String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }

    $("#send-voice").click(function(e) {
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
            var recognition = new webkitSpeechRecognition();

            recognition.continuous = false;
            recognition.interimResults = true;

            recognition.lang = "en-GB";
            recognition.start();

            var final_transcript = '';

            recognition.onresult = function(event) {
                var interim_transcript = '';

                for (var i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        final_transcript += event.results[i][0].transcript;
                    } else {
                        interim_transcript += event.results[i][0].transcript;
                    }
                }

                final_transcript = interim_transcript.capitalize();
                $("#id_question").val(final_transcript);
            };

            recognition.onaudioend = function(event) {
                recognition.stop();
                $("#id_question").val(final_transcript);
                $("#ask-question").submit();
            }
      }
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

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

    var fetchReply = function(query) {
        return $.ajax({
            url: "/chat/",
            type: "POST",
            data: {
                question: query
            },
            success: function(data) {
                $("#buffering").remove();
                createReply(data);
            },
        });
    }

    function processingQuery() {
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

    function createReply(data) {
        var response = JSON.parse(data["response"]);

        var synth = window.speechSynthesis;
        var utterThis = new SpeechSynthesisUtterance(response['speech']);
        synth.speak(utterThis);

        switch(response["type"]) {
            case "company":
                break;
            case "news":
                break;
            case "top":
                var card = response["text"];
                var reply = "<div class='bubble-interactive received'>" +
                              "<div class='card white'>" +
                                "<div class='card-content black-text'>" +
                                  "<span class='card-title'>" + card["title"] + "</span>" +
                                  "<table class='striped'><thead><tr><th>Name</th><th>Price</th><th>%+/-</th></tr></thead>" +
                                  "<tbody>";

                card["companies"].forEach(function(obj) {
                    reply += "<tr><td>" + obj.name + "</td><td>" + obj.price +"</td>";

                    if (obj.percentage_change[0] == '+') {
                        reply += "<td class='green-text'>" + obj.percentage_change + "</td>";
                    } else {
                        reply += "<td class='red-text'>" + obj.percentage_change + "</td>";
                    }

                    reply += "</tr>";
                });

                reply += "</tbody></table></div></div></div>";
                break;
            default:
                var reply = "<div class='bubble received blue lighten-1 scale-transition scale-out'><span class='white-text'>" + data["response"]["text"] + "</span></div>";
        }

        $("#chat-history").append(reply);
        $(".received").last().removeClass("scale-out").addClass("scale-in");
        $("html, body").animate({ scrollTop: $(document).height() }, "slow");
    }

    $("#send-text").click(function(e) {
        if ($("#id_question").val() != "") {
            $("#ask-question").submit();
        }
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

            if (!$("#send-voice").hasClass("pulse")) {
                $("#send-voice").addClass("pulse");

                var finalTranscript = "";

                recognition.onspeechstart = function(event) {
                    var queryBubble = "<div class='bubble sent blue lighten-1 scale-transition scale-out'><span class='white-text'></span></div>";
                    $("#chat-history").append(queryBubble);
                    $(".sent").last().removeClass("scale-out").addClass("scale-in");
                    $("html, body").animate({ scrollTop: $(document).height() }, "slow");
                };

                recognition.onresult = function(event) {
                    var interimTranscript = "";

                    for (var i = event.resultIndex; i < event.results.length; ++i) {
                        if (event.results[i].isFinal) {
                            finalTranscript += event.results[i][0].transcript;
                        } else {
                            interimTranscript += event.results[i][0].transcript;
                        }
                    }

                    finalTranscript = interimTranscript.capitalize();
                    $(".sent").last().find('span').text(finalTranscript);
                };

                recognition.onspeechend = function(event) {
                    recognition.abort();
                    // $("#send-voice").removeClass("pulse");
                    processingQuery();
                    fetchReply(finalTranscript);
                }

                recognition.onend = function(event) {
                    recognition.abort();
                    $("#send-voice").removeClass("pulse");
                }
            } else {
                recognition.abort();
                $("#send-voice").removeClass("pulse");
            }
        }
    });

    $("#ask-question").submit(function(e) {
        e.preventDefault();
        var query = "<div class='bubble sent blue lighten-1 scale-transition scale-out'><span class='white-text'>" + $('#id_question').val() + "</span></div>";
        $("#chat-history").append(query);
        $(".sent").last().removeClass("scale-out").addClass("scale-in");
        $("html, body").animate({ scrollTop: $(document).height() }, "slow");

        processingQuery();
        $("#id_question").val("");
        fetchReply(query);
    });
});

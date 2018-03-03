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

function appendReply(history, voice, data) {
    if (voice) {
        var synth = window.speechSynthesis;
        var utterThis = new SpeechSynthesisUtterance(data['speech']);
        synth.speak(utterThis);
    }

    var reply = createReply(data);

    $("#chat-history").append(reply);

    if (!history) {
        $("html, body").animate({ scrollTop: $(document).height() }, "slow");
    }
}

function createReply(data) {
    var card = data["text"];
    var reply = '';

    switch(data["type"]) {
        case "company":
            reply +=  "<div class='bubble-interactive received'>" +
                          "<div class='card white'>" +
                            "<div class='card-content black-text'>" +
                              "<span class='card-title'>" + card["name"] + "</span>" +
                              "<p class='grey-text code-time'>" + card["code"] + "<br>" + card["date"] + "</p>" +
                              "<p class='black-text price-impact'" + getStyle(card['primary_type'], card['primary']) + card['primary'] + getUnits(card['primary_type']) +
                              "<br>" + getStyle(card['secondary_type'], card['secondary']) + card['secondary'] + getUnits(card['secondary_type']) + "</p>" +
                            "</div>" +
                          "</div>" +
                        "</div>";
            break;
        case "news":
            reply += "<div class='bubble-interactive received'><section class='scrollable-container'>";

            card.forEach(function(obj) {
                reply +=  "<div class='news-article'>" +
                   "<div class='card'>" +
                     "<div class='card-content'>" +
                       "<span class='card-title grey-text text-darken-4'>" + obj.headline + "</span>";

                if (obj.impact != "-") {
                    reply += "<span>" + getImpact(obj.impact) + obj.impact + "</span>";
                }

                reply += "<p>" + obj.summary+ "</p>"

                if (obj.keywords.length == 5) {
                    reply += "<blockquote>"
                    for (var i = 0; i < 5; i++) {
                        try {
                            reply += "<div class='chip'>" + obj.keywords[i] + "</div>"
                        } catch(err) {
                            break;
                        }
                    }
                    reply += "</blockquote>"
                }

                if (obj.sentiment != "none") {
                    reply += "<p class='grey-text'>Sentiment: ";
                    if (obj.sentiment == "positive"){
                        reply += "<span class='green-text'>Positive</span>"
                    }
                    else if (obj.sentiment == "neutral"){
                        reply += "<span class='grey-text'>Neutral</span>"
                    }
                    else if (obj.sentiment == "negative"){
                        reply += "<span class='red-text'>Negative</span>"
                    }
                    reply += "</p>"
                }

                reply += "<p class = 'grey-text'>Date published: " + obj.date + "</p>"
                reply += "<p class = 'grey-text'>Source: " + obj.source + "</p>"
                reply += "<div class='card-action'><p><a href=" + obj.url + ">Go to article</a></p></div>" +
                "</div></div></div>";
            });
            reply += "</section></div>";

            break;
        case "top":
            reply += "<div class='bubble-interactive received'>" +
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
        case "revenue":
            reply += "<div class = 'bubble-interactive received'>" +
                          "<div class = 'card white'>" +
                            "<div class = 'card-content black-text'>" +
                              "<span class = 'card-title'>" + card["title"] + "</span>" +
                              "<table class = 'striped'><thead><tr><th>Date</th><th>Revenue (&poundm)</th>" +
                              "<tbody>";

            card["revenue_data"].forEach(function(obj) {
                reply += "<tr><td>" + obj.date + "</td><td>" + obj.revenue +"</td><tr>";
            });

            reply += "</tbody></table></div></div></div>";
            break;
        case "briefing":
            card['companies'].forEach(function(obj) {
                reply += simpleReply("Here is the latest data on " + obj.name + ".");

                reply += "<div class='bubble-interactive received'>" +
                              "<div class='card white'>" +
                                "<div class='card-content black-text'>" +
                                  "<span class='card-title'>" + obj.name + "</span>" +
                                  "<table class='centered'><thead><tr>";

                reply += "<th>Price</th>";

                if ("high" in obj) {
                    reply += "<th>High</th>";
                }

                if ("low" in obj) {
                    reply += "<th>Low</th>";
                }

                if ("per_diff" in obj) {
                    reply += "<th>Percentage change</th>";
                }

                reply += "</tr></thead><tbody><tr>";

                reply += "<td>" + obj.price + "</td>";

                if ("high" in obj) {
                    reply += "<td>" + obj.high + "</td>";
                }

                if ("low" in obj) {
                    reply += "<td>" + obj.low + "</td>";
                }

                if ("per_diff" in obj) {
                    reply += "<td>" + getImpact(obj.per_diff) + obj.per_diff + "</span></td>";
                }

                reply += "</tr></tbody></table>";
                reply += "<p class='grey-text'>" + obj.date + "</p>";
                reply += "</div></div></div>";

                reply += simpleReply("Here are the latest news on " + obj.name + ".");

                reply += createReply(obj.news);
            });

            card['sectors'].forEach(function(obj) {
                reply += simpleReply("The highest price in " + obj.name + " is:");
                reply += createReply(obj.highest_price);

                reply += simpleReply("The lowest price in " + obj.name + " is:");
                reply += createReply(obj.lowest_price);

                reply += simpleReply("The rising companies in " + obj.name + " are:");
                reply += createReply(obj.rising);

                reply += simpleReply("The falling companies in " + obj.name + " are:");
                reply += createReply(obj.falling);

                if ("news" in obj) {
                    reply += simpleReply("Here are some news about " + obj.name + ".");
                    reply += createReply(obj.news);
                }
            });

            break;
        default:
            var reply = simpleReply(data['text']);
    }

    return reply;
}

function simpleReply(text) {
    return "<div class='bubble received blue lighten-1'><span class='white-text'>" + text + "</span></div>";
}

function getImpact(value) {
    if (value.charAt(0) == "+"){
        return "<span class='green-text'><i class='material-icons valign-icon'>trending_up</i>";
    }
    else if (value.charAt(0) == "-"){
        return "<span class='red-text'><i class='material-icons valign-icon'>trending_down</i>";
    }
}

function getStyle(attribute, value){
    if (attribute == "per_diff"){
        return getImpact(value);
    }
    else if (attribute == "high"){
        return "<span class='black-text'>High: ";
    }
    else if (attribute == "low"){
        return "<span class='black-text'>Low: ";
    }
    else if (attribute == "market_cap"){
        return "<span class='black-text'>Market Cap: ";
    }
    else if (attribute == "revenue"){
        return "<span class='black-text'>Revenue: ";
    }
    else if (attribute == "bid"){
        return "<span class='black-text'>Bid: ";
    }
    else if (attribute == "offer"){
        return "<span class='black-text'>Offer: ";
    }
    else if (attribute == "sector"){
        return "<span class='black-text'>Sector: ";
    }
    else if (attribute == "sub_sector"){
        return "<span class='black-text'>Sub-Sector: ";
    }
    else if (attribute == "volume"){
        return "<span class='black-text'>Volume: ";
    }
    else if (attribute == "last_close_value"){
        return "<span class='black-text'>Last Close Value: ";
    }
    else if (attribute == "last_close_date"){
        return "<span class='black-text'>Last Close Date: ";
    }
    else if (attribute == "price"){
        return "<span class='black-text'>Price: ";
    }
    else{
        return "<span class='black-text'>";
    }
}

function getUnits(attribute){
    if (attribute == "per_diff"){
        return "%";
    }
    else if (attribute == "price"){
        return " GBX";
    }
    else{
        return "";
    }
}

$(document).ready(function() {
    $('.scrollable-container').hScroll();

    $('.tooltipped').tooltip({delay: 50});

    var voice;

    $.ajax({
        url: '/ajax/getvoice',
        success: function(result) {
            voice = result.voice;
        }
    });

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

    var fetchReply = function(query, history, voice) {
        return $.ajax({
            url: "/chat/",
            type: "POST",
            data: {
                question: query
            },
            success: function(data) {
                $("#buffering").remove();

                appendReply(false, voice, data);
                $('.scrollable-container').hScroll();
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
                    var queryBubble = "<div class='bubble sent blue lighten-1'><span class='white-text'></span></div>";
                    $("#chat-history").append(queryBubble);
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
                    processingQuery();
                    fetchReply(finalTranscript, voice);
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

        var now = new Date();
        var time = now.getHours() + ":" + now.getMinutes();

        var query = "<div class='bubble sent blue lighten-1 tooltipped'" +
                    "data-position='right' data-delay='50' data-tooltip='" + time + "'>" +
                    "<span class='white-text'>" + $('#id_question').val() + "</span></div>";

        $("#chat-history").append(query);
        $('.tooltipped').tooltip({delay: 50});
        $("html, body").animate({ scrollTop: $(document).height() }, "slow");

        processingQuery();
        fetchReply($('#id_question').val(), false, false);
        $("#id_question").val("");
    });
});

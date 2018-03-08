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

function appendReply(data, colour, history, voice) {
    if (voice) {
        var synth = window.speechSynthesis;
        var utterThis = new SpeechSynthesisUtterance(data['speech']);
        synth.speak(utterThis);
    }

    var reply = createReply(data, colour);

    $("#chat-history").append(reply);

    $(".suggestion-chip").on('click', function(e) {
        var suggestion = $($($(e.target)).contents()[0]).text();
        addQuery(suggestion, colour);
        processingQuery();
        fetchReply(suggestion, colour, false, voice);
    })

    if (!history) {
        $("html, body").animate({ scrollTop: $(document).height() }, "slow");
    }
}

function topPerformers(card) {
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

    return reply;
}

function members(card) {
    var reply = "<div class='bubble-interactive received'>" +
                  "<div class='card white'>" +
                    "<div class='card-content black-text'>" +
                      "<span class='card-title'>" + card["title"] + "</span>" +
                      "<table class='striped'><thead><tr><th>Name</th></tr></thead>" +
                      "<tbody>";

    card["companies"].forEach(function(obj) {
        reply += "<tr><td>" + obj.name + "</td></tr>";
    });

    reply += "</tbody></table></div></div></div>";

    return reply;
}

function createReply(data, colour) {
    var card = data["text"];
    var reply = '';

    switch(data["type"]) {
        case "company":
            reply +=  "<div class='bubble-interactive received'>" +
                          "<div class='card white'>" +
                            "<div class='card-content black-text'>" +
                              "<span class='card-title'>" + card["name"] + "</span>" +
                              "<p class='grey-text code-time'>" + card["code"] + "<br>" + card["date"] + "</p>" +
                              "<p class='price-impact'>" + getStyle(card['primary_type'], card['primary']) + card['primary'] + getUnits(card['primary_type']) +
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

            if(data['positive_negative'] != null)
                reply += simpleReply(data['positive_negative'], colour);
            break;
        case "top":
            reply += topPerformers(card);
            break;
        case "members":
            reply += members(card)
            break;
        case "risers&fallers":
            reply += topPerformers(card['risers']);
            reply += topPerformers(card['fallers']);
            break;
        case "comparison":
            reply += "<div class='bubble-interactive received'><section class='scrollable-container'>";

            card.forEach(function(obj) {
                reply += "<div class='company-comparison'>" +
                            "<div class='card white'>" +
                            "<div class='card-content black-text'>" +
                              "<span class='card-title'>" + obj["text"]["name"] + "</span>" +
                              "<p class='grey-text code-time'>" + obj["text"]["code"] + "<br>" + obj["text"]["date"] + "</p>" +
                              "<p class='price-impact'>" + getStyle(obj["text"]['primary_type'], obj["text"]['primary']) + obj["text"]['primary'] + getUnits(obj["text"]['primary_type']) +
                              "<br>" + getStyle(obj["text"]['secondary_type'], obj["text"]['secondary']) + obj["text"]['secondary'] + getUnits(obj["text"]['secondary_type']) + "</p>" +
                            "</div>" +
                            "</div>" +
                          "</div>"
            });

            reply += "</section></div>";

            break;
        case "revenue":
            reply += "<div class='bubble-interactive received'>" +
                          "<div class='card white'>" +
                            "<div class='card-content black-text'>" +
                              "<span class='card-title'>" + card["title"] + "</span>" +
                              "<table class='striped'><thead><tr><th>Date</th><th>Revenue (&poundm)</th>" +
                              "</tr></thead><tbody>";

            card["revenue_data"].forEach(function(obj) {
                reply += "<tr><td>" + obj.date + "</td><td>" + obj.revenue +"</td></tr>";
            });

            reply += "</tbody></table></div></div></div>";
            break;
        case "briefing":
            card['companies'].forEach(function(obj) {
                reply += simpleReply("Here is the latest data on " + obj.name + ":", colour);

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

                if ("news" in obj) {
                    reply += simpleReply("Here are the latest news on " + obj.name + ":", colour);

                    reply += createReply(obj.news, colour);
                }
            });

            card['sectors'].forEach(function(obj) {
                reply += simpleReply("The highest price in " + obj.name + " is:", colour);
                reply += createReply(obj.highest_price, colour);

                reply += simpleReply("The lowest price in " + obj.name + " is:", colour);
                reply += createReply(obj.lowest_price, colour);

                reply += simpleReply("The rising companies in " + obj.name + " are:", colour);
                reply += createReply(obj.rising, colour);

                reply += simpleReply("The falling companies in " + obj.name + " are:", colour);
                reply += createReply(obj.falling, colour);

                if ("news" in obj) {
                    reply += simpleReply("Here is some news about " + obj.name + ":", colour);
                    reply += createReply(obj.news, colour);
                }
            });

            break;
        default:
            var reply = simpleReply(data['text'], colour);
    }

    // Display suggestions
    if (data['suggestions'] != null) {
        var suggestions = data['suggestions']

        reply += '<div class="bubble-interactive received" id="suggestions">';

        for (i = 0; i < suggestions.length; i++) {
            reply +=
            '<div class="waves-effect suggestion-chip suggestion-chip-' + colour + ' z-depth-2">' +
              '<span><a class="grey-text text-darken-2" >' + suggestions[i] + '</a></span>' +
            '</div>';
        }

        reply += '</div">';
    }

    return reply;
}

function simpleReply(text, colour) {
    var reply = "<div class='bubble received ";

    if (colour == "indigo") {
        reply += "indigo lighten-1";
    } else if (colour == "dark") {
        reply += "grey darken-3";
    } else {
        reply += "grey lighten-3";
    }

    reply += "'><span class='";

    if (colour == "light") {
        reply += "black-text";
    } else {
        reply += "white-text";
    }

    reply += "'>" + text + "</span></div>";

    return reply;
}

function getQuery(text, colour) {
    var now = new Date();
    var time = now.getHours() + ":" + now.getMinutes();

    var query = "<div class='bubble sent ";

    if (colour == "indigo") {
        query += "indigo";
    } else if (colour == "dark") {
        query += "grey darken-4";
    } else {
        query += "grey lighten-2";
    }

    query += " tooltipped' data-position='right' data-delay='50' data-tooltip='" + time + "'><span class='";

    if (colour == "light") {
        query += "black-text";
    } else {
        query += "white-text";
    }

    query += "'>" + text + "</span></div>";

    return query;
}

function getImpact(value) {
    if (value.charAt(0) == "+"){
        return "<span class='green-text'><i class='material-icons valign-icon'>trending_up</i>";
    }
    else if (value.charAt(0) == "-"){
        return "<span class='red-text'><i class='material-icons valign-icon'>trending_down</i>";
    }
}

function addQuery(question, colour) {
    if ($('#suggestions').length) {
        $('#suggestions').remove();
    }

    var now = new Date();
    var time = now.getHours() + ":";

    if (now.getMinutes() < 10) {
        time += "0";
    }

    time += now.getMinutes();

    var query = getQuery(question, colour);

    $("#chat-history").append(query);
    $('.tooltipped').tooltip({delay: 50});
    $("html, body").animate({ scrollTop: $(document).height() }, "slow");
}

function getStyle(attribute, value){
    if (attribute == "per_diff" || attribute == "diff"){
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

var fetchReply = function(query, colour, history, voice) {
    return $.ajax({
        url: "/chat/",
        type: "POST",
        data: {
            question: query
        },
        success: function(data) {
            $("#buffering").remove();

            appendReply(data, colour, false, voice);
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

$(document).ready(function() {
    $('.scrollable-container').hScroll();

    $('.tooltipped').tooltip({delay: 50});

    var voice;
    var colour;

    $.ajax({
        url: '/ajax/getpreferences',
        success: function(result) {
            voice = result.voice;
            colour = result.colour_scheme;
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

    $("#send-text").click(function(e) {
        if ($("#id_question").val().trim() != "") {
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
                    addQuery('', colour);
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
                    fetchReply(finalTranscript, colour, false, voice);
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

        if ($("#id_question").val().trim() != "") {
            addQuery($('#id_question').val(), colour);
            processingQuery();
            fetchReply($('#id_question').val(), colour, false, false);
            $("#id_question").val("");
        }
    });
});

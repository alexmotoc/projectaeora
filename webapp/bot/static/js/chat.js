$(document).ready(function() {
    $('#ask-question').submit(function() {
        $.ajax({
            url: "chat/",
            type: "POST",
            data: {},
            success: function(data) {
                console.log("success");
            },
        });
    });
});

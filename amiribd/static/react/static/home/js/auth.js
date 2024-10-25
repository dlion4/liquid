$(document).ready(function () {
    $("#signin-form").submit(function (event) {
        event.preventDefault();
        var form = $(this);
        var formData = new FormData(form[0]); // Use form[0] to get the DOM element
        form.find("button[type=submit]").prop("disabled", true).text("Submitting...");
        $.ajax({
            url: form.attr("action"),
            type: "POST",
            data: formData,
            processData: false, // Prevent jQuery from automatically processing the data
            contentType: false,  // Let the browser set the content type
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                console.log(response);
                const {message} = response;
                $("#login-email-lookup-result").text("Login email send successful")
                $("#login-email-lookup-result").attr("class", "");
                $("#login-email-lookup-result").html(`${message}`).addClass("alert alert-success").css("padding","0.75rem 4rem");
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseJSON);
                $("#login-email-lookup-result").attr("class", "");
                $("#login-email-lookup-result").html(`${xhr.responseJSON.errors}`
                ).addClass("alert alert-danger").css("padding", "0.75rem 4rem")
            },
            complete: function () {
                form.find("button[type=submit]").prop("disabled", false).text("Log In"); 
                
            }
        });
    });

    $("#signup-form").submit(function(event){
        event.preventDefault();
        var form = $(this);
        var formData = new FormData(form[0]);
        form.find("button[type=submit]").prop("disabled", true).text("Submitting...");
        $.ajax({
            url: form.attr("action"),
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                console.log(response);
                const {url, message} = response;
                $("#signup-email-lookup-result").attr("class", "");
                $("#signup-email-lookup-result").html(`${message}`).addClass("alert alert-success").css("padding","0.75rem 4rem");

                setTimeout(() => {
                    window.location.href = url
                }, 3000);
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseJSON);
                $("#signup-email-lookup-result").attr("class", "");
                $("#signup-email-lookup-result").html(`${xhr.responseJSON.errors}`
                ).addClass("alert alert-danger").css("padding", "0.75rem 4rem")
            },
            complete: function(){
                form.find("button[type=submit]").prop("disabled", false).text("create account");
            }
        });
    })
});

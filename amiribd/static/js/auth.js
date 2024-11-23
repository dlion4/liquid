

$(document).ready(function () {
    $("form#loginForm").submit(function(event){
        event.preventDefault();
        const form = $(this)
        const fd = new FormData(this);
        const btn = form.find("button[type=submit]");
        btn.prop("disabled", true);
        btn.find("span#loginButton").addClass("d-none").removeClass("d-sm-inline");
        btn.find("div#spinner").addClass("d-flex").removeClass("d-none");
        const response = form.find("div#response");
        const url = "/users/login/"
        response.addClass("alert")

        $.ajax({
            type: "POST",
            data: fd,
            url: url,
            contentType: false,
            processData: false,
            success: function (data) {
                response.removeClass("alert-danger")
                response.addClass("alert-success").text(data.detail || "Authentication successful. Redirecting ...");
                setTimeout(function(){
                    window.location.href = data.url;
                }, 2000);

            },
            error: function(xhr, status, errorThrown){
                response.removeClass("alert-success")
                response.addClass("alert-danger").text(xhr.responseJSON.detail|| "Error authenticating the request");
            },
            complete: function(){
                btn.prop("disabled", false);
                btn.find("span#loginButton").removeClass("d-none").addClass("d-sm-inline");
                btn.find("div#spinner").removeClass("d-flex").addClass("d-none");
            }
        })

    });

    $("form#registerForm").submit(function(event){
        event.preventDefault();
        const form = $(this)
        const fd = new FormData(this);
        const btn = form.find("button[type=submit]");
        btn.prop("disabled", true);
        btn.find("span#registerButton").addClass("d-none").removeClass("d-sm-inline");
        btn.find("div#spinner").addClass("d-flex").removeClass("d-none");
        const response = form.find("div#response");
        const url = "/users/signup/"
        response.addClass("alert")

        $.ajax({
            type: "POST",
            data: fd,
            url: url,
            contentType: false,
            processData: false,
            success: function (data) {
                response.removeClass("alert-danger")
                response.addClass("alert-success").text(data.detail || "Registration successful. Redirecting ...");
                setTimeout(function(){
                    window.location.href = data.url;
                }, 2000);
            },
            error: function(xhr, status, errorThrown){
                const {url, detail} = xhr.responseJSON;
                if(url != undefined || null){
                    window.location.href = url;
                }
                response.removeClass("alert-danger").text(detail)
            },
            complete: function(){
                btn.prop("disabled", false);
                btn.find("span#registerButton").removeClass("d-none").addClass("d-sm-inline");
                btn.find("div#spinner").removeClass("d-flex").addClass("d-none");
            }
        });

    });


})


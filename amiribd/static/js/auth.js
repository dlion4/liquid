

$(document).ready(function () {
    function validateToken(data) {
        $.ajax({
            url: '/api/auth/validate-access-token',
            type: 'POST',
            headers: {
                'Authorization': `Bearer ${data.accessToken}`,
                'Content-Type': 'application/json',
            },
            success: function (response) {
                window.location.href = "/dashboard/"

                console.log("Token is valid:", response);
            },
            error: function (xhr) {
                console.error("Invalid token:", xhr.responseJSON);
            }
        });
    }

    window.addEventListener('message', (event) => {
        if (event.origin !== "https://auth.earnkraft.com") {
            return;
        }
        const data = event.data
        validateToken(data);
    });


    // Retrieve the authentication status from the hidden input
    const isUserAuthenticated = $("input[type=hidden][name=user]").val();

    // Retrieve the authentication URL from the hidden input
    const authenticationUrl = $("input[type=hidden][name=earnkraft_auth_url]").val();

    // Check if the user is not authenticated
    if (isUserAuthenticated ==="AnonymousUser") {
        // Redirect to the authentication URL
        window.location.href = authenticationUrl;
    }

    console.log("User authenticated:", isUserAuthenticated);
    console.log("Authentication URL:", authenticationUrl);



})


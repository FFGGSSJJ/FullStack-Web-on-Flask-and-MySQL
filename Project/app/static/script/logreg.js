$(document).ready(function () {
    // login button function
    $('#loginbtn').click(function () {
        console.log('login clicked');
        $.ajax({
            type: "POST",
            url: "/login",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({

            }),
            success: function (res) {
                console.log(res.response)
                location.href = '/homepage';
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    
});
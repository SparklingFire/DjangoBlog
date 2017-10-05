$(window).load(function () {
    $('.password-recovery-button').click(function (e) {
        let form = $(this).parent();
        e.preventDefault();
        $.ajax({type: 'POST',
                url: '/password_recovery/',
                data: form.serialize(),
                dataType: 'json',
                success: function (response) {
                    if ('errors' in response){
                        return errorCatcher(response.errors)
                    }
                }})
    })
});
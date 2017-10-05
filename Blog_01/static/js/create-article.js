$(document).ready(function () {
    $('.send-article').on('click', function (e) {
        let form = $('.create-article-form');
        $.ajax({method: 'POST',
                url: '/create_article/',
                data: form.serialize(),
                dataType: 'json',
                success: function (response) {
                    if (response.errors){
                        errorCatcher(response.errors)
                    }
                }
        })
    })
});

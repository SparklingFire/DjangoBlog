$(document).ready(function () {
    $(document).on('click', '.blacklist-user-popover', function (e) {
        e.preventDefault();
        let url = $(this).attr('href');
        let username = $(this).closest('.comment-message').find('.comment-author-username').data('id');
        $.ajax({type: 'GET',
                url: url,
                dataType: 'json',
                success: function (response) {
                    if (response.error){
                        return errorCatcher(response)
                    }
                    $('.comment-message').each(function (comment) {
                        if ($(this).find('.comment-author-username').data('id') == username){
                            if (response.block) {
                                $(this).replaceWith(blacklistUser($(this)));
                            }
                            else{
                                $(this).replaceWith(removeFromBlacklist($(this)));
                            }
                        }
                    })
        }
        })
    });
});

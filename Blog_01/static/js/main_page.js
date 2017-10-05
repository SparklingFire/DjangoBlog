function loadPage(url, pagefield_id, loadbutton_id) {
    let page = parseInt($(pagefield_id).val());
    $(loadbutton_id).prop("disabled", true);
    $(loadbutton_id).text("Загрузка ...");

    $.ajax({
        type: 'GET',
        url: url,
        data: {page: page + 1},
        error: function () {
            $(loadbutton_id).replaceWith('<p></p>');
        },
        success: function (response) {
            let article_list = $('#main-article-list');
            response.forEach(function (item) {
                let article_list_box = $('<div class="article-list-box" id="' + item.primary_key +'"></div>');
                let image_layer = $('<div class="image-layer"><img src="' + item.image_object + '"></div>');
                let title_layer = $('<div class="title-layer">' + item.title + '</div>');
                let info_layer = $('<div class="info-layer"></div>');
                let info_layer_hits = $('<div class="info-layer-hits">' +
                                        '<span class="glyphicon glyphicon-comment"></span>' + ' ' + item.comment_number  +
                                        ' <span class="glyphicon glyphicon-eye-open"></span>' + ' ' + item.hits +
                                        '</div>');
                let info_layer_created = $('<div class="info-layer-created">' + item.created + '</div>');
                let text_layer = $('<div class="text-layer">' + item.text + '</div>');
                info_layer.append(info_layer_created).append(info_layer_hits);
                let box = article_list_box.append(image_layer).append(title_layer).append(text_layer).append(info_layer);
                article_list.append(box);
            });

            if (article_list.children().length % 12 >= 1 && article_list.children().length <= 12){
                $(loadbutton_id).text('Показать больше');
                $(loadbutton_id).prop("disabled", false);
            }

            else{
                $(loadbutton_id).hide()
            }
        }
    });

}


$(window).load(function () {


    $('a[href="' + $(location).attr('pathname') + '"]').parent().attr('class', 'active');

    $(document).on('click', '.article-list-box', function () {
        let url = '/article/' + $(this).attr('id') + '/';
        return window.location.replace(url);
    });

    $("#load-id").click(function(){
    loadPage(
        "/",
        "#pagination-id",
        "#load-id",
        "#pagediv-id");});

    $(document).on('mouseenter', '.article-list-box', function () {
        $(this).css('cursor', 'pointer');
        $(this).find('.title-layer').css('color', '#cc181e');
    });

    $(document).on('mouseleave', '.article-list-box', function () {
        $(this).find('.title-layer').css('color', '#1a1a1a')
    });

    $('.recent-comment').click(function (e) {
        let url = $(this).attr('id');
        let message_id = $(this).find('.comment-info').attr('id');
        localStorage.setItem('message_id', message_id);
        window.location.replace(url);
    });
});

$(document).ready(function () {
  $(document).on('click', '.like', function (e) {
      let this_color = $(this).css('color');
      e.preventDefault();
      let url = $(this).find('a').attr('href');
      let likes = $(this).closest('.comment-message-footer').find('.total-likes');
      let dislikes = $(this).closest('.comment-message-footer').find('.total-dislikes');
      $.ajax({type: 'GET',
              url: url,
              dataType: 'json',
              success: function(response){
                  if (response.error){
                      return errorCatcher(response)
                  }
                  let glyph_1 = null;
                  let glyph_2 = null;
                  let color_1 = '';
                  let color_2 = '';

                  if (this_color != 'rgb(179, 179, 179)'){
                      color_1 = '#b3b3b3';
                      color_2 = '#b3b3b3';
                      glyph_1 = $('.glyphicon-thumbs-up');
                      glyph_2 = $('.glyphicon-thumbs-down');
                  }

                  else if (response.like == true){
                      glyph_1 = $('.glyphicon-thumbs-up');
                      glyph_2 = $('.glyphicon-thumbs-down');
                      color_2 = '#00af14';
                      color_1 = '#b3b3b3';

                  }
                  else {
                      glyph_1 = $('.glyphicon-thumbs-down');
                      glyph_2 = $('.glyphicon-thumbs-up');
                      color_1 = '#b3b3b3';
                      color_2 = '#cc181e';
                  }

                  likes.parent().find(glyph_2).css('color', color_1);
                  likes.parent().find(glyph_1).css('color', color_2);
                  likes.html(response.likes);
                  dislikes.html(response.dislikes);
              },
              error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);}
      });
  })
});

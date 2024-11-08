$(document).ready(function() {
    // Показать/скрыть блок авторов
    $("#but_addauthors").on('click', function() {
        $("#block_select_authors").removeClass("none").addClass("block_authors");
    });
    $("#close_authors").on('click', function() {
        $("#block_select_authors").addClass("none").removeClass("block_authors");
    });

    // Показать/скрыть блок жанров
    $("#but_addgenres").on('click', function() {
        $("#block_select_genres").removeClass("none").addClass("block_genres");
    });
    $("#close_genres").on('click', function() {
        $("#block_select_genres").addClass("none").removeClass("block_genres");
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const auth_url = $('#block_select_authors').data('url');
    const genre_url = $('#block_select_genres').data('url');

    $.ajax({
        url: auth_url,
        type: 'GET',
        success: function(data) {
            $('#but_authors').empty();
            data.forEach(function(author, index) {
                const bookHtml = `
                    <div class="author">
                        <input type="checkbox" id="chkbx_${index + 1}" class="author-checkbox">
                        <label for="chkbx_${index + 1}">${author.name}</label>
                    </div>
                `;
                $('#but_authors').append(bookHtml);
            });
        },
        error: function(xhr, status, error) {
            console.log('Ошибка:', error);
        }
        
    });

    $.ajax({
        url: genre_url,
        type: 'GET',
        success: function(data) {
            $('#but_genres').empty();
            data.forEach(function(genre, index) {
                const bookHtml = `
                    <div class="genre">
                        <input type="checkbox" id="chkbx_${index + 1}" class="genres-checkbox">
                        <label for="chkbx_${index + 1}">${genre.name}</label>
                    </div>
                `;
                $('#but_genres').append(bookHtml);
            });
        },
        error: function(xhr, status, error) {
            console.log('Ошибка:', error);
        }
        
    });
});

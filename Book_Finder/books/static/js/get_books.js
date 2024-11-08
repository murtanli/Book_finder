document.addEventListener("DOMContentLoaded", function() {
    const books_url = $('#book_spisok').data('url');

    $.ajax({
        url: books_url,
        type: 'GET',
        success: function(data) {
            //$('#book_spisok').empty();
            data.forEach(function(book, index) {
                const authorsHtml = Array.isArray(book.author_ob) ? book.author_ob.map(author => author).join(", ")  : "Автор не указан";
                const genresHtml = Array.isArray(book.genres) ? book.genres.map(genre => genre).join(", ") : "Жанр не указан";
                //alert(book.genres);
                const bookHtml = `
            <div class="book_info">
                <img src="/get_book_image/${book.image_url}/" alt="Обложка книги" class="book_cover">
                <div class="book_details">
                    <div class="age_limit">
                        <p>${book.age_limit} +</p>
                    </div>
                   
                    <div class="nam_rat">
                        <h2 class="book_title">${book.book_name}</h2>
                        <h2>${book.rating}</h2>
                       </div>
                    <button class="but_spoiler">Спойлер</button>
                    <div class="spoiler_block">
                        <p class="book_author">Автор: ${authorsHtml}</p>
                        <p class="book_genre">Жанр: ${genresHtml}</p>
                    </div>
                    <p class="book_description">${book.description}</p>
                    <div class="pages_block">
                        <p>${book.pages} страниц</p>
                    </div>
                </div>
            </div>
                `;
                $('#book_spisok').append(bookHtml);
            });
        },
        error: function(xhr, status, error) {
            console.log('Ошибка:', error);
        }
        
    });
    
});

$(document).on('click', '.up-arrow-button', function() {
    const getSelectedAuthors = () => {
        const selectedCheckboxes_au = document.querySelectorAll(".author-checkbox:checked");
        const selectedAuthors = Array.from(selectedCheckboxes_au).map(checkbox => checkbox.nextElementSibling.textContent.trim());
        
        console.log(selectedAuthors);
        return selectedAuthors;
    };

    const getSelectedGenres = () => {
        const selectedCheckboxes_ge = document.querySelectorAll(".genres-checkbox:checked");
        const selectedGenres = Array.from(selectedCheckboxes_ge).map(checkbox => checkbox.nextElementSibling.textContent.trim());

        console.log(selectedGenres);
        return selectedGenres;
    }

    const authors = getSelectedAuthors();
    const genres = getSelectedGenres();
    const text = document.querySelector("#input_text").value;
    const csrfToken = document.getElementById("csrf-token").dataset.token;
    
    $.ajax({
        type: 'POST',
        url: '/find_book/',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'authors': JSON.stringify(authors),
            'genres': JSON.stringify(genres),
            'text': text
        },
        success: function(data) {
            $('#book_spisok').empty();
            if (!data || data.length === 0) {
                let info = `
                <div class="not_found_block">
                    <p>Ничего не найдено по указанным фильтрам</p>
                </div>
                `
                $('#book_spisok').append(info);
                return;
            }
            data.forEach(function(book, index) {
                const authorsHtml = Array.isArray(book.author_ob) ? book.author_ob.map(author => author).join(", ")  : "Автор не указан";
                const genresHtml = Array.isArray(book.genres) ? book.genres.map(genre => genre).join(", ") : "Жанр не указан";
                const bookHtml = `
                    <div class="book_info">
                        <img src="/get_book_image/${book.image_url}/" alt="Обложка книги" class="book_cover">
                        <div class="book_details">
                            <div class="age_limit">
                                <p>${book.age_limit} +</p>
                            </div>

                            <div class="nam_rat">
                                <h2 class="book_title">${book.book_name}</h2>
                                <h2>${book.rating}</h2>
                               </div>
                            <button class="but_spoiler">Спойлер</button>
                            <div class="spoiler_block">
                                <p class="book_author">Автор: ${authorsHtml}</p>
                                <p class="book_genre">Жанр: ${genresHtml}</p>
                            </div>
                            <p class="book_description">${book.description}</p>
                            <div class="pages_block">
                                <p>${book.pages} страниц</p>
                            </div>
                        </div>
                    </div>
                `;
                $('#book_spisok').append(bookHtml);
            });
        },
        error: function(error) {
            console.error("Ошибка при отправке данных:", error);
        }
    });
    
});

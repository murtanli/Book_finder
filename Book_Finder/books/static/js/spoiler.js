$(document).on('click', '.but_spoiler', function() {
    $(this).next('.spoiler_block').toggleClass("active");
    $(this).toggleClass("deactive");
});
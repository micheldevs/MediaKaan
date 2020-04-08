// Contador de letras de la biografia
$(document).ready(function () {
    $('#id_bio').keyup(function () {
        $('.word-counter').text($.trim(this.value.length) + '/150');
    })
});
// Función de valoración con estrellas
function starRating(id, val) {

    var previous_value = $("#selected_rating_" + id).val();
    var selected_value = val;
    $("#selected_rating_" + id).val(selected_value);
    $("#selected-rating-" + id).empty();
    $("#selected-rating-" + id).html(selected_value);
    for (i = 1; i <= selected_value; ++i) {
        $("#rating-star-" + id + "-" + i).toggleClass('btn-warning');
        $("#rating-star-" + id + "-" + i).toggleClass('btn-default');
    }

    for (ix = 1; ix <= previous_value; ++ix) {
        $("#rating-star-" + id + "-" + ix).toggleClass('btn-warning');
        $("#rating-star-" + id + "-" + ix).toggleClass('btn-default');
    }
}
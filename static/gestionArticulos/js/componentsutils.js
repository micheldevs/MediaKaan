function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#output_fotoart').attr('src', e.target.result);
    }
    
    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

// Mostrador de preview de imagen de Media
$("#id_fotoart").change(function() {
  readURL(this);
});

// Contador de letras de la descripción de Media
$('#id_descripcion').keyup(function () {
    $('.word-counter').text($.trim(this.value.length) + '/240');
})

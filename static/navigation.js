function readURLFront(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap-front').hide();

      $('.file-upload-image-front').attr('src', e.target.result);
      $('.file-upload-content-front').show();

      $('.image-title-front').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } 
  else {
    removeUploadFront();
  }
}

function readURLLeft(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap-left').hide();

      $('.file-upload-image-left').attr('src', e.target.result);
      $('.file-upload-content-left').show();

      $('.image-title-left').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUploadLeft();
  }
}

function readURLRight(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap-right').hide();

      $('.file-upload-image-right').attr('src', e.target.result);
      $('.file-upload-content-right').show();

      $('.image-title-right').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUploadRight();
  }
}

function readURLBack(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap-back').hide();

      $('.file-upload-image-back').attr('src', e.target.result);
      $('.file-upload-content-back').show();

      $('.image-title-back').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUploadBack();
  }
}

function removeUploadFront() {
  $('.file-upload-input-front').replaceWith($('.file-upload-input-front').clone());
  $('.file-upload-content-front').hide();
  $('.image-upload-wrap-front').show();
}
$('.image-upload-wrap-front').bind('dragover', function () {
        $('.image-upload-wrap-front').addClass('image-dropping');
    });
    $('.image-upload-wrap-front').bind('dragleave', function () {
        $('.image-upload-wrap-front').removeClass('image-dropping');
});

function removeUploadLeft() {
  $('.file-upload-input-left').replaceWith($('.file-upload-input-left').clone());
  $('.file-upload-content-left').hide();
  $('.image-upload-wrap-left').show();
}
$('.image-upload-wrap-left').bind('dragover', function () {
        $('.image-upload-wrap-left').addClass('image-dropping');
    });
    $('.image-upload-wrap-left').bind('dragleave', function () {
        $('.image-upload-wrap-left').removeClass('image-dropping');
});

function removeUploadBack() {
  $('.file-upload-input-back').replaceWith($('.file-upload-input-back').clone());
  $('.file-upload-content-back').hide();
  $('.image-upload-wrap-back').show();
}
$('.image-upload-wrap-back').bind('dragover', function () {
        $('.image-upload-wrap-back').addClass('image-dropping');
    });
    $('.image-upload-wrap-back').bind('dragleave', function () {
        $('.image-upload-wrap-back').removeClass('image-dropping');
});

function removeUploadRight() {
  $('.file-upload-input-right').replaceWith($('.file-upload-input-right').clone());
  $('.file-upload-content-right').hide();
  $('.image-upload-wrap-right').show();
}
$('.image-upload-wrap-right').bind('dragover', function () {
        $('.image-upload-wrap-right').addClass('image-dropping');
    });
    $('.image-upload-wrap-right').bind('dragleave', function () {
        $('.image-upload-wrap-right').removeClass('image-dropping');
});
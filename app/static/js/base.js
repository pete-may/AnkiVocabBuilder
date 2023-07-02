function playSound() {
    console.log("INSIDE playSound");

    var filename = document.getElementById("recording").value
    var filepath = "/tmp/recordings/" + filename

    console.log(filepath);

    const audio = new Audio(filepath);
    audio.play();
}

function loadMoreImages() {
    console.log("loading more images...")
    query = $("#search_query").val()
    loading_button = $("#loader").html()
    $("#loader").html("<img src=/static/loading.gif>")
    $.getJSON('/get_more_images', { query: query, offset: offset}, function(data) {
        console.log(data)
        new_divs = ""

        for (var file_name of data) {
            new_divs += '<div class="gallery-item-wrapper col-md-4">'
            new_divs += '<div class="gallery-item">'
            new_divs += '<img class="img-responsive" src="/static/tmp/images/' + file_name + '">'
            new_divs += '</div>'
            new_divs += '</div>'
        }

        $("#images_row").html(new_divs)
        $("#loader").html(loading_button)
    }).fail(function() {
    $("#loader").html(loading_button)
        alert("error");
    });
    offset = offset + 1
    console.log(offset)
    return false;
}

function imgSelectWatch() {
    $("body").on("click", ".gallery div.gallery-item-wrapper", function () {
        $(this).children("div.gallery-item").addClass("img-selected");
        $(this).detach().appendTo(".gallery-selected");
    }).on("click", ".gallery-selected div.gallery-item-wrapper", function () {
        $(this).children("div.gallery-item").removeClass("img-selected");
        $(this).detach().appendTo("#images_row");
    });
}

function submitWatch() {
    $("body").on("click", "#create_submit", function () {
        const selectedImages = $.map($(".img-selected"), function (el) {
            src = $(el).children("img").attr("src");
            return src.substring(src.lastIndexOf('/') + 1);
        });
        console.log(selectedImages)
        var field = document.getElementById("images");
        field.value = selectedImages;
    });
}

function imageSearchSubmitWatch() {
    $("#image_search").on("submit", function (e) {
        e.preventDefault();

        query = $("#image_query").val()

        var field = document.getElementById("search_query");
        field.value = query

        offset = 0
        loadMoreImages()
    });
}

$(document).ready(function () {
    imgSelectWatch();
    submitWatch();
    imageSearchSubmitWatch();
});

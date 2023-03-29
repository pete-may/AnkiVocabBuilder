
function imgSelectWatch() {
    $("body").on("click", ".gallery div.gallery-item-wrapper", function () {
        $(this).children("div.gallery-item").addClass("img-selected");
        $(this).detach().appendTo(".gallery-selected");
    })
        .on("click", ".gallery-selected div.gallery-item-wrapper", function () {
            $(this).children("div.gallery-item").removeClass("img-selected");
            $(this).detach().appendTo("#images_row");
        });
}

function handleTabClick(tab_type) {
    var str = ""
    if (tab_type == "local") {
        if ($("#local_file").html()) {
            return
        }

        recording_select = $("#forvo_file").html();
        $("#forvo_file").html("");
        $("#local_file").html(recording_select);
        
        for (var file_name of local_recordings) {
            str += "<option>" + file_name + "</option>"
        }
        $("#recording").html(str)

        var field = document.getElementById("recording_type");
        field.value = 'local';
    }
    else if (tab_type == "forvo") {
        if ($("#forvo_file").html()) {
            return
        }

        recording_select = $("#local_file").html();
        $("#local_file").html("");
        $("#forvo_file").html(recording_select);
        

        for (var file_name of forvo_recordings) {
            str += "<option>" + file_name + "</option>"
        }
        $("#recording").html(str)

        var field = document.getElementById("recording_type");
        field.value = 'forvo';
    }
}

function playSound(tab_type) {

    console.log("INSIDE playSound");

    var filename = document.getElementById("recording").value

    var filepath = ""
    if (tab_type == "local") {
        filepath = "/recordings/" + filename
    }
    else if (tab_type == "forvo") {
        filepath = "/tmp/recordings/" + filename
    }

    console.log(filepath);

    const audio = new Audio(filepath);
    audio.play();
}

function loadMoreImages(refresh_images) {
    console.log("loading more images...")
    query = $("#search_query").val() 
    load_more_button = $("#loader").html()
    $("#loader").html("<img src=/static/loading.gif>")
    $.getJSON('/get_more_images', { query: query, offset: offset, refresh_images: refresh_images}, function(data) {
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
            $("#loader").html(load_more_button)
        })

        .fail(function() { 
            $("#loader").html(load_more_button)
            alert("error"); 
        });
    offset = offset + 1
    console.log(offset)
    return false;
}


function submitWatch() {
    console.log("blub")
    $("body").on("click", "#create_submit", function () {
        console.log("BLUB")

        const selectedImages = $.map($(".img-selected"), function (el) {
            console.log("yo");
            src = $(el).children("img").attr("src");
            return src.substring(src.lastIndexOf('/') + 1);
        });
        console.log(selectedImages)
        var field = document.getElementById("images");
        field.value = selectedImages;
    });
}


function imageSearchSubmitWatch() {
    console.log("blurb")
    $("#image_search").on("submit", function (e) {
        console.log("BLURB")

        e.preventDefault();

        query = $("#image_query").val() 

        var field = document.getElementById("search_query");
        field.value = query

        offset = 0 
        loadMoreImages(true)
    });
}

// function enterWatch() {
//     $("body").on("keypress", "input#word", function (e) {
//         if (e.which === 13) {
//             e.preventDefault();
//             search();
//         }
//     })
//         .on("keypress", "input#image_query", function (e) {
//             if (e.which === 13) {
//                 e.preventDefault();
//                 searchImages(null, null, true);
//             }
//         });
// }


$(document).ready(function () {
    imgSelectWatch();
    submitWatch();
    imageSearchSubmitWatch();
});
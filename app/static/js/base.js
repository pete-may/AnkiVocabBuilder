
function imgSelectWatch() {
    var selectedImages = [];
    $("body").on("click", ".gallery div.gallery-item-wrapper", function () {
        $(this).children("div.gallery-item").addClass("img-selected");
        selectedImages.push(this.src);
        $(this).detach().appendTo(".gallery-selected");
    })
        .on("click", ".gallery-selected div.gallery-item-wrapper", function () {
            $(this).children("div.gallery-item").removeClass("img-selected");
            selectedImages.pop(this.src);
            $(this).detach().appendTo(".gallery");
        });
}

function submitWatch() {
    console.log("blub")
    $("body").on("click", "#create_submit", function () {
        console.log("BLUB")

        const selectedImages = $.map($(".img-selected"), function (el) {
            console.log("yo")
            return $(el).children("img").attr("src");
        });
        console.log(selectedImages)
        var field = document.getElementById("images");
        field.value = selectedImages;
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


$(document).ready(function () {
    imgSelectWatch();
    submitWatch();
});
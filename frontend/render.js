document.getElementById('displaytext').style.display = 'none';

function searchPhoto() {

    var imgContainer = document.getElementById('image-container');
    imgContainer.innerHTML = '';
    var apigClient = apigClientFactory.newClient();
    var user_message = document.getElementById('note-textarea').value;

    var body = {};
    var params = { q: user_message };
    var additionalParams = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    apigClient
        .searchGet(params, body, additionalParams)
        .then(function (res) {
            var resp_data = res.data;
            // Check if no images were found
            if (!resp_data.results || resp_data.results.length === 0) {
                document.getElementById('displaytext').innerHTML =
                    'Sorry could not find any images. Try another search term!';
                document.getElementById('displaytext').style.display = 'block';
                return;
            }

            // Display a message
            document.getElementById('displaytext').innerHTML =
                'Images returned for query as specified by the user';

            // Loop through the results and display images
            const imageContainer = document.getElementById('image-container');
            resp_data.results.forEach(function (imgObj) {
                var img = new Image();
                img.src = imgObj.url;
                img.classList.add('banner-img');
                img.setAttribute('alt', imgObj.labels[0]); // Set alt text using the label
                imageContainer.appendChild(img);
            });

            document.getElementById('displaytext').style.display = 'block';
        })
        .catch(function (result) {
            // Handle errors
        });
}

function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        // reader.onload = () => resolve(reader.result)
        reader.onload = () => {
            let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
            if (encoded.length % 4 > 0) {
                encoded += '='.repeat(4 - (encoded.length % 4));
            }
            resolve(encoded);
        };
        reader.onerror = (error) => reject(error);
    });
}

function uploadPhoto() {
    // var file = document.getElementById('file_path').files[0];
    const reader = new FileReader();
    document.getElementById('upload_button').innerHTML = 'Uploading...';
    document.getElementById('upload_button').style.backgroundColor = '#005af0';
    var encoded_image = getBase64(file).then((data) => {
        var apigClient = apigClientFactory.newClient();

        var file_type = file.type + ';base64';
        var body = data;
        var params = {
            'bucket': 's3-photos-store',
            "object": file.name,
            'x-amz-meta-customLabels': note_customtag.value,
        };
        var additionalParams = {};
        apigClient
            .uploadBucketObjectPut(params, body, additionalParams)
            .then(function (res) {
                if (res.status == 200) {
                    document.getElementById('upload_button').innerHTML = 'Upload succeeded';
                    document.getElementById('upload_button').style.backgroundColor = '#499C55';

                }
            }).catch(() => {
                document.getElementById('upload_button').innerHTML = 'Upload failed';
                document.getElementById('upload_button').style.backgroundColor = '#F54234';
            }
        );
    });
}

const dropArea = document.querySelector(".drop_box"),
    button = dropArea.querySelector("button"),
    dragText = dropArea.querySelector("header"),
    input = dropArea.querySelector("input");
let file;
var filename;

button.onclick = () => {
    input.click();
};

input.addEventListener("change", function (e) {
    var fileName = e.target.files[0].name;
    let filedata = `
    <h4>${fileName}</h4>
    <input placeholder="Input Custom tag!" type="text" class="form-control" id="note_customtag">
    <button class="btn" id="upload_button" type="submit" onclick="uploadPhoto()">Upload</button>
    `;
    file = document.getElementById('file_path').files[0];
    dropArea.innerHTML = filedata;
});


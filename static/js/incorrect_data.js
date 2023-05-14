fetch('static/json/error_timetable.json')
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                appendData(data);
            })
            .catch(function (err) {
                console.log('error: ' + err);
            });
        function appendData(data) {
            var mainContainer = document.getElementById("incorrect_data");
            for (var i = 0; i < data["teacher"].length; i++){
            var div = document.createElement("div");
                div.innerHTML = data["teacher"][i];
                mainContainer.appendChild(div);
            }
            for (var i = 0; i < data["student"].length; i++){
            var div = document.createElement("div");
                div.innerHTML = data["student"][i];
                mainContainer.appendChild(div);
            }
        }
fetch('static/json/error.json')
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
            for (var i = 0; i < data.length; i++) {
                for(var j = 0; j < data[i].length; j++){
                var div = document.createElement("div");
                div.innerHTML = data[i][j];
                mainContainer.appendChild(div);
            }
        }
       }
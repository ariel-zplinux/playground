
function xml_http_post(url, data, callback) {
    var req = false;
    try {
        // Firefox, Opera 8.0+, Safari
        req = new XMLHttpRequest();
    }
    catch (e) {
        // Internet Explorer
        try {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }
    }
    req.open("POST", url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            callback(req);
        }
    }
    req.send(data);
}

function change_period() {
    var data = document.form_period.period.value;  
    // I write data like this to be able to easily use same python function
    // that I was using for non-ajax version
    data = "index.html?period="+data+"&per_page=20";
    //alert(data);         
    xml_http_post("index.html", data, test_handle)
}

function test_handle(req) {
    var elem = document.getElementById('table_result')
    elem.innerHTML =  req.responseText
}

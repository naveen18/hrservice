
	var host = "http://127.0.0.1:5000"
// index.html funtions######################################################################
	function login() {
		url = host + "/userservice/api/v1.0/user/login";
		var data = {};
		data.email = $("#username").val()
		data.password  = $("#password").val()
		if (!validateParamsForLogin()) return;
		var json = JSON.stringify(data);
		var xhr = new XMLHttpRequest();
		xhr.open("PUT", url, true);
		xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
		xhr.onload = function () {
			var users = JSON.parse(xhr.responseText);
			if (xhr.readyState == 4 && xhr.status == "200") {
	            // document.cookie = document.cookie + ";path=/";
	            console.log("login successfull");
	            setTimeout(routeCall(), 3000);
	            window.location = host + "/home";
	        } else {
	        	console.log("login failed");
	        	alert("Invalid username or password. Please login again");
	        	$("#username").val("")
	        	$("#password").val("")
	        }
		}
	    xhr.send(json);
	}

	function routeCall() {
		window.location = host + "/home";
	}

	function validateParamsForLogin(){
    	email = $("#username").val()
    	password  = $("#password").val()
    	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    	if (!re.test(email)) {
    		$(".error-messages").text("*email is invalid").fadeIn();
    		return false;
    	}
    	if (password.length < 5) {
    		$(".error-messages").text("*password should be atleast five digit long").fadeIn();
    		return false;
    	}
    	return true;
	}

    function captureEnter(event) {
    	if (event.keyCode == 13) {
    		login();
    		return false;
    	}
    	$(".error-messages").empty().fadeOut();
    	return true;
    };



// home.html funtions.######################################################################

	function getVisualizations() {
	    checkSession();
	    sessionid = getCookie("sessionid");
	    url = host + "/userservice/api/v1.0/visualizations/" + encodeURIComponent(sessionid);
	    var xhr = new XMLHttpRequest();
	    xhr.open("GET", url, true);
	    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
	    xhr.onload = function () {
	        if (xhr.readyState == 4 && xhr.status == "200") {
	            var result = JSON.parse(xhr.responseText);
	            console.log("getting getting visualizations");
	            console.log(result);
	            if (result["success"] == true) {
	                // parese images and display
	                console.log(result["images"]);
	                renderImages(result["images"]);
	            }
	            else {
	                console.log("exiting from here");
	                // alert("Your session expired please login again");
	                window.location = host;
	            }
	        }
	    }
	    xhr.send();
	}

    function checkSession() {
        console.log("in index");
        sessionid = getCookie("sessionid");
        userid = getCookie("userid");
        console.log("user id is" + userid);
        console.log("sessionid id is" + sessionid);
        if (sessionid === null || userid === null) {
            console.log("invalid session");
            // alert("Your session expired please login again");
            window.location = host;
            return;
        }
        url = host + "/userservice/api/v1.0/session/" + encodeURIComponent(sessionid);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
        xhr.onload = function () {
            if (xhr.readyState == 4 && xhr.status == "200") {
                var result = JSON.parse(xhr.responseText);
                if (result["session_valid"] == true) {
                    console.log("session is valid");
                    //return true;
                }
                else {
                    console.log("invalid session");
                    // alert("Your session expired please login again");
                    window.location = host;
                }
            }
        }
        xhr.send();
    }

    function openInNewTab(url) {
        var win = window.open(url, '_blank');
        win.focus();
    }

    function getCookie(name) {
        if (document.cookie == 0) return null;
        var cookieItems = document.cookie.split(";");
        var dictionary = {};
        for (i = 0; i < cookieItems.length; i++) {
            cookieItems[i] = cookieItems[i].split("=");
            dictionary[cookieItems[i][0].trim()] = cookieItems[i][1].trim();
        }
        if (!(name in dictionary)) {
            return null;
        }
        return dictionary[name];
    }

    function logout() {
        checkSession();
        sessionid = getCookie("sessionid");
        userid = getCookie("userid");
        var xhr = new XMLHttpRequest();
        url = host + "/userservice/api/v1.0/user/logout"
        xhr.open("PUT", url, true);
        xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
        xhr.setRequestHeader('sessionid',sessionid);
        xhr.setRequestHeader('userid',userid);
        xhr.onload = function () {
            if (xhr.readyState == 4 && xhr.status == "200") {
                var resp = JSON.parse(xhr.responseText);
                console.log(resp)
                console.log("logging out");
                window.location = host;
            } else {
                console.log("logout failed, try again");
            }
        }
        xhr.send();
    }

    function deleteCookie(name) {
        document.cookie = name + '=;expires=Thu, 05 Oct 1990 00:00:01 GMT;';
    }

    function renderImages(images) {
        console.log(images);
        heights = [250, 250, 250, 300, 400, 400, 400];
        widths = [500, 600, 500, 500, 500, 500, 500];
        $("#about").empty().fadeOut();
        $("#dp").empty().fadeOut();
        $("#vis").empty().fadeIn();
        for (i = 0; i < images.length; i++) {
            $("#vis").append("<img src=" + "../" + images[i] + " height=\"" + heights[i] + "\"" + " width=\"" + widths[i] + "\" id=\"myimg\">");
        }
    }

    function getUserData() {
        sessionid = getCookie("sessionid");
        userid = getCookie("userid");
        checkSession();
        url = host + "/userservice/api/v1.0/user";
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url, true);
        xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
        xhr.setRequestHeader('sessionid',sessionid);
        xhr.setRequestHeader('userid',userid);
        xhr.onload = function () {
            if (xhr.readyState == 4 && xhr.status == "200") {
                var resp = JSON.parse(xhr.responseText);
                showUserDetails(resp["data"]);
                console.log(resp);
            } else {
                alert("Your session expired please login again")
                window.location = host;
                return;
            }
        }
        xhr.send();
    }

    function showUserDetails(data){
        console.log("came for rendering user details");
        url = "https://kooledge.com/assets/default_medium_avatar-57d58da4fc778fbd688dcbc4cbc47e14ac79839a9801187e42a796cbd6569847.png";
        var htm = $("<img src=" + "\"" + url + "\"" + "height=\"150\" width=\"150\" id = \"avatar\">");
        var tbl = $("<table/>").attr("id", "mytable");
        var tr1 = "<tr id = \"mytr\"><td id = \"mytd\">" + "Firstname" + "</td>" + "<td id = \"mytd\">" + data["firstname"] + "</td></tr>";
        var tr2 = "<tr id = \"mytr\"><td id = \"mytd\">" + "Lastname" + "</td>" + "<td id = \"mytd\">" + data["lastname"] + "</td></tr>";
        var tr3 = "<tr id = \"mytr\"><td id = \"mytd\">" + "Email" + "</td>" + "<td id = \"mytd\">" + data["email"] + "</td></tr>";
        tbl.append(tr1);
        tbl.append(tr2);
        tbl.append(tr3);
        $("#vis").empty().fadeOut();
        $("#about").empty().fadeIn();
        $("#dp").empty().fadeIn();

        $("#dp").append(htm)
        $("#about").html(tbl);
    }


// predict.html functions##################################################################################

	function getLabel() {
		checkSession();
		sessionid = getCookie("sessionid");
		url = host + "/userservice/api/v1.0/predict/" + sessionid + "?";
		data = {};
		data["satisfaction_level"] = parseInt($("#sl").val(), 10);
		data["last_evaluation"] = parseInt($("#le").val(), 10);
		data["number_project"] = parseInt($("#nop").val(), 10);
		data["average_montly_hours"] = parseInt($("#amh").val(), 10);
		data["time_spend_company"] = parseInt($("#tsp").val(), 10);
		data["Work_accident"] = parseInt($("#wa").val(), 10);
		data["promotion_last_5years"] = parseInt($("#pc").val(), 10);
		data["sales"] = $("#dept").val();
		data["salary"] = $("#salary").val();
		console.log(data);
		if (!validateParamsForPredict(data)) return;
        // normalize satisfaction and evaluation to get in 0 to 1 range
        data["satisfaction_level"] = data["satisfaction_level"]/100;
        data["last_evaluation"] = data["last_evaluation"]/100;
        console.log(data);
		params = encodeQueryData(data);
		console.log(url + params)
		url = url + params;
		var xhr = new XMLHttpRequest();
		xhr.open("GET", url, true);
		xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
		xhr.onload = function () {
			if (xhr.readyState == 4 && xhr.status == "200") {
				var result = JSON.parse(xhr.responseText);
				if (result["success"] == true) {
					if (result["left"] == "1") {
						alert("employee is likely to leave");
						// $("#emp-label").text("Employee is not likely to leave").fadeIn()
					}
					else{
						alert("employee is not likely to leave");
						// $("#emp-label").text("Employee is not likely to leave").fadeIn()
					}
                }
                else {
					$("#error-messages").text("Could not reach the prediction api").fadeIn();
                }
            }
        }
        xhr.send();
    }


    function encodeQueryData(data) {
    	let ret = [];
    	for (let d in data)
    		ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    	return ret.join('&');
    }

    function validateParamsForPredict(data){
            $("#error-messages").text("").fadeOut();
            console.log("came to validate params for prediction form");
            numbers_key = ["satisfaction_level", "last_evaluation", "number_project", "average_montly_hours", "time_spend_company", "promotion_last_5years"];
            for(var key in numbers_key){
                if (isNaN(data[numbers_key[key]])) {
                    // console.log(key, numbers_key[key], data[numbers_key[key]]);
                    $("#error-messages").text("*" + numbers_key[key] + " feild should be a number").fadeIn();
                    return false;
                }
            }
            if (data["satisfaction_level"] < 0 || data["satisfaction_level"] > 100) {
                console.log("satisfaction_level is not valid")
                $("#error-messages").text("*Satisfaction level should be between 0 to 100").fadeIn();
                return false;
            }
            if (data["last_evaluation"] < 0 || data["last_evaluation"] > 100) {
                $("#error-messages").text("*Last evaluation should be between 0 to 100").fadeIn();
                return false;
            }
            if (data["number_project"] < 0) {
                $("#error-messages").text("*Number of projects can not be negitive").fadeIn();
                return false;
            }
            if (data["average_montly_hours"] < 0) {
                $("#error-messages").text("*Average montly hours can not be negitive").fadeIn();
                return false;
            }

            if (data["time_spend_company"] < 0) {
                $("#error-messages").text("*Time spend in company can not be negitive").fadeIn();
                return false;
            }
            if (data["Work_accident"] != 0 && data["Work_accident"] != 1) {
                $("#error-messages").text("*Work accident should be either Yes or No").fadeIn();
                return false;
            }

            if (data["promotion_last_5years"] < 0) {
                $("#error-messages").text("*promotion_last_5 years should be greater than 0").fadeIn();
                return false;
            }

            return true;
    }

// signup.html functions##################################################################################

    function signup() {
        url = host + "/userservice/api/v1.0/user"
        var data = {};
        data.email = $("#username").val()
        data.password  = $("#password").val()
        data.firstname = $("#firstname").val()
        data.lastname = $("#lastname").val()
        if (!validateParamsForSignup()) return;
        var json = JSON.stringify(data);
        var xhr = new XMLHttpRequest();
        xhr.open("PUT", url, true);
        xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
        xhr.onload = function () {
            var users = JSON.parse(xhr.responseText);
            if (xhr.readyState == 4 && xhr.status == "200") {
                console.log("signup successfull");
                alert("signup successfull, redirecting to login page");
                window.location = host;
            } else {
                console.log("signup failed");
                alert("signup failed, please try after sometime");
                $("#username").val("")
                $("#password").val("")
                $("#firstname").val("")
                $("#lastname").val("")
            }
        }
        xhr.send(json);
    }

    function validateParamsForSignup(){
        email = $("#username").val()
        password  = $("#password").val()
        firstname = $("#firstname").val()
        lastname = $("#lastname").val()

        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (firstname.length == 0) {
            $(".error-messages").text("*firstname can't be empty").fadeIn();
            return false;
        }
        if (lastname.length == 0) {
            $(".error-messages").text("*lastname can't be empty").fadeIn();
            return false;
        }
        if (!re.test(email)) {
            $(".error-messages").text("*email is invalid").fadeIn();
            return false;
        }
        if (password.length < 5) {
            $(".error-messages").text("*password should have atleast five characters").fadeIn();
            return false;
        }
         $(".error-messages").empty().fadeOut();
        return true;
    }

    function routeToSignupPage() {
        window.location = host + "/signup";
    }





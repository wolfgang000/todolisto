
if (window.location.hostname == 'localhost') {
	var Config = {
		firebase : {
			apiKey: "AIzaSyC3HlGlSkot2CJyH4DuLpdLcnfoddp4gCU",
			authDomain: "testupload-140219.firebaseapp.com",
			databaseURL: "https://testupload-140219.firebaseio.com",
			storageBucket: "localhost:8080"
		},
		backendHostUrl : 'https://localhost:8080'
	};
} else {
	var Config = {
		firebase : {
			apiKey: "",
			authDomain: "",
			databaseURL: "",
			storageBucket: ""
		},
		backendHostUrl : ''
	};
}

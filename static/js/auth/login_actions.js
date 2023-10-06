console.clear();

const loginBtn = document.getElementById('login');
const signupBtn = document.getElementById('signup');

loginBtn.addEventListener('click', (e) => {
	let parent = e.target.parentNode.parentNode;
	Array.from(e.target.parentNode.parentNode.classList).find((element) => {
		if(element !== "slide-up") {
			parent.classList.add('slide-up')
		}else{
			signupBtn.parentNode.classList.add('slide-up')
			parent.classList.remove('slide-up')
		}
	});
});

signupBtn.addEventListener('click', (e) => {
	let parent = e.target.parentNode;
	Array.from(e.target.parentNode.classList).find((element) => {
		if(element !== "slide-up") {
			parent.classList.add('slide-up')
		}else{
			loginBtn.parentNode.parentNode.classList.add('slide-up')
			parent.classList.remove('slide-up')
		}
	});
});


// document.querySelector(".submit-signup-btn").addEventListener("click", function(e) {
//     e.preventDefault();

//     var email = document.querySelector('input[name="email"]').value;
//     var password1 = document.querySelector('input[name="password1"]').value;
//     var password2 = document.querySelector('input[name="password2"]').value;

//     var errorDiv = document.getElementById("signup-error-messages");
//     var errorMessage = "";

//     // Check if email exists using AJAX
//     fetch('/check_email/?email=' + email)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error("Network response was not ok");
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data.exists) {
//                 errorMessage = "Email already exists.";
//                 errorDiv.style.display = "block";
//                 errorDiv.innerHTML = errorMessage;
//             } else if (password1 !== password2) {
//                 errorMessage = "Passwords do not match.";
//                 errorDiv.style.display = "block";
//                 errorDiv.innerHTML = errorMessage;
//             } else {
//                 errorDiv.style.display = "none";
//                 document.querySelector(".signup form").submit();
//             }
//         })
//         .catch(error => {
//             console.error("There was a problem with the fetch operation:", error.message);
//         });
// });



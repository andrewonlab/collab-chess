var myNum;
window.onload = function() {
	setMyNum(14);
	startCountDown(1000);
}

function getMyNum(){
return myNum;
}

function setMyNum(k){
myNum = k+1;
}

function startCountDown(p) {
	var pause = p;
	var countDownObj = document.getElementById("countDown");
	countDownObj.style.fontSize = "150px";
	if (countDownObj == null) {
		return;
	}
	counter = getMyNum();
	countDownObj.count = function(counter) {
		if (counter <= 5){
			countDownObj.style.color = "Red";
		}
		else{
			countDownObj.style.color = "Black";
		}
		if (counter < 0){
			counter = 0;
			pause = 10;
		}
		else{
			pause = 1000;
		}
		countDownObj.innerHTML = counter;
		setTimeout(function() {
			counter = getMyNum();
			setMyNum(counter - 2);
			countDownObj.count(counter - 1);	
		},
		pause
		);
	}
	countDownObj.count(counter);
}

/*
1. 컴퓨터의 랜덤 수로 정답 만들기
2. 사용자가 입력한 숫자를 제출하기
3. up&down&정답 여부 판단하여 출력하기
4. 시도 횟수 카운트하기
 */
let target_Number = Math.ceil(Math.random() * 100);
console.log(target_Number);
let attempts = 0;

document
  .querySelector("#userInput")
  .addEventListener("keypress", function (event) {
    if (event.key == "Enter") {
      guessNumber();
    }
  });

function guessNumber() {
  attempts++;
  //1. textbox의 값을 가져옵니다. id는 고유값이니까 1개 밖에 없음 #userinput
  let userNumber = document.querySelector("#userInput").value;
  console.log(userNumber);
  let Message = "";

  //2. textbox의 값과 컴퓨터의 랜덤수를 비교합니다. up&down&정답 여부 판단
  if (userNumber == target_Number) {
    Message = `정답입니다, ${attempts}번 시도했습니다`;
  } else if (userNumber > target_Number) {
    Message = "Down";
  } else if (userNumber < target_Number) {
    Message = "Up";
  }

  document.querySelector("#result").innerText = Message;
}

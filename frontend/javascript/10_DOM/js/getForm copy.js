let btnSend = document.querySelector("#send");
btnSend.onclick = () => {
  let userName = document.querySelector("#userName").value;
  let major = document.querySelector("#major").selectedIndex;
  let subject = document.testForm.subject.value;
  let mailing = document.querySelectorAll(
    "input[name='mailing']:checked"
  ).length;
  //   console.log(userName);
  //   console.log(major);
  //   console.log(subject);
  //   console.log(mailing);
  if (userName === "") {
    alert("이름을 입력하세요");
  } else if (major === 0) {
    alert("학과를 선택하세요");
  } else if (subject === "") {
    alert("신청 과목을 선택하세요");
  } else if (mailing === 0) {
    alert("메일링을 한개 이상 선택하세요.");
  }
};

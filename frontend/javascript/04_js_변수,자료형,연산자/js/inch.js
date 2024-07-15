let inch = parseFloat(prompt("인치(inch)를 입력하세요"));
let cm = inch / 2.54;
cm = cm.toFixed(1);
let msg = `<span class="red">${inch}inch</span>는 `;
msg += `<span class="red">${cm}cm</span> 입니다.<br>`;
document.write(msg);

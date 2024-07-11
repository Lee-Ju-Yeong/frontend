document
  .getElementById("initial-capital")
  .addEventListener("input", function (e) {
    var value = e.target.value.replace(/,/g, "").replace(/원/g, "");
    if (!isNaN(value) && value !== "") {
      e.target.value = parseInt(value).toLocaleString("ko-KR") + " 원";
    }
  });

document
  .getElementById("backtest-form")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    runBacktest();
  });

function runBacktest() {
  const initialCapital = parseInt(
    document
      .getElementById("initial-capital")
      .value.replace(/,/g, "")
      .replace(/원/g, "")
  );
  const numSplits = parseInt(document.getElementById("num-splits").value);
  const investmentRatio = parseFloat(
    document.getElementById("investment-ratio").value
  );
  const buyThreshold = parseFloat(
    document.getElementById("buy-threshold").value
  );
  const pbrThreshold = parseFloat(
    document.getElementById("pbr-threshold").value
  );
  const perThreshold = parseFloat(
    document.getElementById("per-threshold").value
  );
  const dividendThreshold = parseFloat(
    document.getElementById("dividend-threshold").value
  );
  const startDate = document.getElementById("start-date").value;
  const endDate = document.getElementById("end-date").value;
  const considerDelisting =
    document.getElementById("consider-delisting").checked;
  const portfolioSize = parseInt(
    document.getElementById("portfolio-size").value
  );

  // 예시 데이터를 사용한 차트 생성 (실제 데이터로 대체 필요)
  const ctx = document.getElementById("portfolio-chart").getContext("2d");
  const portfolioChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Day 1", "Day 2", "Day 3"], // 날짜 데이터로 대체
      datasets: [
        {
          label: "포트폴리오 가치",
          data: [initialCapital, initialCapital * 1.05, initialCapital * 1.1], // 실제 백테스팅 데이터로 대체
          borderColor: "rgba(75, 192, 192, 1)",
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: "날짜",
          },
        },
        y: {
          display: true,
          title: {
            display: true,
            text: "가치",
          },
        },
      },
    },
  });

  // 매수 및 매도 신호를 표시
  const signalsDiv = document.getElementById("signals");
  signalsDiv.innerHTML =
    "<h3>매수/매도 신호</h3><ul><li>매수 신호: Day 1</li><li>매도 신호: Day 2</li></ul>"; // 실제 신호 데이터로 대체
}

const calendarDates = document.getElementById("calendarDates");
const currentMonthElement = document.getElementById("currentMonth");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

function renderCalendar() {
  const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const startDayOfWeek = firstDayOfMonth.getDay();
  currentMonthElement.textContent = `${currentYear}년 ${currentMonth + 1}월`;
  calendarDates.innerHTML = "";

  for (let i = 0; i < startDayOfWeek; i++) {
    const emptyDate = document.createElement("div");
    emptyDate.classList.add("date", "empty");
    calendarDates.appendChild(emptyDate);
  }


  for (let i = 1; i <= daysInMonth; i++) {
    const dateElement = document.createElement("div");
    dateElement.classList.add("date");
    dateElement.textContent = i;
    calendarDates.appendChild(dateElement);
  }

}

renderCalendar();


prevBtn.addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();

  const events = [
    { startDate: "2025-02-10", endDate: "2025-02-18", eventName: "행사 A" },
    { startDate: "2025-02-08", endDate: "2025-02-12", eventName: "행사 B" },
    { startDate: "2025-02-15", endDate: "2025-02-18", eventName: "행사 C" },
    { startDate: "2025-05-11", endDate: "2025-05-25", eventName: "행사 D" }
  ];//버튼을 눌러 새롭게 달력이 생성되도 이벤트 값이 들어가도록 <-임시로 들어가 있는 데이터
  
  // 시작일 기준 오름차순 정렬
  events.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));
  
  // 이벤트마다 setDate 호출
  events.forEach(event => {
    setDate(event.startDate, event.endDate, event.eventName);
  });
});


nextBtn.addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar();
  const events = [
    { startDate: "2025-02-10", endDate: "2025-02-18", eventName: "행사 A" },
    { startDate: "2025-02-08", endDate: "2025-02-12", eventName: "행사 B" },
    { startDate: "2025-02-15", endDate: "2025-02-18", eventName: "행사 C" },
    { startDate: "2025-05-11", endDate: "2025-05-25", eventName: "행사 D" }
  ]; ///버튼을 눌러 새롭게 달력이 생성되도 이벤트 값이 들어가도록 <-임시로 들어가 있는 데이터
  
  // 시작일 기준 오름차순 정렬 (빠른 이벤트가 위로 오도록)
  events.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));
  
  // 이벤트마다 setDate 호출
  events.forEach(event => {
    setDate(event.startDate, event.endDate, event.eventName);
  });
});

function setDate(startDate, endDate, eventName) {   //이벤트 표시 함수
  // "YYYY-MM-DD" 형식의 문자열을 Date 객체로 변환
  const start = new Date(startDate);
  const end = new Date(endDate);

  // 랜덤 색상 배열 - 파스텔 계열
  const colors = ['#F15F5F', '#F29661', '#F2CB61', '#E5D85C', '#BCE55C',
    '#86E57F', '#5CD1E5', '#6799FF', '#6B66FF','#A566FF', '#F361DC', '#F361A6', ];
  const randomColor = colors[Math.floor(Math.random() * colors.length)];

  // 달력에서 날짜 셀(.date에서 .empty 제외)을 선택
  const dateCells = calendarDates.querySelectorAll('.date:not(.empty)');
  dateCells.forEach(cell => {
    // 셀에 표시된 숫자를 바탕으로 날짜 객체 생성 (현재 달과 연도 기준)
    const day = parseInt(cell.textContent, 10);
    const cellDate = new Date(currentYear, currentMonth, day);

    // 만약 셀의 날짜가 이벤트 기간에 포함된다면
    if (cellDate >= start && cellDate <= end) {
      // 이벤트 표시용 요소 생성
      const eventBar = document.createElement("div");
      eventBar.classList.add("event");
      eventBar.textContent = eventName;
      eventBar.style.backgroundColor = randomColor;
      eventBar.style.height = "10px";
      eventBar.style.marginTop = "5px";
      eventBar.style.borderRadius = "2px";
      eventBar.style.color = "white";
      eventBar.style.fontSize = "10px";
      eventBar.style.textAlign = "center";
      
      // 이벤트 시작일의 타임스탬프를 data 속성에 저장(
      eventBar.dataset.start = start.getTime();

      // 동일 셀 내에 이미 추가된 이벤트들 중 적절한 위치에 삽입하여 오름차순 정렬
      const existingEventBars = cell.querySelectorAll(".event");
      if (existingEventBars.length === 0) {
        cell.appendChild(eventBar);
      } else {
        let inserted = false;
        existingEventBars.forEach(existingBar => {
          if (!inserted && parseInt(existingBar.dataset.start) > start.getTime()) {
            cell.insertBefore(eventBar, existingBar);
            inserted = true;
          }
        });
        if (!inserted) {
          cell.appendChild(eventBar);
        }
      }
    }
  });
}

function detailEvent(startDate, endDate, eventName, location, explain, image){ //이벤트 디테일 표시 함수
  const start = new Date(startDate);
  const end = new Date(endDate);
  const Name = new Date(eventName);
  const Location = new Date(location);
  const Explain = new Date(explain);
  const Image = new Date(image);

  

}

const events = [
  { startDate: "2025-02-10", endDate: "2025-02-18", eventName: "행사 A" },
  { startDate: "2025-02-08", endDate: "2025-02-12", eventName: "행사 B" },
  { startDate: "2025-02-15", endDate: "2025-02-18", eventName: "행사 C" },
  { startDate: "2025-05-11", endDate: "2025-05-25", eventName: "행사 D" }
];//임시로 들어간 있는 데이터

// 시작일 기준 오름차순 정렬
events.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));

// 이벤트마다 setDate 호출
events.forEach(event => {
  setDate(event.startDate, event.endDate, event.eventName);
});

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

  // 시작 요일 이전의 빈 셀 생성
  for (let i = 0; i < startDayOfWeek; i++) {
    const emptyDate = document.createElement("div");
    emptyDate.classList.add("date", "empty");
    calendarDates.appendChild(emptyDate);
  }

  // 날짜 셀 생성
  for (let i = 1; i <= daysInMonth; i++) {
    const dateElement = document.createElement("div");
    dateElement.classList.add("date");
    dateElement.textContent = i;
    calendarDates.appendChild(dateElement);
  }
}

// 이벤트 데이터를 달력에 적용하는 함수
function updateCalendarEvents() {
  // myEvents는 템플릿에서 전달받은 배열입니다.
  myEvents.forEach(event => {
    setDate(
      event.startDate, 
      event.endDate, 
      event.eventName, 
      event.location, 
      event.explain, 
      event.image
    );
  });
}

// 최초 달력 렌더링 및 이벤트 적용
renderCalendar();
updateCalendarEvents();

prevBtn.addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();
  updateCalendarEvents(); // 새 달력에 다시 이벤트 적용
});

nextBtn.addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar();
  updateCalendarEvents(); // 새 달력에 다시 이벤트 적용
});

/**
 * setDate: 지정한 날짜 범위에 해당하는 달력 셀에 이벤트 표시를 추가
 * @param {string} startDate - "YYYY-MM-DD" 형식의 시작 날짜
 * @param {string} endDate - "YYYY-MM-DD" 형식의 종료 날짜
 * @param {string} eventName - 행사 이름
 * @param {string} location - 행사 위치
 * @param {string} explain - 행사 설명
 * @param {string} image - 행사 이미지 URL
 */
function setDate(startDate, endDate, eventName, location, explain, image) {
  const start = new Date(startDate);
  const end = new Date(endDate);

  // 랜덤 색상 배열
  const colors = ['#F15F5F', '#F29661', '#F2CB61', '#E5D85C', '#BCE55C', '#86E57F'];
  const randomColor = colors[Math.floor(Math.random() * colors.length)];

  // 달력에서 날짜 셀(.date 중 .empty 제외)을 선택
  const dateCells = calendarDates.querySelectorAll('.date:not(.empty)');
  dateCells.forEach(cell => {
    // 셀의 숫자(일)를 바탕으로 현재 달의 날짜 객체 생성
    const day = parseInt(cell.textContent, 10);
    const cellDate = new Date(currentYear, currentMonth, day);

    // 셀 날짜가 이벤트 기간에 포함되면
    if (cellDate >= start && cellDate <= end) {
      // 이벤트 표시용 요소 생성
      const eventBar = document.createElement("div");
      eventBar.classList.add("event");
      eventBar.textContent = eventName;
      eventBar.style.backgroundColor = randomColor;
      eventBar.style.height = "20px";
      eventBar.style.marginTop = "5px";
      eventBar.style.borderRadius = "2px";
      eventBar.style.color = "white";
      eventBar.style.fontSize = "10px";
      eventBar.style.textAlign = "center";
      
      // 시작일 타임스탬프 (정렬 기준) 및 추가 데이터 저장
      eventBar.dataset.start = start.getTime();
      eventBar.dataset.location = location;
      eventBar.dataset.explain = explain;
      eventBar.dataset.image = image;
      
      // 클릭 시 오른쪽 상세 정보 영역 업데이트
      eventBar.addEventListener("click", () => {
        // image 변수는 my_image 값을 담고 있음 (예: "static/pic/fall.png")
        let imagePath = image;
        // 경로가 절대경로가 아니라면 앞에 '/' 추가
        if (!imagePath.startsWith("/")) {
          imagePath = "/" + imagePath;
        }
        document.getElementById("detailImage").src = imagePath;
        document.getElementById("detailEventName").textContent = eventName;
        document.getElementById("detailLocation").textContent = "위치: " + location;
        document.getElementById("detailExplain").textContent = "설명: " + explain;
      });

      // 동일 셀 내에 이미 추가된 이벤트들 사이에 시작일 기준 오름차순 정렬로 삽입
      const existingEvents = cell.querySelectorAll(".event");
      if (existingEvents.length === 0) {
        cell.appendChild(eventBar);
      } else {
        let inserted = false;
        existingEvents.forEach(existingEvent => {
          if (!inserted && parseInt(existingEvent.dataset.start) > start.getTime()) {
            cell.insertBefore(eventBar, existingEvent);
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

// -------------------------
// 전역 변수 및 DOM 요소 참조
// -------------------------

// 달력의 날짜들이 들어갈 컨테이너
const calendarDates = document.getElementById("calendarDates");

// 현재 달/년을 표시하는 요소 (예: "2025년 2월")
const currentMonthElement = document.getElementById("currentMonth");

// 이전 달, 다음 달로 이동시키는 버튼
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// 오늘 날짜 기준으로 초기 currentMonth, currentYear 설정
const today = new Date();
let currentMonth = today.getMonth();  // 0 ~ 11 (0=1월, 11=12월)
let currentYear = today.getFullYear(); // 예: 2025

// -------------------------
// 달력 렌더링 함수
// -------------------------
function renderCalendar() {
  // 현재 달의 1일(예: 2025-02-01) 기준 정보
  const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
  
  // 현재 달에 며칠까지 있는지 계산 (예: 2월이면 28, 29)
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  
  // 달의 시작 요일 (일:0, 월:1, ... 토:6)
  const startDayOfWeek = firstDayOfMonth.getDay();
  
  // 달력 헤더(예: "2025년 2월") 업데이트
  currentMonthElement.textContent = `${currentYear}년 ${currentMonth + 1}월`;
  
  // 달력 날짜 부분을 초기화 (이전 달의 날짜들이 남아있지 않도록)
  calendarDates.innerHTML = "";

  // 1일이 시작되는 요일 이전에 빈 칸(빈 셀)을 생성
  // 예: 2월 1일이 수요일이면, 일, 월, 화 (3일)만큼 빈 셀이 필요
  for (let i = 0; i < startDayOfWeek; i++) {
    const emptyDate = document.createElement("div");
    emptyDate.classList.add("date", "empty");  // 'empty'는 클릭이나 이벤트 표시를 막기 위함
    calendarDates.appendChild(emptyDate);
  }

  // 실제 날짜 셀 생성 (1일부터 daysInMonth일까지)
  for (let i = 1; i <= daysInMonth; i++) {
    const dateElement = document.createElement("div");
    dateElement.classList.add("date");
    dateElement.textContent = i;  // 날짜 숫자를 셀에 표시
    calendarDates.appendChild(dateElement);
  }
}

// -------------------------
// 달력에 이벤트를 표시하는 함수
// -------------------------
function updateCalendarEvents() {
  // myEvents 배열에 담긴 각 이벤트 정보를 setDate 함수로 전달
  // myEvents는 HTML 템플릿에서 전역으로 선언했다고 가정 (예: const myEvents = [...])
  myEvents.forEach(event => {
    setDate(
      event.startDate,   // "YYYY-MM-DD" 형식의 시작 날짜
      event.endDate,     // "YYYY-MM-DD" 형식의 종료 날짜
      event.eventName,   // 행사 이름
      event.location,    // 행사 위치
      event.explain,     // 행사 설명
      event.image        // 행사 이미지 경로 (예: "fall.png")
    );
  });
}

// -------------------------
// 초기 달력 렌더링 및 이벤트 표시
// -------------------------
renderCalendar();
updateCalendarEvents();

// -------------------------
// 이전 달 버튼 클릭 시
// -------------------------
prevBtn.addEventListener("click", () => {
  // currentMonth를 1 감소 (예: 2월 -> 1월)
  currentMonth--;
  // 만약 1월에서 이전 달을 누르면 (currentMonth < 0) => 전 해의 12월로 이동
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  // 달력을 다시 렌더링하고, 이벤트도 다시 표시
  renderCalendar();
  updateCalendarEvents();
});

// -------------------------
// 다음 달 버튼 클릭 시
// -------------------------
nextBtn.addEventListener("click", () => {
  // currentMonth를 1 증가 (예: 2월 -> 3월)
  currentMonth++;
  // 만약 12월에서 다음 달을 누르면 (currentMonth > 11) => 다음 해의 1월로 이동
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  // 달력을 다시 렌더링하고, 이벤트도 다시 표시
  renderCalendar();
  updateCalendarEvents();
});

/**
 * setDate 함수
 * - 지정한 날짜 범위(시작일 ~ 종료일)에 해당하는 달력 셀에 이벤트 표시를 추가합니다.
 * - 클릭 시 detail-container에 상세 정보를 표시하도록 설정합니다.
 *
 * @param {string} startDate  - "YYYY-MM-DD" 형식의 시작 날짜
 * @param {string} endDate    - "YYYY-MM-DD" 형식의 종료 날짜
 * @param {string} eventName  - 행사 이름
 * @param {string} location   - 행사 위치
 * @param {string} explain    - 행사 설명
 * @param {string} image      - 행사 이미지 파일명 (예: "fall.png")
 */
function setDate(startDate, endDate, eventName, location, explain, image) {
  // startDate와 endDate를 Date 객체로 변환
  const start = new Date(startDate);
  const end = new Date(endDate);

  // 이벤트 배경색을 무작위로 선택 (하이라이트 역할)
  const colors = ['#F15F5F', '#F29661', '#F2CB61', '#E5D85C', '#BCE55C', '#86E57F', '#FFD8D8','#FAF4C0','#CEFBC9','#DAD9FF'];
  const randomColor = colors[Math.floor(Math.random() * colors.length)];

  // 달력에서 날짜 셀(클래스가 .date이면서 .empty가 아닌 셀들) 선택
  // => 실제 날짜가 있는 셀들만 대상
  const dateCells = calendarDates.querySelectorAll('.date:not(.empty)');
  
  // 각 날짜 셀을 순회
  dateCells.forEach(cell => {
    // 셀 안의 텍스트를 숫자로 변환 (일자)
    const day = parseInt(cell.textContent, 10);
    // 현재 year, month, day로 Date 객체를 생성 (셀의 실제 날짜)
    const cellDate = new Date(currentYear, currentMonth, day);

    // 만약 이 셀의 날짜가 이벤트 기간에 포함된다면
    if (cellDate >= start && cellDate <= end) {
      // 이벤트를 시각적으로 표시할 작은 div를 생성
      const eventBar = document.createElement("div");
      eventBar.classList.add("event");
      eventBar.textContent = eventName;        // div 안에 행사 이름 표시
      eventBar.style.backgroundColor = randomColor; // 무작위 색상
      eventBar.style.height = "20px";               // 높이
      eventBar.style.marginTop = "5px";
      eventBar.style.borderRadius = "2px";
      eventBar.style.color = "white";
      eventBar.style.fontSize = "10px";
      eventBar.style.textAlign = "center";
      
      // 이벤트 시작일 타임스탬프를 data 속성에 저장 (같은 셀에 여러 이벤트가 있을 때 정렬용)
      eventBar.dataset.start = start.getTime();
      // 상세 정보(위치, 설명, 이미지 경로)도 data 속성으로 저장할 수 있음
      eventBar.dataset.location = location;
      eventBar.dataset.explain = explain;
      eventBar.dataset.image = image;
      
      // 이벤트를 클릭하면 detail-container에 상세 정보 표시
      eventBar.addEventListener("click", () => {
        // imagePath를 실제로 사용 가능한 경로로 만든다
        // 여기서는 'static/pic/' 디렉토리 하위에 이미지 파일이 있다고 가정
        document.getElementById("detailImage").src = 'static/pic/' + image;
        document.getElementById("detailEventName").textContent = eventName;
        document.getElementById("detailLocation").textContent = "위치: " + location;
        document.getElementById("detailExplain").textContent = "설명: " + explain;
      });

      // 이미 이 날짜 셀에 다른 이벤트들이 들어 있을 수 있으므로
      // 이벤트 시작일 기준으로 오름차순 정렬을 해준다.
      const existingEvents = cell.querySelectorAll(".event");
      if (existingEvents.length === 0) {
        // 기존 이벤트가 없다면 그냥 추가
        cell.appendChild(eventBar);
      } else {
        // 기존 이벤트들이 있을 때, 적절한 위치에 삽입
        let inserted = false;
        existingEvents.forEach(existingEvent => {
          // 기존 이벤트보다 start가 작으면(더 이른 이벤트면) 그 앞에 삽입
          if (!inserted && parseInt(existingEvent.dataset.start) > start.getTime()) {
            cell.insertBefore(eventBar, existingEvent);
            inserted = true;
          }
        });
        // 만약 삽입되지 않았다면(가장 늦은 이벤트라면) 맨 뒤에 붙인다
        if (!inserted) {
          cell.appendChild(eventBar);
        }
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
    const slider = document.querySelector(".slider");
    const eventItems = document.querySelectorAll(".eventItem");
    const prevBtn = document.querySelector(".prev");
    const nextBtn = document.querySelector(".next");

    let index = 0;
    const slidesToShow = 5; // 한 번에 보여줄 이미지 개수
    const slideWidth = eventItems[0].offsetWidth; // 개별 슬라이드 크기
    const totalSlides = eventItems.length;

    function updateSlider() {
        slider.style.transform = `translateX(${-index * slideWidth}px)`;
    }

    nextBtn.addEventListener("click", () => {
        if (index + slidesToShow < totalSlides) {
            index += slidesToShow;
        } else {
            index = 0; // 마지막에서 처음으로 돌아감
        }
        updateSlider();
    });

    prevBtn.addEventListener("click", () => {
        if (index - slidesToShow >= 0) {
            index -= slidesToShow;
        } else {
            index = Math.max(0, totalSlides - slidesToShow); // 처음에서 마지막으로 이동
        }
        updateSlider();
    });
});

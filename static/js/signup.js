
    (function() {
        var signupUseridInput = document.getElementById('id');
        var signupForm = document.getElementById('signupForm');
        var signupBtn = signupForm.querySelector('button[type="submit"]');
        var duplicationChecked = false;
        
        // 페이지 로드 시 회원가입 버튼 비활성화
        signupBtn.disabled = true;

        // 중복 확인 버튼 이벤트 (AJAX 사용)
        document.getElementById('overlap').addEventListener('click', function() {
            var userId = signupUseridInput.value.trim();
            if (!userId) {
                alert('사용자 ID를 입력하세요.');
                return;
            }
            // AJAX 호출: 서버의 /checkDup 엔드포인트에 userId 전달
            fetch('/checkDup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ userId: userId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    alert('아이디가 증복 되었습니다 다른 아이디를 입력해주세요');
                    duplicationChecked = false;
                    signupBtn.disabled = true;
                } else {
                    alert('사용가능한 아이디 입니다');
                    duplicationChecked = true;
                    signupBtn.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        // 회원가입 폼 제출 전 중복 확인 여부 검사
        signupForm.addEventListener('submit', function(event) {
            if (!duplicationChecked) {
                alert('증복 확인 하시기 바랍니다.');
                event.preventDefault();
            }
        });
    })();

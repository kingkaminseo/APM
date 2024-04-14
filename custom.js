function toggleDiv(event) {
    event.preventDefault();

    var div = document.getElementById("myDiv");
    var currentDisplay = div.style.display;

    if (currentDisplay === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}

function changeColor(event) {
    // 모든 <a> 태그에서 'selected' 클래스 제거
    const links = document.querySelectorAll('.simpleul a');
    links.forEach(link => link.classList.remove('selected'));

    // 클릭한 <a> 태그에 'selected' 클래스 추가
    const clickedLink = event.target;
    clickedLink.classList.add('selected');
}

window.addEventListener('scroll', function () {
    var banner = document.querySelector('.flip');
    var bannerHeight = banner.offsetHeight;
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var scrollThreshold = 459; // 고정되는 스크롤 거리를 조정하세요


    if (scrollTop > scrollThreshold) {
        banner.classList.add('sticky');
    } else {
        banner.classList.remove('sticky');
    }
});




   // 메뉴 요소를 선택합니다.
   const menu = document.querySelector('.menu');

   // 메뉴 내의 링크 요소를 선택합니다.
   const links = menu.querySelectorAll('.mainnav');

   // 링크 요소에 클릭 이벤트 리스너를 추가합니다.
   links.forEach(link => {
       link.addEventListener('click', (event) => {
           event.preventDefault(); // 링크의 기본 동작을 막습니다.

           // 현재 클릭된 링크에 active 클래스를 추가하고, 이전에 active 클래스를 가진 링크에서는 제거합니다.
           links.forEach(link => {
               if (link === event.target) {
                   link.classList.add('active');
               } else {
                   link.classList.remove('active');
               }
           });
       });
   });













   var flip = document.querySelector('.flip');
   var card = document.querySelector('.card');
   var adbtn = document.querySelector('.adbtn');

   adbtn.addEventListener('click', function(event) {
       event.preventDefault(); // 기본 동작(링크 이동) 막기
       card.style.transition = 'none'; // 애니메이션 멈춤
       setTimeout(function() {
           card.style.transform = 'rotateY(180deg)'; // 회전 애니메이션 적용
           card.style.transition = ''; // 애니메이션 재개
       }, 0);
   });











  




// CSV 파일 경로
var csvFile = "python sleeps here/전체.csv"; // 여기에 실제 파일 경로를 넣어주세요.

// HTML 테이블의 tbody 요소를 가져옵니다.
var tableBody = document.getElementById("tableBody");

// CSV 파일을 불러와서 처리하는 함수
function loadCSVFile() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", csvFile, true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var csvData = xhr.responseText;
            var lines = csvData.split("\n");

            for (var i = 1; i < lines.length; i++) {
                var rowData = lines[i].split(",");
                var row = tableBody.insertRow(-1);

                // 숙소 이름과 위치 정보 추가
                var cell1 = row.insertCell(0);
                cell1.textContent = rowData[0];

                var cell2 = row.insertCell(1);
                cell2.textContent = rowData[1];

                // 이미지 추가
                var cell3 = row.insertCell(2);
                var img = document.createElement("img");
                img.src = rowData[2];
                cell3.appendChild(img);
            }
        }
    };

    xhr.send();
}

// 페이지 로드 시 CSV 파일 불러오기 함수 호출
window.onload = loadCSVFile;





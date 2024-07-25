/** 첨부파일 처리 핸들러(jquery활용) */


//csrf_token 초기화
$(function () {
    var csrf_token = $('csrf_token').val() // main.html에서 id나 class로 된 게 아니라 그냥 저 이름으로 form을 통해 전달된다.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    })
})

var FILE_NUM = 10 // 첨부된 파일 개수
var FILE_ARRAY = new Array() // 첨부 파일 저장용 배열(파일을 배열에 넣게 되면 로컬 컴퓨터 메모리에 올라가 있는 거임)

function add_file(obj){
    let max_file_count = 10 // 첨부 파일 최대 개수
    let attach_file_count = $('.filebox').length
    let remain_file_count = max_file_count - attach_file_count
    let current_file_count = obj.files.length // 현재 첨부된 파일 개수
    $('#attached-file-list').attr('hidden', false) // id가 attached-file-list인 HTML컴포넌트의 attribute중 hidden을 false로 바꾼다.
    // 첨부 파일 개수 확인
    if (current_file_count > remain_file_count){
        alert(`첨부파일은 최대 ${max_file_count}까지 첨부 가능 합니다.`)
    } else{
        for(const file of obj.files){
            // 파일 검증
            if(validation(file)){
                let reader = new FileReader() // 파일 읽기 위한 객체 생성(js 내장 클래스)
                reader.readAsDataURL(file) // 파일 읽기
                reader.onload = function(){ // 파일 읽기가 성공했다면 어떤 함수를 실행시킬 거냐?
                    FILE_ARRAY.push(file) // 배열에 저장하는 함수를 실행할 거다.
                }
                // 파일 목록을 화면에 추가
                const img_path = '<img src="/static/imgs/delete-doc.ico" width="20px" alt="문서 삭제">'
                let html_data =`
                <div class="filebox my-2 ml-2" id="file${FILE_NUM}">
                    <p class="name">
                        첨부${FILE_NUM + 1}: ${file.name}
                        <span>
                            <a class="delete" onclick="deleteFile(${FILE_NUM});">${img_path}</a>
                        </span>
                    </p>
                </div>`
                $('.file-list').append(html_data) // main.html에다가 파일 추가
                FILE_NUM++ // 파일 추가 되었으니 늘려주기
            } else{
                continue // 현재 파일이 검증을 통과하지 못하면 다음 파일로 넘어가기
            }

        }
    }
    // 첨부 파일을 저장하였으므로 Form input 내용 초기화
    $('input[type=file]').val('')
}

// 업로드 되는 파일을 검증하는 함수
function validation(obj){
    const fileTypes = [
        'application/pdf',
        'application/haansofthwp',
        'application/x-hwp',
        'application/msword', // .doc
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
        'application/vnd.ms-excel', // .xls
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
        'video/x-msvideo', // .avi
        'application/zip',
        'audio/mpeg',
        'video/mp4',
        'video/mpeg',
        'image/gif',
        'image/jpeg',
        'image/png',
        'image/bmp',
        'image/tif',
        'text/plain', // .txt
        'text/csv', // .csv
    ]

    if (obj.name.legnth > 200){
        alert('파일명이 200글자 이상인 파일은 제외되었습니다.')
        return false
    } else if (obj.size > (500*1024*1024)){
        alert('최대 500메가를 초과한 파일은 제외되었습니다.')
        return false
    } else if (obj.name.lastIndexOf('.') == false){
        alert('확장자가 없는 파일은 제외되었습니다.')
        return false
    } else if (!fileTypes.includes(obj.type)){
        alert('지원하지 않는 파일형식은 제외되었습니다.')
        return false
    } else {
        return true
    }

}

function deleteFile(num){
    $('#file'+num).remove() // id가 file넘버 인 HTML 태그를 잡아서 화면상에서 없애기(제이쿼리 문법)
    FILE_ARRAY.splice(num, 1) // 삭제하고 싶은 파일의 인덱스를 통해 배열에서도 삭제
    FILE_NUM--
}

$(function(){
    // 서버 전송하기 버튼을 클릭한 경우 서버 전송 처리
    let submit_btn = $('#submit_files')
    submit_btn.on('click', function(e){
        // 파일이 첨부되어 있는지 확인
        if (FILE_NUM === 0){
            alert('첨부파일이 없습니다. \n분석할 파일을 추가해주세요')
            return
        }
        // 분석할 파일이 있다면 서버로 전송
        let form_data = saveFilesToForm()
        e.preventDefault() // a태그의 기본 이벤트는 href로 이동. 근데 그 기본(default)동작을 하지못하게 막는 것(prevent) 왜? 서버로 보낼 거니까.
        $.ajax({
            method : 'POST',
            url : '/process',
            data : form_data,
            dataType : 'json',
            contentType : false,
            processData : false,
            cache : false,
            success : function(result){ // ajax요청이 성공했든 실패했든 무언가를 반환해주는데 그걸 매개변수로 받게 됨. 매개변수 이름은 자유.
                console.log(result['content'])
                let text_area = $('#floatingTextarea2');
                $('#textarea_label').remove();
                text_area.attr('readonly', false)
                text_area.val(result['content'])
                text_area.attr('readonly', true)

            },
            error : function(error){
                alert('에러가 발생했습니다.')
                console.log(error)
                return
            }
        })
    })
    /* 화면 초기화 버튼을 클릭했을 경우 처리*/
    $('#clear-content-btn').on('click', function(){
        location.reload();
    });
})

function saveFilesToForm(){
    let form = $('form') // form태그를 잡는데 id나 class이름이 아닌 form태그 이름으로 잡는다.
    let form_data = new FormData(form[0]) // form이 여러 개일 때 첫번째 form을 서버로 보낸다.
    for(let i=0; i<FILE_ARRAY.length; i++){
        form_data.append('file', FILE_ARRAY[i])
    }
    return form_data
}
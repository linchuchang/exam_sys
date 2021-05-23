function getCookie(name) {
    var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
    if (arr != null)
        return unescape(arr[2]);
}
window.onload = function () {
    //调用方法，获得身份信息
    let identity = getCookie("identity");
    if (identity == 'student') {
        $("p[class$='student-description']").css('display', 'block');
        $("p[class$='teacher-description']").css('display', 'none');
    } else {
        $("p[class$='student-description']").css('display', 'none');
        $("p[class$='teacher-description']").css('display', 'block');
    }
    //将所有input设为不可编辑
    $("input[class$='edit']").attr('readOnly', true)
};




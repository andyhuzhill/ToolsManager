var log = console.log.bind(document);

function doSubmit() {
    var userID = document.querySelector("#user-id").value;
    if (userID == "") {
        alert("请输入用户ID!");
        return false;
    }
    var password = document.querySelector("#password").value;
    if (password == "") {
        alert("请设置密码!");
        return false;
    }
    var name = document.querySelector("#name").value;
    if (name == "") {
        alert("请输入用户名");
        return false;
    }
    var photo = document.querySelector("#photo").value;
    if (photo == "") {
        alert("请上传照片!");
        return false;
    }
    var duty = document.querySelector("#duty").value;
    if (duty == "") {
        alert("请输入用户职务");
        return false;
    }
    var department = document.querySelector("#department").value;
    if (department == "") {
        alert("请输入部门名称");
        return false;
    }
    var re_phone_num = /^\d+$/;
    var phone_number = document.querySelector("#phone-number").value;
    if (phone_number == "" || !re_phone_num.test(phone_number)) {
        alert("请输入合法的电话号码");
        return false;
    }

    var submitForm = document.querySelector("#add-form");
    submitForm.submit();
}

function fileChanged(target) {
    if ((target.files.length != 0)) {
        var fileType = target.files[0].type;
        var reg = /^image/;

        if (!reg.test(fileType)) {
            alert("请不要上传非图片文件！");
            target.value = '';
            return ;
        }

        if (target.files[0].size > 512 * 1024) {
            alert("请不要上传超过512kb大小的图片！");
            target.value = '';
            return ;
        }
    }   
}
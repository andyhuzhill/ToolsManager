var log = console.log.bind(document)

function doSubmit() {
    var userID = document.querySelector("#user-id").value
    log(userID)
    return false
}

function fileChanged(target) {
    if ((target.files.length != 0)) {
        var fileType = target.files[0].type
        var reg = /^image/

        if (!reg.test(fileType)) {
            alert("请不要上传非图片文件！")
            target.value = ''
            return 
        }

        if (target.files[0].size > 512 * 1024) {
            alert("请不要上传超过512kb大小的图片！")
            target.value = ''
            return 
        }
    }   
}
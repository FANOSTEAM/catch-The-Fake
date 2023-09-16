let certificateForm = $('#certificateForm');
let c2=document.getElementById('certificateForm')
certificateForm.on('submit',(e)=>{  
e.preventDefault()
    var data = new FormData();

    // var url = "/single_upload/";
    // data.append("file", $("input[id^='file']")[0].files[0]);

    var url = "{%url 'adminUpload'%}";
    var files = $("input[id^='file']")[0].files;
    for (i=0; i<files.length; i++) {
      data.append("files", files[i]);
    }
    let  excel=$("input[id^='excel']")[0].files[0];
    console.log(excel)
    data.append('excel',excel)
    data.append("csrfmiddlewaretoken", "{{ csrf_token }}");
    $.ajax({
      method: "POST",
      url: url,
      processData: false,
      contentType: false,
      mimeType: "multipart/form-data",
      data: data,
      success: function (res) {
        var blob=new Blob([res]);
    var link=document.createElement('a');
    link.href=window.URL.createObjectURL(blob);
    link.download="certificate.bmp";
    link.click();}})
      },
    );
  


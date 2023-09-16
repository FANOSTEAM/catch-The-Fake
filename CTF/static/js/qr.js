


document.addEventListener("DOMContentLoaded", function(event){



  const body= document.getElementById('form-container')
  let scan= 0;
  let toggleBtn=document.getElementById('qr')
  const html5QrCode = new Html5Qrcode("reader");
  const reader =document.getElementById("reader");
  const fileinput = document.getElementById('qr-input-file');

  toggleBtn.addEventListener('click',(e)=>{
      if (scan==0){
      const qrCodeSuccessCallback = (decodedText, decodedResult) => {
        $.ajax(
          {url:'/verify/search/',
          type:'GET',
          mode: 'same-origin',
          data:{'id':decodedText},
      success:function (response){
        var blob=new Blob([response]);
        var link=document.createElement('a');
        link.href=window.URL.createObjectURL(blob);
        link.download="certificate.pdf";
        link.click();}})
      };
        const config = { fps: 10, qrbox: { width: 400, height: 300 } };
          html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback);
          scan=1
          toggleBtn.textContent='stop scan'
      }
        
      else {
          html5QrCode.stop().then((ignore) => {
              // QR Code scanning is stopped.
              console.log("stop was success")
              scan=0
              toggleBtn.textContent='start scan'
            }).catch((err) => {
              console.log(`error occured with: ${err}`)
            });
           
  
      }})
      fileinput.addEventListener('change', e => {
        if (e.target.files.length == 0) {
          // No file selected, ignore 
          return;
        }
      
        const imageFile = e.target.files[0];
        // Scan QR Code
        html5QrCode.scanFile(imageFile)
        .then(decodedText => {
          console.log(decodedText);
         
          $.ajax(
              {url:'/verify/search/',
              type:'GET',
              mode: 'same-origin',
              data:{'id':decodedText},
          success:function (response){
            var blob=new Blob([response]);
            var link=document.createElement('a');
            link.href=window.URL.createObjectURL(blob);
            link.download="certificate.pdf";
            link.click();}})

      }).catch(err => {
                // failure, handle it.
                reader.textContent=""
                console.log(`Error scanning file. Reason: ${err}`)
           
              })
              });
          
          
          
      })


  

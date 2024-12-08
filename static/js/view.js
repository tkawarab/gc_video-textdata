
    
    function OnFileSlect( inputElement ){
        // ファイルリストを取得
        var fileList = inputElement.files;
    
        // ファイルの数を取得
        var fileCount = fileList.length;
    
        // HTML文字列の生成
        var fileListBody = "<br>選択されたファイルの数 = " + fileCount + "<br/><br/>";
    
        // 選択されたファイルの数だけ処理する
        for ( var i = 0; i < fileCount; i++ ) {
    
            // ファイルを取得
            var file = fileList[ i ];
    
            // ファイルの情報を文字列に格納
            //fileListBody += "[ " + ( i + 1 ) + "ファイル目 ]<br/>";
            fileListBody += file.name + "<br/>";
            //fileListBody += "type             = " + file.type + "<br/>";
            //fileListBody += "size             = " + file.size + "<br/>";
            //fileListBody += "lastModifiedDate = " + file.lastModifiedDate + "<br/>";
            //fileListBody += "lastModified     = " + file.lastModified + "<br/>";
            //fileListBody += "<br/>";
        }
    
        // 結果のHTMLを流し込む
        document.getElementById( "ID001" ).innerHTML = fileListBody;    
        document.getElementById( "submit_btn" ).style.display = "inline-block";

    }

    //window.onload = function(){
    window.addEventListener('load', function(){
        document.getElementById("submit_btn").onclick = function() {
            function loading(){
                document.getElementById("fullOverlay").style.display = "block";  
            }
            function req_send(token){
                const fd = new FormData();
                total = document.getElementById("select_input").files.length;
                for (var i=0; i<total; i++){
                    file_name = document.getElementById('select_input').files[i].name;
                    fd.append("files", document.getElementById('select_input').files[i],file_name);
                    console.log(file_name);
                }

                var request = new XMLHttpRequest();
                request.onload = function(){
                    var data = this.response;   
                    const blob = new Blob([data], {type: "application/zip"});
                    var objectURL = URL.createObjectURL(blob);
                    a = document.createElement("a");
                    document.body.appendChild(a);
                    //a.download = 'test.zip'
                    a.href = objectURL;
                    a.click();
                    document.body.removeChild(a);
                    document.getElementById("fullOverlay").style.display = "none";                
                    window.alert("完了しました")
                }            

                request.open("POST", "/create_sbv", true); 
                //request.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded' ); // 明示的に宣言しない
                request.responseType = 'blob';
                request.setRequestHeader( 'Accept', 'application/zip' );
                request.setRequestHeader( 'Authorization', `Bearer ${token}` );
                request.send(fd);
            }

            function req_video_text_detection(request,fd,token){
                request.onload = function(){
                    var data = this.response;   
                    const blob = new Blob([data], {type: "application/zip"});
                    var objectURL = URL.createObjectURL(blob);
                    a = document.createElement("a");
                    document.body.appendChild(a);
                    //a.download = 'test.zip'
                    a.href = objectURL;
                    a.click();
                    document.body.removeChild(a);
                    window.alert("完了しました")                
                    document.getElementById("fullOverlay").style.display = "none";  

                }            

                request.open("POST", "/video_text_detection", true); 
                request.responseType = 'blob';
                //request.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded' );
                request.setRequestHeader( 'Content-Type', 'application/json' );                
                request.setRequestHeader( 'Accept', 'application/zip' );
                request.setRequestHeader( 'Authorization', `Bearer ${token}` );

                files = fd.getAll('files');
                var array = []
                for (file of files){
                    array.push(file.name);
                }
                var data = JSON.stringify(array);
                request.send(data);
            }            

            function req_generate_url(request,fd,token){
                console.log("generate_url");
                request.onload = function(){
                    var data = this.response;   
                    req_upload_file(fd,data)
                }                      
                request.open("POST", "/upload_file", false); 
                request.setRequestHeader( 'Content-Type', 'application/x-www-form-urlencoded' );
                request.setRequestHeader( 'Authorization', `Bearer ${token}` );
                request.send("file_name=" + fd.name);                
            }

            function req_upload_file(fd,urls){
                console.log("upload_file")
                var g_request = new XMLHttpRequest();
                var cnt = 0;

                //for (url in urls){
                    g_request.onload = function(){
                        console.log("upload_file_end");
                    }                    
                    g_request.open("PUT", urls.replace(/"/g,""), false); 
                    g_request.setRequestHeader( 'Content-Type', 'application/octet-stream' );
                    g_request.send(fd)
                //}
            }
            
            async function gcs_upload(request,fd,token){
                console.log("gcs_upload");
                await Promise.all(
                    fd.getAll('files').map(async value => {
                        file_name = value.name;
                        console.log(file_name);
                        //fd.append("files", value,file_name);
                        await req_generate_url(request,value,token);
                    })
                )
                await req_video_text_detection(request,fd,token)
                console.log("gcs_upload_end")

            }
            console.log("loading");
            loading();
            window.setTimeout(function(){
                get_idtoken().then(result => {
                    console.log("start");
                    token = result
                    var request = new XMLHttpRequest();
                    const fd = new FormData();
                    total = document.getElementById("select_input").files.length;
                    for (var i=0; i<total; i++){
                        file_name = document.getElementById('select_input').files[i].name;
                        fd.append("files", document.getElementById('select_input').files[i],file_name);
                    }                
                    gcs_upload(request,fd,token);
                });
            }, 1000);

       
        }        
    });   
import { showToast, updateLabelChars } from "../../global/functios.js";


(() => {
  // btn aplicar cambios en la edición
  document.getElementById("sendEditedPost").addEventListener("click", (e) => {

    let type_post = document.getElementById("type_post").value.length; // int > 0
    let theme_category = document.getElementById("theme_category").value.length; // int > 0
    let post_title = document.getElementById("post_title").value.length; // int > 0
    let resume_post = document.getElementById("resume_post").value.length; // int > 0
    let lenNewPost = `${CKEDITOR.instances.ckeditor.document.getBody().getText()}`.length; // int
    let inputFile = document.getElementById("uploadFile");
    let t = "error";
    let m;


    if (type_post == 0 || theme_category == 0 || post_title == 0 || resume_post == 0 || lenNewPost <= 1) {
      e.preventDefault();
      m = "<p>Verificar los campos vacios, todos los campos son obligatorios</p>";
      showToast(t, m);
    }

    if (inputFile.style.color == 'red') {
      e.preventDefault();
      m = "<p>Verificar que el archivo sea de una extensión compatible o que no se haya cargado previamente.</p>"
      showToast(t, m)
    }
  });
})();

(() => {
  let charNumPost = document.getElementById("charNumPost");
  let sendPost = document.getElementById("sendEditedPost");
  let maxChrs = 50000;

  let editor = CKEDITOR.instances.ckeditor;

  editor.on('instanceReady', function (event) {

    // inicio fetch
    let url = window.location.href + '/post-info';
    fetch(url)
      .then(dataJson => dataJson.json())
      .then(data => {

        let f_name = document.getElementById("file_name");
        let f_size = document.getElementById("file_size");

        // inicio vaciado de información en campos
        document.getElementById("type_post").value = data['id_tp_post'];
        document.getElementById("theme_category").value = data['id_category'];
        document.getElementById("post_title").value = data['str_post_title'];
        document.getElementById("resume_post").value = data['str_resumen_post'];

        if (f_name != null) {
          f_name.innerText = data['str_file_name'];
          f_size.innerText = data['str_file_size'];
        }

        CKEDITOR.instances.ckeditor.setData(data['str_html_body_post']);

        // final vaciado de información en campos

        // inicio conteo de caracteres:
        updateLabelChars('resume_post', 'charNum', 500);
        updateLabelChars('post_title', 'charNumTitle', 100);
        // final conteo de caracteres:

        // inicio conteo caracteres CKEDITOR
        this.document.on("keyup", function (event) {

          let lenContentCkeditor = `${CKEDITOR.instances.ckeditor.document.getBody().getText()}`.length;
          let numeroFormateado = lenContentCkeditor.toLocaleString();

          if (lenContentCkeditor == 1) {
            charNumPost.innerText = `0 / 50,000`;
            charNumPost.style.color = 'black';
          } else if (lenContentCkeditor >= 1 && lenContentCkeditor <= 40000) {
            charNumPost.style.color = 'green';
          } else if (lenContentCkeditor > 40000 && lenContentCkeditor <= 45000) {
            charNumPost.style.color = 'orange';
          } else if (lenContentCkeditor > 45000 && lenContentCkeditor <= 50000) {
            charNumPost.style.color = 'red';
          };

          charNumPost.innerText = `${numeroFormateado} / 50,000`;

          if (lenContentCkeditor > 50000) {
            charNumPost.innerText = `Máximo 50,000 caracteres, ingresados: ${numeroFormateado}`;
            charNumPost.style.color = 'red';
            sendPost.disabled = true;
          } else if (lenContentCkeditor <= 50000) {
            sendPost.disabled = false;
          };
        });
        // final conteo caracteres CKEDITOR


      });

  });

})();





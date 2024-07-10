import { showToast } from "../../global/functios.js";

(() => {
  // al cargar la instancia de ckedit establecerle el tamaño y el idioma por default
  CKEDITOR.on('instanceReady', function () {
    // editor.config.font_defaultLabel = 'Monserrat';
    let editor = CKEDITOR.instances.ckeditor;
    editor.config.height = 150;
    editor.config.language = 'es';
  });

})();

(() => {
  // conteo de caracteres
  let charNumPost = document.getElementById("charNumPost");
  let sendPost = document.getElementById("sendPost");
  let maxChrs = 50000;

  let editor = CKEDITOR.instances.ckeditor;
  editor.on('instanceReady', function (event) {
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
      }

      charNumPost.innerText = `${numeroFormateado} / 50,000`;

      if (lenContentCkeditor > 50000) {
        charNumPost.innerText = `Máximo 50,000 caracteres, ingresados: ${numeroFormateado}`;
        charNumPost.style.color = 'red';
        sendPost.disabled = true;
      } else if (lenContentCkeditor <= 50000) {
        sendPost.disabled = false;
      }

    });
  });

})();

(() => {
  // manejar el botón de enviar post
  document.getElementById("sendPost").addEventListener("click", (e) => {
    // id ckeditor
    let type_post = `${document.getElementById("type_post").value}`.length; // int > 0
    let theme_category = `${document.getElementById("theme_category").value}`.length;
    let post_title = `${document.getElementById("post_title").value}`.length;
    let resume_post = `${document.getElementById("resume_post").value}`.length;
    let lenNewPost = `${CKEDITOR.instances.ckeditor.document.getBody().getText()}`.length; // int
    let inputFile = document.getElementById("uploadFile");
    let t = "error";
    let m;

    if (type_post == 0 || theme_category == 0 || post_title == 0 || resume_post == 0 || lenNewPost <= 1) {
      e.preventDefault();
      m = "<p>Revisar los campos vacíos, todos los campos son obligatorios.</p>"
      showToast(t, m);
    }
    if (inputFile.style.color == 'red') {
      e.preventDefault();
      m = "<p>Verificar que el tipo de archivo sea una extensión permitida o que no haya sido previamnete cargado.</p>";
      showToast(t, m);
    }
  });
})();

(() => {
  if (flashMsg) {
    showToast(flashMsg.type, flashMsg.message);
  }
})();

import { showToast, modalTitleAndBody } from '../../global/functios.js';

function delete_db(url) {
  fetch(url)
    .then(response => response.json())  // <-- Agregado .json() para obtener los datos JSON
    .then(data => {
      showToast(data.type, data.mensaje)
    })
    .catch(error => {
      showToast("error", `Ocurrio el siguiente error: ${error}`)
    });
}

(() => {
  let lstATagDel = document.querySelectorAll("a.delete");
  let mTitle;
  let mBody;
  let nombre;
  let url;
  let globalTr;

  lstATagDel.forEach(ele => {
    ele.addEventListener("click", () => {
      let tblSeccion = ele.getAttribute("categoria");

      let eleId = ele.id;
      if (tblSeccion == 'usuarios') {
        url = `${window.location.href}/del-usr/${eleId}`;
        nombre = document.getElementById(`usr_name_${eleId}`).innerText;
        mTitle = "Eliminación de Usuario";
        mBody = `<p>¿Deseas continuar con la eliminación del usuario?, también se borrarán todas las publicaciones hechas por: <br><b>${nombre}</b></p>`;
        globalTr = `tr_usr_${eleId}`;
      } else if (tblSeccion == 'administradores') {
        url = `${window.location.href}/del-adm/${eleId}`;
        nombre = document.getElementById(`nombre_adm_${eleId}`).innerText;
        mTitle = "Eliminación de Administrador";
        mBody = `<p>¿Deseas continuar con la eliminación del adminitrador?:<br><b>${nombre}</b></p>`;
        globalTr = `tr_adm_${eleId}`;
      } else if (tblSeccion == 'categorias') {
        url = `${window.location.href}/del-cat/${eleId}`;
        nombre = document.getElementById(`categoria_${eleId}`).innerText;
        mTitle = "Eliminación de Categoria";
        mBody = `<p>¿Deseas continuar con la eliminación de la categoria?, también se borrarán todas las publicaciones dentro de esa sección: <br><b>${nombre}</b></p>`;
        globalTr = `tr_cat_${eleId}`;
      } else if (tblSeccion == 'files') {
        // '/admin//<file_name>'
        nombre = document.getElementById(`files_${eleId}`).innerText;
        url = `${window.location.href}/delete-file/${nombre}`;
        mTitle = "Eliminación de Archivo";
        mBody = `<p>¿Deseas continuar con la eliminación del archivo?, el propietario recibira un email por la eliminación del documento: <br><b>${nombre}</b></p>`;
        globalTr = `tr_${eleId}`;
      }
      modalTitleAndBody(mTitle, mBody);
    });
  });

  btn_conf.addEventListener("click", () => {
    let delTr = document.getElementById(globalTr);
    delTr.remove();
    delTr.style.display = 'none';
    delete_db(url);
  });

})();
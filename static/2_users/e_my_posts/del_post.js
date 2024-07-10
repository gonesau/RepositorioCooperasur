import { showToast, modalTitleAndBody } from '../../global/functios.js';

let id_to_del, ttl_pst;

function borrar_post(id_post) {
  let cur_path = `${window.location.href}/del-post/${id_post}`;
  fetch(cur_path)
    .then(response => response.json())  // <-- Agregado .json() para obtener los datos JSON
    .then(data => {
      showToast(data.type, data.mensaje)
    })
    .catch(error => {
      let e = `Error al realizar la solicitud: ${error}`;
      showToast('error', e);
    });
}


(() => {
  // 1 \ 2 ) eliminar el post
  let btnDelPost = document.querySelectorAll("a.btn_del_post");
  btnDelPost.forEach(btn => {
    btn.addEventListener("click", () => {

      id_to_del = btn.id;

      ttl_pst = document.getElementById(`ttl_post_${btn.id}`).innerText;
      let cat_pst = document.getElementById(`cat_${btn.id}`).innerText;
      let tp_pst = document.getElementById(`tp_post_${btn.id}`).innerText;

      let bodyText = `<span>Deseas continuar con la eliminación de la publicación: <br>
      <b>Título:</b> ${ttl_pst} <br>
      <b>Categoria:</b> ${cat_pst} <br>
      <b>Tipo publicación: </b> ${tp_pst}
      </span>`;

      modalTitleAndBody("Confirmación de eliminación", bodyText);

    });
  });
})();

(() => {
  // 2 \ 2 ) confirmación de eliminar el post
  let btnConfDel = document.getElementById("btn_conf");
  btnConfDel.addEventListener("click", () => {
    borrar_post(id_to_del);
    document.querySelector('[data-dismiss="modal"]').click();
    let trToDel = `tr_${id_to_del}`;
    let tr = document.getElementById(trToDel);
    tr.style.display = 'none';
    tr.remove()
  });
})();
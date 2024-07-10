import { activateInputs, desactivarInputs } from '../../global/functios.js'

let lst_ids = ["name", "lastName", "country", "institution", "jobTitle"];


(() => {
  desactivarInputs(lst_ids);
})();

(() => {
  let chkEdit = document.getElementById("editDataChk");

  chkEdit.addEventListener("change", function () {
    if (chkEdit.checked) {
      activateInputs(lst_ids);
    } else {
      desactivarInputs(lst_ids);
    }
  });

})();
import { showToast } from '../../global/functios.js';

function IsSecurePassword(password) {
  const passwordRegex = /^(?=.*[!@#$%^&*(),.?":{}|<>])(?=.*\d)(?=.*[A-Z]).{10,}$/;
  if (passwordRegex.test(password)) {
    return true
  } else {
    return false
  }
}


function valInputPswd(iconNewPswd, inputPswd) {
  let ok = "bi-check-lg";
  let bad = "bi-x-lg";

  inputPswd.addEventListener("input", (e) => {
    let isSecure = IsSecurePassword(inputPswd.value);

    if (inputPswd.value.length > 0) {
      if (isSecure) {
        iconNewPswd.classList.remove(bad);
        iconNewPswd.classList.add("glyphicon", ok);
      } else {
        iconNewPswd.classList.remove(ok);
        iconNewPswd.classList.add("glyphicon", bad);
      }
    } else {
      iconNewPswd.classList.remove(ok);
      iconNewPswd.classList.remove(bad);
    }
  });
}

function enableBtnChngPwsd(inputPswdMain, inputPswdSecond, btnChangPswd) {
  inputPswdMain.addEventListener('keyup', e => {
    let statusP1 = IsSecurePassword(inputPswdMain.value);
    let statusP2 = IsSecurePassword(inputPswdSecond.value);
    if (statusP1 == true && statusP2 == true && inputPswdMain.value === inputPswdSecond.value) {
      btnChangPswd.disabled = false;
    } else {
      btnChangPswd.disabled = true;
    }
  });
}

(() => {
  let iNewPswd = document.getElementById("newPswd");
  let confNewPswd = document.getElementById("confNewPswd");
  let pswd1 = document.getElementById("pswd1");
  let pswd2 = document.getElementById("pswd2");
  let btnChgPswd = document.getElementById("btnCambiarContraseña");
  btnChgPswd.disabled = true;

  valInputPswd(iNewPswd, pswd1);
  valInputPswd(confNewPswd, pswd2);

  enableBtnChngPwsd(pswd1, pswd2, btnChgPswd);
  enableBtnChngPwsd(pswd2, pswd1, btnChgPswd);
})();
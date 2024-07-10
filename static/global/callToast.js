import { showToast } from '../global/functios.js';

(() => {
  if (flashMsg) {
    showToast(flashMsg.type, flashMsg.message)
  }
})();

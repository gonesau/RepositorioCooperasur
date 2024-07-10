
import { showToast, validate_file_to_upload } from "../../global/functios.js";

(async () => {
    let url = "/repo/np/nueva-publicacion/lst-files";
    try {
			let response = await fetch(url);
			let lst_previous_files_uploaded = await response.json();
			validate_file_to_upload("uploadFile", "sendEditedPost", lst_previous_files_uploaded);
    } catch (error) {
        console.error('Error al obtener la lista de archivos:', error);
    }
})();

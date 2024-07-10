function showToast(tipo, mensaje) {
  let position = {
    x: 'center',
    y: 'top',
  }
  const notyf = new Notyf({
    types: [
      {
        type: 'info',
        background: 'orange',
        icon: '<i class="bi bi-info-circle-fill"></i>',
        duration: 6000,
        position: position,
        dismissible: true,

      },
      {
        type: 'error',
        background: 'red',
        icon: '<i class="bi bi-exclamation-circle"></i>',
        duration: 6000,
        position: position,
        dismissible: true,

      },
      {
        type: 'success',
        background: 'green',
        icon: '<i class="bi bi-check2-circle"></i>',
        duration: 6000,
        position: position,
        dismissible: true,

      }
    ]
  });
  // notyf.open({
  // 	type: 'info',
  // 	message: mensaje
  // });
  notyf.open({
    type: tipo,
    message: mensaje
  });

}

// Uso de la función:
// showToast('success', 'Custom success text');
// showToast('error', 'Custom error text');
// showToast('warning', 'Custom warning text');
// showToast('info', 'Custom information text');


function modalTitleAndBody(textTitle, htmlBody) {
  let modalTitle = document.getElementById("modal-title");
  let modalBody = document.getElementById("modal-body");
  modalTitle.innerText = textTitle;
  modalBody.innerHTML = htmlBody;
}


function updateLabelChars(idTextAreaStr, idSpanNumberLenRes, intMaxLen) {
  $(document).ready(function () {
    $(`#${idTextAreaStr}`).keyup(function () {
      let len = $(this).val().length;
      let nLi = 71;
      let nLs = 90;
      let porcentajeLen = (len / intMaxLen) * 100;
      // actualizar número
      if (len >= intMaxLen) {
        $(`#${idSpanNumberLenRes}`).text(`Máximo ${intMaxLen} caracteres.`);
      } else {
        $(`#${idSpanNumberLenRes}`).text(len + ` / ${intMaxLen}`);
      };

      // actualizar color
      if (porcentajeLen < nLi) {
        $(`#${idSpanNumberLenRes}`).css('color', 'green');
      } else if (porcentajeLen > nLs) {
        $(`#${idSpanNumberLenRes}`).css('color', 'red');
      } else {
        $(`#${idSpanNumberLenRes}`).css('color', 'orange');
      };

    });
  });
}


function activateInputs(lst_ids) {
  let l = lst_ids.length;
  let i = 0;
  for (; i < l; i++) {
    document.getElementById(lst_ids[i]).value = dataUser[i];
    document.getElementById(lst_ids[i]).disabled = false;
  }
  document.getElementById("btnModData").disabled = false;
}

function desactivarInputs(lst_ids) {
  let l = lst_ids.length;
  let i = 0;
  for (; i < l; i++) {
    document.getElementById(lst_ids[i]).value = dataUser[i];
    document.getElementById(lst_ids[i]).disabled = true;
  }
  document.getElementById("btnModData").disabled = true;
}

// Función para agregar filtros a una tabla DataTable
function addDataTableFilters(tableId, tableCaptionTitle) {
  // info columns width mod: https://datatables.net/reference/option/columns.width
  // column auto width mod: https://datatables.net/extensions/fixedcolumns/examples/initialisation/size_fixed.html
  // Clonar la fila de encabezado y agregar la clase 'filters'
  $(`#${tableId} thead tr`)
    .clone(true)
    .addClass('filters')
    .appendTo(`#${tableId} thead`);

  // Obtener la tabla DataTable
  var table = $(`#${tableId}`).DataTable({
    fixedColumns: true,
    orderCellsTop: true,
    fixedHeader: true,
    pageLength: 10,
    caption: tableCaptionTitle,
    layout: {
      topStart: {
        buttons: ['csv', 'excel', 'pdf']
      }
    }
  });

  // Para cada columna
  table.columns().eq(0).each(function (colIdx) {
    // Obtener el título de la columna
    var title = $(`#${tableId} thead th`).eq(colIdx).text();

    // Agregar un input de texto al encabezado de la columna
    $(`#${tableId} thead .filters th`).eq(colIdx).html('<input class="form-control" type="text" placeholder="' + title + '" />');

    // Filtrar la columna en base al valor ingresado en el input
    $('input', $(`#${tableId} thead .filters th`).eq(colIdx)).on('keyup change', function () {
      table.column(colIdx).search(this.value).draw();
    });
  });
}



function validate_file_to_upload(str_id_file_input, str_id_btn_send_post, lst_previous_uploaded) {
  let fileInput = document.getElementById(str_id_file_input);
  let sendPost = document.getElementById(str_id_btn_send_post);
  let lst_allowed_ext = ['jpg', 'png', 'jpeg', 'xlsx', 'xls', 'pptx', 'odp', 'odt', 'docx', 'doc', 'zip', 'rar', 'pdf', 'txt', 'ods', 'csv'];

  fileInput.style.fontWeight = 'bold';
  // --------------------------------------------------
  // verificar si el archivo ya esta en la base de datos
  // --------------------------------------------------
  fileInput.addEventListener('change', function () {
    // const fileName = this.files[0].name;
    const fileName = this.files.length > 0 ? `${this.files[0].name}`.replace('(', '').replace(')', '').replace(' ', '_') : 'No se eligío ningun archivo';

    // si el archivo no esta en los docs, previamente cargados

    if (!lst_previous_uploaded.includes(fileName) && fileName != 'No se eligío ningun archivo') {
      // en caso de extensiones no válidas || extension no válida
      let fileExtension = fileName.split('.').pop().toLowerCase(); // ext archivo
      if (!lst_allowed_ext.includes(fileExtension) || fileName.length > 60 || fileInput.files[0].size > 52428800) {
        sendPost.disabled = true;
        fileInput.style.color = 'red';
        let m;

        if (fileInput.files[0].size > 52428800) {
          m = `<p>El archivo pesa más de 50 MB, favor de comprimir el archivo o en su defecto compartirlo a través de un enlace.</p>`;
        } else if (!lst_allowed_ext.includes(fileExtension)) {
          m = `<p>Archivo con extensión no permitida, verifica las "Caracteristicas del archivo".</p>`;
        } else if (fileName.length > 60) {
          m = `<p>Nombre de archivo muy largo, debe tener máximo de 60 caractéres.</p>`;
        }
        showToast('error', m);
      } else {
        fileInput.style.color = 'green';
        sendPost.disabled = false;
      }
    } else if (fileName === 'No se eligío ningun archivo') {
      fileInput.style.color = 'black';
      sendPost.disabled = false;

    } else {
      showToast('error', `Archivo cargado previamente en otra publicación, no se puede cargar nuevamente.<br>${fileName}`);
      fileInput.style.color = 'red';
      sendPost.disabled = true;
    }
  });

};


export { showToast, modalTitleAndBody, updateLabelChars, activateInputs, desactivarInputs, addDataTableFilters, validate_file_to_upload }
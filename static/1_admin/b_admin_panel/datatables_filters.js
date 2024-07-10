import { addDataTableFilters } from '../../global/functios.js';
// Llamar a la función para agregar filtros a cada tabla
$(document).ready(function () {
  addDataTableFilters("tblUsuarios", "Usuarios");
  addDataTableFilters("tbAdmins", "Administradores");
  addDataTableFilters("tbCategorias", "Categorias");
  addDataTableFilters("tbFiles", "Archivos");
});



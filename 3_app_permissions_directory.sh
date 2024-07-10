#!/bin/bash

# Verificar si el directorio existe
if [ -e '/var/www/cooperasur-app' ]; then
  echo "El directorio '/var/www/cooperasur-app' existe."

  # Verificar permisos
  if [ "$(stat -c '%U:%G' /var/www/cooperasur-app)" != "www-data:www-data" ] || [ "$(stat -c '%a' /var/www/cooperasur-app)" != "2775" ]; then
    # Cambiar propietario y permisos
    sudo chown -R www-data:www-data /var/www/cooperasur-app
    sudo chmod -R g+w /var/www/cooperasur-app
    echo "Se han cambiado los permisos en '/var/www/cooperasur-app'."
  else
    echo "Los permisos en '/var/www/cooperasur-app' ya son correctos."
  fi


  # Verificar permisos del directorio "static"
  if [ "$(stat -c '%U:%G' /var/www/cooperasur-app/static)" != "www-data:www-data" ] || [ "$(stat -c '%a' /var/www/cooperasur-app/static)" != "2775" ]; then
    # Cambiar propietario y permisos del directorio "static"
    sudo chown -R www-data:www-data /var/www/cooperasur-app/static
    sudo chmod -R g+w /var/www/cooperasur-app/static
    echo "Se han cambiado los permisos en '/var/www/cooperasur-app/static'."
  else
    echo "Los permisos en '/var/www/cooperasur-app/static' ya son correctos."
  fi



  # Reiniciar Apache
  sudo systemctl restart apache2
  echo "Apache se ha reiniciado."
else
  echo "El directorio '/var/www/cooperasur-app' no existe."
fi


# psql -h 127.0.0.1 -U postgres -a -f ./help_files/db_tables.sql

# eliminar la carpeta de uploads
uploads="static/uploads"

if [ -d "$uploads" ]; then
    rm -r "$uploads"
    if [ $? -eq 0 ]; then
        echo "Se ha eliminado la carpeta de uploads"
    else
        echo "No se pudo eliminar la carpeta de uploads"
    fi
else
    echo "No hay carpeta de uploads"
fi

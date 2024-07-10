venv="cooperasur-venv"

if [ -d "$venv" ]; then
		echo "El ambiente virtual si existe, se procede a activarlo.."
    source "$venv"/bin/activate
else
		echo "El entorno virtual no existe, se procede a crearlo:"
    python3 -m venv "$venv"
		echo "Se activa el ambiente virtual"
    source "$venv"/bin/activate
		echo "Se instalan las dependencias:"
		pip install -r requirements.txt
fi

code .
python main.py

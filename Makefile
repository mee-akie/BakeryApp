run-unix: virtualenv-unix
	python main.py

run-windows: virtualenv-windows
	python main.py

virtualenv-windows:
	tutorial-env\Scripts\activate.bat

virtualenv-unix:
	source tutorial-env/Scripts/activate
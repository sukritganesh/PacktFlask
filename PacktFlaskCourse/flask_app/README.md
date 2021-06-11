# DO ONLY ONCE
cd ../Sukrit Ganesh/Documents/LearningProgramming/Python/PacktFlaskCourse/flask_app

conda create --name packt_flask_env python=3.9

# DO EVERY TIME
cd ../Sukrit Ganesh/Documents/LearningProgramming/Python/PacktFlaskCourse/flask_app
conda activate packt_flask_env
set FLASK_DEBUG=1
flask run
conda deactivate
































# DO EVERY TIME
cd Python/PacktFlaskCourse/flask_app
py -m venv env
env\Scripts\activate
flask run
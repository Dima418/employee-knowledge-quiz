# EMPLOYEE KNOWLEDGE QIUZ 

## Usage

### Install

1. Clone this project from the GitHub repository on yor mashine:

        git clone https://github.com/Dima418/employee-knowledge-quiz.git

2. Change the working directory:

        cd employee-knowledge-quiz

### Run using Docker

1. Build an image:

        docker build -f "Dockerfile" -t employee_knowledge_quiz:latest .

2. Run the image, binding associated ports:

        docker run -p 8000:8000 employee_knowledge_quiz

### Run using local virtual environment

The script `envsetup.sh` will perform the following operations:

1. If no folders called `env`, `venv` or `virtualenv` exists, then  python venv folder called `venv` will be installed.

2. Activates virtal environment.

3. Installs required libraries from `requirements.txt` file.

Run script using one of the following:

-        ./envsetup.sh

-        sh envsetup.sh

-        bash envsetup.sh

## Services

Service     | Port | Usage
------------|------|------
Employee Knowladge Quiz      | 8000 | visit `http://localhost:8000` in your browser

---

#### Dmytro Dziubenko (2022)
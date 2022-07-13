# EMPLOYEE KNOWLEDGE QIUZ

## Usage

### Install

1. Clone this project from the GitHub repository on yor mashine:

        git clone https://github.com/Dima418/employee-knowledge-quiz.git

2. Change the working directory:

        cd employee-knowledge-quiz

### Run using Docker-compose

1. Run the docker-compose using:

        docker-compose up

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

Service                 | Port | Usage
------------------------|------|------
Employee Knowladge Quiz | 8000 | visit `http://localhost:8000` in your browser

## API endpoints

| Method 	| Endpoint               	| Description                                                        	|
|--------	|------------------------	|--------------------------------------------------------------------	|
| GET    	| /                      	| Root endpoint.                                                     	|
| POST   	| /signin                	| Signin.                                                            	|
| POST   	| /signup                	| Signup.                                                            	|
| GET    	| /users/                	| Get all users. Authentication required.                            	|
| PUT    	| /update/me             	| Update current user. Authentication required.                      	|
| DELETE 	| /user/{user_id}        	| Delete specific user. Authentication required.                     	|
| GET    	| /quiz/{quiz_id}/start  	| Get quiz`s questions and answer variants. Authentication required. 	|
| POST   	| /quiz/{quiz_id}/submit 	| Submit answers for the quiz. Authentication required.              	|

---

#### Dmytro Dziubenko (2022)
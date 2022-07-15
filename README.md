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

| Method 	| Endpoint               	| Description                                                        	                |
|---------------|-------------------------------|---------------------------------------------------------------------------------------|
| GET    	| /                      	| Root endpoint.                                                     	                |
| POST   	| /signin                	| Signin.                                                            	                |
| POST   	| /signup                	| Signup.                                                            	                |
| GET    	| /users/                	| Get all users. Authentication required.                            	                |
| PATCH    	| /update/me             	| Update current user. Authentication required.                      	                |
| PATCH    	| /update/{user_id}             | Update user superuser status. Authentication required. Superuser permision required   |
| DELETE 	| /user/{user_id}        	| Delete specific user. Authentication required. Superuser permision required           |
| GET    	| /quiz/{quiz_id}/view  	| Get quiz`s questions and answer variants. Authentication required. 	                |
| POST   	| /quiz/{quiz_id}/submit 	| Submit answers for the quiz. Authentication required.              	                |
| POST   	| /quiz	                        | Create a new quiz. Authentication required.  Superuser permision required             |
| GET   	| /quizzes                      | View all quizzes. Authentication required.  Superuser permision required              |
| GET   	| /quiz/{quiz_id}               | View the specific quiz. Authentication required.  Superuser permision required        |
| DELETE   	| /quiz/{quiz_id}               | Delete the specific quiz. Authentication required.  Superuser permision required      |
| PATCH   	| /quiz/{quiz_id}               | Update the specific quiz. Authentication required.  Superuser permision required      |
| POST   	| /question                     | Create a new question. Authentication required.  Superuser permision required         |
| GET   	| /questions                    | View all questions. Authentication required.  Superuser permision required            |
| GET   	| /question/{question_id}       | View the specific question. Authentication required.  Superuser permision required    |
| DELETE   	| /question/{question_id}       | Delete the specific question. Authentication required.  Superuser permision required  |
| PATCH   	| /question/{question_id}       | Update the specific question. Authentication required.  Superuser permision required  |
| POST   	| /category                     | Create a new category. Authentication required.  Superuser permision required         |
| GET   	| /categories                   | View all categories. Authentication required.  Superuser permision required           |
| GET   	| /category/{category_id}       | View the specific category. Authentication required.  Superuser permision required    |
| DELETE   	| /category/{category_id}       | Delete the specific category. Authentication required.  Superuser permision required  |
| PATCH   	| /category/{category_id}       | Update the specific category. Authentication required.  Superuser permision required  |
| POST   	| /answer                       | Create a new answer. Authentication required.  Superuser permision required           |
| GET   	| /answers                      | View all answers. Authentication required.  Superuser permision required              |
| GET   	| /answer/{answer_id}           | View the specific answer. Authentication required.  Superuser permision required      |
| DELETE   	| /answer/{answer_id}           | Delete the specific answer. Authentication required.  Superuser permision required    |
| PATCH   	| /answer/{answer_id}           | Update the specific answer. Authentication required.  Superuser permision required    |
| GET   	| /results                      | View all results. Authentication required.  Superuser permision required              |
| GET   	| /result/{result_id}           | View the specific result. Authentication required.  Superuser permision required      |
| DELETE   	| /result/{result_id}           | Delete the specific result. Authentication required.  Superuser permision required    |

---

#### Dmytro Dziubenko (2022)
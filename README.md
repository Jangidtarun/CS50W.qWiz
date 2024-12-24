# CS50W Final Project [ qWiz ]

## Project Description

This project is a dynamic quiz-taking platform where users can engage in quizzes on a variety of topics. Users have the freedom to choose a quiz based on their preferred topics from a vast, user-generated question bank. Any registered user can contribute questions to the platform, tagging them with specific topics for easy filtering, thus constantly enriching the quiz database.

### Key Features:

1. **Quiz Customization**: Users can select the number of questions and specific topics they want to focus on, allowing for a tailored quiz experience.
2. **Question Bank Contribution**: Users can contribute questions to the platform, and each question can be categorized by topics. This ensures that the quiz content is diverse, up-to-date, and community-driven.
3. **Instant Quiz Mode**: For those looking for a faster, more gamified experience, the "Instant Quiz" mode challenges users with a timed, rapid-fire quiz where one question is presented at a time, enhancing engagement through a game-like format.
4. **Discussion Panel**: Each question features a discussion panel where users can engage in meaningful conversations, clarifications, or debates about the question's topic or answer. This fosters a community of learning and shared knowledge.
5. **Voting System**: Users can vote on the quality and relevance of questions. High-quality questions receive more visibility, while poor or outdated questions can be flagged by the community.
6. **Responsive Design**: The platform is mobile-friendly, ensuring users can take quizzes or contribute on any device, be it a phone, tablet, or desktop.

This web application not only enhances the quiz-taking experience with personalized options and gamified features but also cultivates an interactive community where users are actively engaged in both creating and discussing quiz content.

## Distinctiveness and Complexity

### Why This Project is Distinct and Complex

This project stands out from other web applications due to its unique approach to personalized learning and its community-driven, gamified quiz experience. Unlike a typical social network or e-commerce site, this platform is designed to provide a versatile and engaging learning environment through user-generated quizzes, real-time interactions, and community discussions.

### Unique Use Case

This platform serves a distinctive purpose by combining personalized quiz experiences with community collaboration. Users can not only take quizzes based on their selected topics but also actively contribute to the platform’s question bank, making it an ever-growing resource for learners. The "Instant Quiz" mode adds a gamified twist to traditional quizzes, providing an interactive, fast-paced quiz-taking experience that heightens user engagement. The discussion panels attached to each question foster a sense of community where users can debate or clarify answers, enhancing the overall learning experience.

### Complex Features

- **Question Bank Creation**: One of the key complexities is the ability for users to contribute to the platform by submitting their own questions. Each question is categorized by topics, allowing for dynamic filtering and search options. Users can customize their quiz by selecting the number of questions and the topics they wish to focus on, creating an adaptable and flexible quiz experience.

- **Voting and Discussion System**: The platform includes an advanced voting system where users can upvote or downvote questions based on their relevance and quality. Additionally, the discussion panel allows users to engage in threaded conversations for each question, promoting a collaborative and interactive learning environment.

- **Instant Quiz Mode**: The "Instant Quiz" feature presents quizzes in a gamified format where users answer one question at a time under a time constraint, adding complexity in terms of user interaction, time management, and dynamic content display.

### Innovative Design

The user interface is designed to provide a seamless experience across devices with mobile responsiveness as a core focus. The layout and design ensure ease of use, with intuitive filtering options for quizzes, a real-time timer in the instant quiz mode, and smooth navigation across different sections such as the question bank, discussions, and user profiles. The voting and discussion system also gives the platform a social, interactive aspect that adds depth to the quiz experience.

### Technical Complexity

This application incorporates multiple layers of technical complexity, from back-end model design to front-end interactivity:

- **Django Models**: The application features complex relational models to manage user-contributed questions, votes, quiz attempts, and user interactions. Topics are associated with questions, and each quiz is dynamically generated based on user inputs such as the number of questions and chosen topics.

- **Real-time Interactivity with JavaScript**: The front-end is enhanced using JavaScript to manage dynamic content updates, such as real-time quiz timers, question navigation, and instant feedback. The discussion panel uses JavaScript for loading new comments without refreshing the page, providing a smooth user experience.

- **Advanced Querying**: Complex queries are used to efficiently retrieve user-selected questions based on topics and other filters. Additionally, the voting and rating system involves real-time data updates, requiring synchronization between the front-end and back-end.

- **Gamification**: The instant quiz mode adds an extra layer of complexity, as it requires real-time tracking of user progress, a countdown timer, and seamless transitions between questions.

## Technologies Used

- **Back-end**: Django 5.1.1
- **Front-end**: JavaScript
- **Database**: SQLite
- **Additional Tools**: Bootstrap Icons and pillow

## Project Structure

### Directory Layout

Provide a clear outline of your project's directory structure, explaining the purpose of each folder/file. For example:

```
.
|-- README.md
|-- db.sqlite3
|-- manage.py
|-- media
|   |-- key.png
|   `-- photos
|-- quiz
|   |-- __init__.py
|   |-- __pycache__
|   |-- admin.py
|   |-- apps.py
|   |-- migrations
|   |-- models.py
|   |-- static/
|   |   |-- js
|   |   |   |-- emailverify.js
|   |   |   |-- instant.js
|   |   |   |-- link-theme-setter.js
|   |   |   |-- profile.js
|   |   |   |-- question.js
|   |   |   |-- sidebar.js
|   |   |   |-- theme.js
|   |   |   `-- tmp-instant.js
|   |   |-- styles
|   |   |   |-- mstyle.css
|   |   |   |-- mstyle.css.map
|   |   |   `-- mstyle.scss
|   |-- templates/
|   |   |-- base.html
|   |   |-- create.html
|   |   |-- createtemplate.html
|   |   |-- edit.html
|   |   |-- index.html
|   |   |-- indextemplate.html
|   |   |-- instantquiz.html
|   |   |-- login.html
|   |   |-- profile.html
|   |   |-- question.html
|   |   |-- questionswtopic.html
|   |   |-- quiz.html
|   |   |-- quiz_finished.html
|   |   |-- register.html
|   |   |-- resetpassword.html
|   |   |-- results.html
|   |   |-- search_results.html
|   |   |-- sendresetlink.html
|   |   |-- tags.html
|   |   |-- take.html
|   |   |-- tree.txt
`   `   `-- view_profile.html
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- requirements.txt
`-- xp
    |-- __init__.py
    |-- __pycache__
    |-- asgi.py
    |-- settings.py
    |-- urls.py
    `-- wsgi.py

```

### File Contents

- **models.py**:

  The `models.py` file defines the database schema for a quiz application using Django. It includes ten models: `User`, `Question`, `Topic`, `Vote`, `View`, `Choice`, `Result`, `UserAnswer`, `Quiz`, and `Comment`. The `User` model extends the default `AbstractUser` model, adding fields for the user's profile picture, bio, and a Many-to-Many relationship with `Topic` for user interests. The `Question` model contains fields for the question text, points, and an associated author, along with a Many-to-Many relationship to `Topic` for categorizing questions.

  The `Topic` model allows for the organization of questions into various topics. The `Vote` model captures user interactions with questions, enabling users to upvote or downvote questions and ensuring that each user can only vote once per question. The `Comment` model facilitates discussion by allowing users to comment on questions, associating comments with both the user and the question. Then there's `Choice` model that store an answer [correct or incorrect] for a `Question`. The `Quiz` model keeps track that after submitting a quiz user cannot submit the same quiz again. `Result` as its name store the results for a particular quiz and the `UserAnswer` model store that in some quiz a user selected some answer for some question. Together, these models create a comprehensive structure for managing users, questions, topics, votes, answers, results and comments within the quiz application.

# `views.py` - Documentation

## Imports:

- `django.core.cache.cache`: Manages caching for optimizing view performance.
- `django.http`: Provides classes for creating HTTP responses like `HttpResponseForbidden` and `HttpResponseBadRequest`.
- `django.views.decorators.http.require_http_methods`: Restricts views to specific HTTP methods.
- `random`, `json`: Standard libraries for random sampling and JSON handling.
- `django.shortcuts`: Provides shortcuts for common tasks like rendering templates, redirecting, and retrieving objects.
- `django.contrib.auth`: Manages user authentication, login, logout, and user sessions.
- `rest_framework`: Used for building RESTful APIs and handling API responses.
- `django.core.mail`: Sends emails for functionalities like password resets.
- `django.db.models.Q`: Allows complex query filtering using OR and AND conditions.
- `django.core.paginator.Paginator`: Implements pagination for lists of data.

## Views:

### `index(request)`

Displays a paginated list of all questions, ordered by creation date.

- **Request Type**: `GET`
- **Template**: `quiz/index.html`
- **Pagination**: 18 questions per page.

### `search(request)`

Handles search functionality for questions.

- **Request Type**: `GET`
- **Query Parameters**:
  - `q`: Search term (query string).
- **Search Fields**: `body`, `created_by__username`, `topics__name`.
- **Template**: `quiz/search_results.html`
- **Pagination**: 18 results per page.

### `delete_comment(request, cid)`

Deletes a comment by its ID.

- **Request Type**: `DELETE`
- **Parameter**: `cid` (comment ID).
- **Response**: 204 status on successful deletion.

### `gotoinstantquiz(request)`

Initializes an instant quiz session by resetting used questions.

- **Request Type**: `GET`
- **Template**: `quiz/instantquiz.html`

### `handle_topics(topicslist, user)`

Processes a comma-separated list of topics, creates new topics if they don't exist, and returns a list of `Topic` objects.

- **Parameters**:
  - `topicslist`: Comma-separated topic names.
  - `user`: User creating the topics.

### `create(request)`

Creates a new question with options and associated topics.

- **Request Type**: `GET` / `POST`
- **Template**: `quiz/create.html`
- **Validation**: Ensures topics and options are provided.

### `edit(request, pk)`

Allows users to edit an existing question.

- **Request Type**: `GET` / `POST`
- **Parameters**: `pk` (question ID).
- **Template**: `quiz/edit.html`
- **Validation**: Ensures topics and options are provided.

### `update_vote(request, qid)`

Updates a user's vote for a question.

- **Request Type**: `PUT`
- **Parameters**: `qid` (question ID).
- **Response**: JSON with updated vote count.

### `topics(request)`

Displays all topics and allows users to create new ones.

- **Request Type**: `GET` / `POST`
- **Template**: `quiz/tags.html`
- **Pagination**: 50 topics per page.

### `delete_topic(request, topic_id)`

Deletes a topic if the request user is the creator.

- **Request Type**: `GET`
- **Parameters**: `topic_id` (topic ID).

### `delete_question(request, pk)`

Deletes a question if the request user is the creator.

- **Request Type**: `GET`
- **Parameters**: `pk` (question ID).

### `make_comment(request)`

Creates a new comment for a question.

- **Request Type**: `POST`
- **Validation**: Requires non-empty comment body and question ID.

### `question_with_topic(request, topicname)`

Displays questions filtered by a specific topic.

- **Request Type**: `GET`
- **Template**: `quiz/questionswtopic.html`
- **Pagination**: 18 questions per page.

### `question(request, pk)`

Displays the details of a specific question and its comments.

- **Request Type**: `GET`
- **Parameters**: `pk` (question ID).
- **Template**: `quiz/question.html`
- **Handles**: Question views, comments, and voting status.

### `take_quiz(request)`

Allows users to initiate a quiz with specified number of questions and topics.

- **Request Type**: `GET` / `POST`
- **Template**: `quiz/take.html`
- **Logic**: Retrieves questions randomly or by selected topics.

### `take_quiz_helper(request, qid)`

Handles the process of displaying quiz questions and choices.

- **Request Type**: `GET`
- **Parameters**: `qid` (quiz ID).
- **Template**: `quiz/quiz.html`
- **Logic**: Shuffles question choices for each quiz.

### `quiz_submit(request)`

Submits a user's quiz attempt and calculates the score.

- **Request Type**: `POST`
- **Template**: Redirects to `showresults` upon completion.
- **Validation**: Ensures the user has not already completed the quiz.

### `showresults(request, rid)`

Displays the results of a completed quiz attempt.

- **Request Type**: `GET`
- **Parameters**: `rid` (result ID).
- **Template**: `quiz/results.html`

### `view_profile`

- **View:** `view_profile(request, pid)`
- **Description**: Fetches and displays the profile of a user specified by `pid` (profile ID). It includes the questions created by the user and the topics related to those questions. Uses pagination for the list of questions.

- **Parameters:**

  - `request`: The HTTP request object.
  - `pid`: ID of the user whose profile is being viewed.

- **Returns:**
  - Renders `quiz/view_profile.html` with the user's details, a paginated list of questions, and distinct topics.

### `profile`

**View:** `profile(request)`

**Description:**
Handles the display of the user's profile page. If a POST request is received, it updates the profile photo.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Renders `quiz/profile.html`.

### `update_profile_photo`

**View:** `update_profile_photo(request)`

**Description:**
Updates the profile photo of the logged-in user if an image is uploaded.

**Parameters:**

- `request`: The HTTP request object containing the uploaded image.

**Returns:**

- Redirects to the `profile` view on successful update, or re-renders with an error message if no file is uploaded.

### `remove_photo`

**View:** `remove_photo(request)`

**Description:**
Removes the user's profile photo and sets it back to a default image.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Redirects to the `profile` view after updating the photo.

### `login_user`

**View:** `login_user(request)`

**Description:**
Displays the login page or processes a login request.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Renders `quiz/login.html` or redirects to `index` upon successful login.

### `handle_login`

**View:** `handle_login(request)`

**Description:**
Processes the login credentials and logs in the user if valid.

**Parameters:**

- `request`: The HTTP request object containing login data.

**Returns:**

- Redirects to `index` on successful login, or re-renders the login page with an error message.

### `register`

**View:** `register(request)`

**Description:**
Displays the registration page or processes a registration request.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Renders `quiz/register.html` or redirects to `index` upon successful registration.

### `handle_registration`

**View:** `handle_registration(request)`

**Description:**
Handles user registration, creates a new user, and logs them in.

**Parameters:**

- `request`: The HTTP request object containing registration data.

**Returns:**

- Redirects to `index` on successful registration or re-renders with an error message if the username is taken.

### `update_user`

**View:** `update_user(request)`

**Description:**
Updates the logged-in user's profile details.

**Parameters:**

- `request`: The HTTP request object containing profile update data.

**Returns:**

- Redirects to `view_profile` on success or re-renders with an error message.

### `handle_user_update`

**View:** `handle_user_update(request)`

**Description:**
Handles updates to a user's profile, including name, email, and bio.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Redirects to `view_profile` on success or re-renders with an error message.

### `delete_user`

**View:** `delete_user(request)`

**Description:**
Deletes the account of the logged-in user.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Redirects to `login_user` after deleting the user account.

### `logout_user`

**View:** `logout_user(request)`

**Description:**
Logs out the current user.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Redirects to the login page.

### `send_otp`

**View:** `send_otp(request, email_id)`

**Description:**
Sends an OTP to the specified email for verification.

**Parameters:**

- `request`: The HTTP request object.
- `email_id`: The email address to which the OTP is sent.

**Returns:**

- A JSON response indicating successful OTP sending.

### `verify_otp`

**View:** `verify_otp(request, email_id, otp)`

**Description:**
Verifies the OTP entered by the user against the stored OTP.

**Parameters:**

- `request`: The HTTP request object.
- `email_id`: The email address used for OTP verification.
- `otp`: The OTP entered by the user.

**Returns:**

- A JSON response indicating if the verification was successful.

### `send_reset_link`

**View:** `send_reset_link(request)`

**Description:**
Handles password reset link requests, generating and sending a reset link to the user's email.

**Parameters:**

- `request`: The HTTP request object.

**Returns:**

- Renders `quiz/sendresetlink.html` with a message indicating the reset link was sent.

### `handle_send_reset_link`

**View:** `handle_send_reset_link(request)`

**Description:**
Sends a password reset link to the specified email if it is associated with an existing user.

**Parameters:**

- `request`: The HTTP request object containing the email.

**Returns:**

- Renders `quiz/sendresetlink.html` with a message about the reset link.

### `reset_password`

**View:** `reset_password(request, uid, token)`

**Description:**
Displays the password reset form or processes the password reset.

**Parameters:**

- `request`: The HTTP request object.
- `uid`: The encoded user ID.
- `token`: The token for password reset verification.

**Returns:**

- Renders `quiz/resetpassword.html` or processes the password reset.

### `handle_reset_password`

**View:** `handle_reset_password(request, uid, token)`

**Description:**
Handles the logic for resetting the user's password.

**Parameters:**

- `request`: The HTTP request object.
- `uid`: The encoded user ID.
- `token`: The token for password reset verification.

**Returns:**

- Redirects or re-renders based on the reset status.

- **serializers.py**:

  The `serializers.py` file in this project defines two serializers: `ChoiceSerializer` and `QuestionSerializer`. The `ChoiceSerializer` is responsible for serializing and deserializing `Choice` model instances, ensuring that all fields are included. Similarly, the `QuestionSerializer` manages the `Question` model, allowing for full representation of the model's data. These serializers are essential for converting complex data types into JSON format for API responses and for validating incoming data during creation or updates.

## How to Run the Application

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Jangidtarun/nrepo.git capstone_tarun
   cd capstone_tarun
   ```

2. **Install Dependencies**:
   Make sure you have Python and pip installed. Then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   Apply database migrations using:

   ```bash
   python manage.py migrate
   ```

4. **Start the Development Server**:
   Run the server with:

   ```bash
   python manage.py runserver
   ```

5. **Access the Application**:
   Open a web browser and go to `http://127.0.0.1:8000` or `localhost:8000` to view the application.

## Additional Information

### Areas for Future Improvement

Future enhancements could include implementing user roles with distinct permissions, enabling a richer user experience with features such as bookmarks for favorite quizzes and enhanced analytics on quiz performance. Additionally, incorporating machine learning algorithms to suggest quizzes based on user preferences could greatly improve engagement. The interface could benefit from further usability testing to refine the user experience based on real user feedback.

### Relevant Documentation

For more information on Django REST Framework and building APIs, the official documentation is an excellent resource: [Django REST Framework](https://www.django-rest-framework.org/) Documentation. For best practices on building serializers, you can refer to the section on [Serializers](https://www.django-rest-framework.org/api-guide/serializers/#serializers).

### Resources

- [Bootstrap Icons](https://icons.getbootstrap.com/)
- [Google's JetBrain Mono font](https://fonts.google.com/specimen/JetBrains+Mono?query=jet)
- [Google's Inter font](https://fonts.google.com/specimen/Inter?query=inter)

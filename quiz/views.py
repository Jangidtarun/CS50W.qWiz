from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
import random, json
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .models import User, Question, Choice, Result, Comment, Topic, Vote, View, UserAnswer, Quiz
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Index view with pagination for questions
def index(request):
    questions = Question.objects.order_by('-created')
    page_obj = Paginator(questions, 18).get_page(request.GET.get('page'))

    return render(request, 'quiz/index.html', {
        'questions': page_obj,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    message = ''
    questions = Question.objects.all()

    if query:
        # Process query to search across multiple fields
        query_words = [word.strip() for word in query.replace(',', ' ').split()]
        q_objects = Q()

        # Add Q filters for each word in multiple fields
        for word in query_words:
            q_objects |= (Q(body__icontains=word) |
                          Q(created_by__username__icontains=word) |
                          Q(topics__name__icontains=word))

        questions = questions.filter(q_objects).distinct()
        message = f'{questions.count()} results found'

    # Paginate results
    page_obj = Paginator(questions, 18).get_page(request.GET.get('page'))
    return render(request, 'quiz/search_results.html', {
        'questions': page_obj,
        'query': query,
        'message': message,
    })


# Delete comment by ID (uses DRF for a simple API response)
@api_view(['DELETE'])
def delete_comment(request, cid):
    comment = get_object_or_404(Comment, pk=cid)
    comment.delete()
    return Response('Deleted successfully', status=204)


# Initialize instant quiz session (clears used questions)
def gotoinstantquiz(request):
    request.session['used_questions'] = []
    return render(request, 'quiz/instantquiz.html')



def handle_topics(topicslist, user):
    """
    Helper function to process topics: split by comma, strip, and create new if not existing.
    """
    topic_names = [name.strip() for name in topicslist.split(',') if name.strip()]
    topics = []
    for name in topic_names:
        if name != 'random':
            try:
                topic = Topic.objects.get(name=name)
            except Topic.DoesNotExist:
                topic = Topic.objects.create(name=name, created_by=user)
            topics.append(topic)
    return topics


def create(request):
    if not request.user.is_authenticated:
        return redirect(login_user)

    if request.method == 'POST':
        body = request.POST['question'].strip()
        points = int(request.POST['points'])
        options = [request.POST[f'option{i+1}'].strip() for i in range(4)]
        topicslist = request.POST['taglist'].strip()

        if not topicslist:
            return render(request, 'quiz/create.html', {'err_message': 'Please mention topics'})

        try:
            # Create question and add topics
            new_question = Question.objects.create(
                body=body, points=points, created_by=request.user
            )
            new_question.topics.set(handle_topics(topicslist, request.user))
            new_question.save()

            # Create choices in bulk
            choices = [Choice(question=new_question, body=opt, is_correct=(i == 0))
                       for i, opt in enumerate(options)]
            Choice.objects.bulk_create(choices)

            return render(request, 'quiz/create.html', {'message': 'Created successfully'})

        except Exception as e:
            return render(request, 'quiz/create.html', {'err_message': str(e)})

    return render(request, 'quiz/create.html')


def edit(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        body = request.POST['question'].strip()
        points = int(request.POST['points'])
        options = [request.POST[f'option{i+1}'].strip() for i in range(4)]
        topicslist = request.POST['taglist'].strip()

        if not topicslist:
            return render(request, 'quiz/edit.html', {'err_message': 'Please mention topics', 'question': question})

        try:
            # Update question details and topics
            question.body = body
            question.points = points
            question.topics.set(handle_topics(topicslist, request.user))
            question.save()

            # Update choices directly or add new ones if needed
            existing_choices = list(question.options.all())
            for i, option in enumerate(options):
                if i < len(existing_choices):
                    existing_choices[i].body = option
                    existing_choices[i].is_correct = (i == 0)
                    existing_choices[i].save()
                else:
                    Choice.objects.create(question=question, body=option, is_correct=(i == 0))

            return redirect('index')

        except Exception as e:
            return render(request, 'quiz/edit.html', {'err_message': str(e), 'question': question})

    topic_list = ', '.join(topic.name for topic in question.topics.all())
    return render(request, 'quiz/edit.html', {
        'question': question,
        'topiclist': topic_list,
    })


@require_http_methods(["PUT"])
def update_vote(request, qid):
    data = json.loads(request.body)
    votechange = data.get('votechange')

    if votechange not in [1, -1]:
        return JsonResponse({'error': 'Invalid vote value'}, status=400)

    question = get_object_or_404(Question, pk=qid)
    user = request.user

    # Retrieve or create the vote
    vote, created = Vote.objects.get_or_create(question=question, user=user, defaults={'voteval': votechange})

    # Update the vote value if it was not newly created
    if not created:
        vote.voteval = votechange
        vote.save()

    # Calculate the new vote count
    new_vote_count = question.votes.filter(voteval=1).count() - question.votes.filter(voteval=-1).count()

    return JsonResponse({
        'message': 'Vote count updated successfully!',
        'new_vote_count': new_vote_count
    }, status=200)


@login_required
def topics(request):
    # Fetch all topics, ordered alphabetically
    topics = Topic.objects.all().order_by('name')
    paginator = Paginator(topics, 50)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # Handle topic creation through a POST request
    if request.method == 'POST':
        name = request.POST['name'].strip()
        if name:
            if not Topic.objects.filter(name=name).exists():
                Topic.objects.create(name=name, created_by=request.user)
                return redirect('topics')
            else:
                err_message = 'This topic already exists'
        else:
            err_message = 'Topic name cannot be empty'

        return render(request, 'quiz/tags.html', {
            'tags': page_obj,
            'err_message': err_message
        })

    # Render the template for GET requests
    return render(request, 'quiz/tags.html', {
        'tags': page_obj
    })


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.user == topic.created_by:
        topic.delete()
        return redirect(view_profile, request.user.pk)
    else:
        return HttpResponseForbidden('You are not allowed to delete this topic.')


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # Check if the user is the creator of the question
    if request.user == question.created_by:
        question.delete()
        return redirect(view_profile, request.user.pk)
    else:
        return HttpResponseForbidden('You are not allowed to delete this question.')


@login_required
def make_comment(request):
    if request.method == 'POST':
        body = request.POST.get('comment', '').strip()
        question_id = request.POST.get('qid')

        # Ensure both comment body and question ID are provided
        if not body or not question_id:
            return HttpResponseBadRequest('Comment body and question ID are required.')

        # Retrieve the question and create the comment
        try:
            question = get_object_or_404(Question, pk=question_id)
            new_comment = Comment.objects.create(
                question=question,
                body=body,
                user=request.user
            )
            new_comment.save()

            return redirect('question', pk=question_id)
        except Exception as e:
            print(f'Error creating comment: {e}')
            return redirect('get-question', pk=question.pk)

    # If not a POST request, return a bad request response
    return HttpResponseBadRequest('Invalid request method.')


def question_with_topic(request, topicname):
    # Retrieve the topic or return a 404 if not found
    topic = get_object_or_404(Topic, name=topicname)

    # Filter questions by the topic
    questions = Question.objects.filter(topics=topic).order_by('-created')

    # Set up pagination with 18 questions per page
    paginator = Paginator(questions, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with the questions and topics
    return render(request, 'quiz/questionswtopic.html', {
        'questions': page_obj,
        'topics': Topic.objects.all().order_by('name'),
        'topic': topicname,
    })


def question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # Handle views for the question
    if request.user.is_authenticated:
        View.objects.get_or_create(question=question, user=request.user)

    # Fetch comments related to the question
    comments = question.qcomments.all().order_by('-created')

    # Calculate the current vote count
    newvote = question.votes.filter(voteval=1).count() - question.votes.filter(voteval=-1).count()

    # Initialize context dictionary
    context = {
        'question': question,
        'comments': comments,
        'votes': newvote,
    }

    # Check if the user has voted on this question
    if request.user.is_authenticated:
        try:
            vote = Vote.objects.get(user=request.user, question=question)
            context['showdownvote'] = vote.voteval == 1
        except Vote.DoesNotExist:
            context['showboth'] = True

    return render(request, 'quiz/question.html', context)


def take_quiz(request):
    if request.method == 'POST':
        noq = int(request.POST['noq'])
        tag_string = request.POST['taglist']

        # Extract and clean topic tags
        tags = [tag.strip() for tag in tag_string.split(',')]

        # Get questions based on topics or select random questions
        if 'random' in tags:
            questions = Question.objects.all()
        else:
            try:
                topics = [Topic.objects.get(name=tag) for tag in tags]
            except Topic.DoesNotExist:
                return render(request, 'quiz/take.html', {
                    'err_message': 'One or more selected topics do not exist'
                })

            questions = Question.objects.filter(topics__in=topics).distinct()

        # Limit questions to the number of questions requested
        noq = min(noq, questions.count())
        questions = random.sample(list(questions), noq)

        # Create a new Quiz instance if no finished quiz exists
        quiz = Quiz.objects.create(user=request.user)
        quiz.questions.set(questions)
        quiz.save()

        return redirect(take_quiz_helper, qid=quiz.pk)

    return render(request, 'quiz/take.html')


def take_quiz_helper(request, qid):
    # Prepare quiz data for rendering
    quiz = get_object_or_404(Quiz, pk=qid)

    if quiz.is_finished:
        return render(request, 'quiz/quiz_finished.html', {
            'message': 'You have already finished this quiz',
        })

    total_score = sum(q.points for q in quiz.questions.all())

    quiz_data = []
    for q in quiz.questions.all():
        choices = list(q.options.all())  # Get all choices for the question
        random.shuffle(choices)           # Shuffle the choices in place
        quiz_data.append({'question': q, 'choices': choices})  # Add the randomized choices to the quiz data

    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'quiz_data': quiz_data,
        'total_score': total_score
    })


def quiz_submit(request):
    if request.method == 'POST':
        qns = request.POST.getlist('questions')
        questions = []
        total_score = 0
        obtained_score = 0
        optionlist = []

        for id in qns:
            prompt = f'option-{id}'
            question = get_object_or_404(Question, pk=id)
            questions.append(question)
            total_score += question.points
            option_id = request.POST.get(prompt)
            if option_id:
                selected_option = get_object_or_404(Choice, pk=option_id)
                optionlist.append(selected_option)
                if selected_option.is_correct:
                    obtained_score += question.points


        if request.user.is_authenticated:
            # Associate the quiz with the user
            quiz = get_object_or_404(Quiz, pk=request.POST.get('quiz_id'))
            if quiz.is_finished:
                return render(request, 'quiz/quiz_finished.html', {
                    'message': 'You have already finished this quiz',
                })
            quiz.user = request.user
            quiz.is_finished = True
            quiz.save()

            result = Result.objects.create(
                quiz = quiz,
                total_score=total_score,
                obtained_score=obtained_score,
            )

            for qn, op in zip(questions, optionlist):
                result.questions.add(qn)
                UserAnswer.objects.create(
                    question=qn,
                    user=request.user,
                    result=result,
                    selected_option=op,
                )

        return redirect(showresults, rid=result.pk)

    return redirect(index)


def showresults(request, rid):
    # Fetch the result object for the provided rid
    result = get_object_or_404(Result, pk=rid)

    if request.user.is_authenticated:
        # Check if the result belongs to the authenticated user
        if result.quiz.user != request.user:
            return redirect(index)  # Redirect if the user does not own the result

    total_score = result.total_score
    obtained_score = result.obtained_score
    # Render the results template with the scores and result object
    return render(request, 'quiz/results.html', {
        'total_score': total_score,
        'obtained_score': obtained_score,
        'result': result,
    })


def view_profile(request, pid):
    user = get_object_or_404(User, pk=pid)
    questions = Question.objects.filter(created_by=user).order_by('-updated')
    # Get distinct topics created by the user or where the questions are created by the user
    topics = Topic.objects.filter(
        Q(created_by=user) | Q(question__created_by=user)
    ).distinct()

    paginator = Paginator(questions, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'quiz/view_profile.html', {
        'cuser': user,
        'questions': page_obj,
        'topics': topics,
    })


def profile(request):
    if request.method == 'POST':
        return update_profile_photo(request)
    return render(request, 'quiz/profile.html')


def update_profile_photo(request):
    input_files = request.FILES.get('nprofile-img')
    if input_files:
        user = request.user
        user.photo = input_files
        user.save()
        return redirect(profile)
    return render(request, 'quiz/profile.html', {
        'err_message': 'No file uploaded.'
    })


def remove_photo(request):
    user = request.user
    user.photo = 'key.png'
    user.save()
    return redirect(profile)


def login_user(request):
    if request.method == "POST":
        return handle_login(request)
    return render(request, "quiz/login.html")


def handle_login(request):
    username = request.POST["username"].strip()
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect("index")
    return render(request, "quiz/login.html", {
        "err_message": "Invalid username or password",
    })


def register(request):
    if request.method == "POST":
        return handle_registration(request)
    return render(request, "quiz/register.html")


def handle_registration(request):
    username = request.POST["username"].strip()
    password = request.POST["password"]
    firstname = request.POST['firstname'].strip()
    lastname = request.POST['lastname'].strip()
    email = request.POST['email'].strip()

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=firstname,
            last_name=lastname,
            email=email
        )
        user.save()
        login(request, user)
        return redirect("index")
    except IntegrityError:
        return render(request, "quiz/register.html", {
            "err_message": "Username already taken."
        })


def update_user(request):
    if request.method == "POST":
        return handle_user_update(request)
    return render(request, "quiz/profile.html")


def handle_user_update(request):
    user = request.user
    user.first_name = request.POST['firstname'].strip()
    user.last_name = request.POST['lastname'].strip()
    user.email = request.POST['email'].strip()
    user.about = request.POST['about'].strip()

    try:
        user.save()
        return redirect(view_profile, request.user.pk)
    except Exception as e:
        return render(request, "quiz/profile.html", {
            "err_message": str(e)
        })


def delete_user(request):
    user = request.user
    user.delete()
    return redirect(login_user)


def logout_user(request):
    logout(request)
    return redirect("login")


@api_view(['GET'])
def send_otp(request, email_id):
    otp = random.randint(1000, 9999)
    subject = 'Your OTP for Verification'
    message = f'Your OTP is {otp}. Please enter this to verify your email address.'
    from_email = 'tarunjangid19102002@gmail.com'

    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[email_id])
    cache.set(email_id, otp, timeout=300)
    return Response({'message': 'OTP sent successfully'})


@api_view(['GET'])
def verify_otp(request, email_id, otp):
    user_otp = int(otp)
    actual_otp = cache.get(email_id)
    is_verified = actual_otp and user_otp == actual_otp
    message = 'Verification successful' if is_verified else 'OTP is incorrect'
    return Response({'message': message, 'pass': is_verified})


def send_reset_link(request):
    if request.method == 'POST':
        return handle_send_reset_link(request)
    return render(request, 'quiz/sendresetlink.html')


def handle_send_reset_link(request):
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(
            reverse('reset_password', kwargs={'uid': uid, 'token': token})
        )

        subject = 'Password Reset Request'
        message = f'Click the link below to reset your password:\n{reset_link}'
        from_email = 'tarunjangid19102002@gmail.com'
        send_mail(subject, message, from_email, [email])

        return render(request, 'quiz/sendresetlink.html', {
            'message': 'If this email is registered with an account, you will receive an email with a link to reset your password.'
        })

    except User.DoesNotExist:
        # Do not reveal whether the email exists for security reasons.
        return render(request, 'quiz/sendresetlink.html', {
            'message': 'If this email is registered with an account, you will receive an email with a link to reset your password.'
        })


def reset_password(request, uid, token):
    if request.method == 'POST':
        return handle_reset_password(request, uid, token)
    return render(request, 'quiz/resetpassword.html')


def handle_reset_password(request, uid, token):
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')

    if password == password_confirm:
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            token_generator = PasswordResetTokenGenerator()

            if token_generator.check_token(user, token):
                user.set_password(password)  # Use set_password for hashing
                user.save()
                return redirect('login')
            else:
                return render(request, 'quiz/resetpassword.html', {'error': 'Invalid or expired token.'})
        except (User.DoesNotExist, ValueError, TypeError):
            return render(request, 'quiz/resetpassword.html', {'error': 'Invalid user.'})
    else:
        return render(request, 'quiz/resetpassword.html', {'error': 'Passwords do not match.'})
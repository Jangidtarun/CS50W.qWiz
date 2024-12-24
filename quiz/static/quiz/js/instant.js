let countdown_time = 3
let countdown_time_intervalid = null
let score = 0
let lives = 3
let intervalid = null
const qwindow = 20
let timerval = qwindow

const countdowndiv = elem_with_id('countdown')
const mdiv = elem_with_id('main-div')
const timerdiv = elem_with_id('timer')
const lifediv = elem_with_id('lives')
const skip_btn = elem_with_id('skip-btn')
const scorediv = elem_with_id('score')
const submit_btn = elem_with_id('submit-btn')
const mbox = elem_with_id('mbox')
const resultsdiv = elem_with_id('results')
const roptionbox = elem_with_id('roption')

document.addEventListener('DOMContentLoaded', () => {
    console.log('hello')

    // countdown
    start_countdown()

    skip_btn.addEventListener('click', () => {
        // reduce life
        lives--;
        update_life(lives)
        timerval = qwindow
        // change to next question
        get_question().then(qdata => {
            update_and_display_question(qdata)
        })
        // update timer to full
    })

    submit_btn.addEventListener('click', () => {
        console.log('submit quiz')
        submit_quiz('you have successfully submitted the quiz')
    })

})


function update_life(clife) {
    if (clife <= 0) {
        submit_quiz('Game Over 🫠')
    } else {
        update_innerHTML(lifediv, clife)
    }
}

function elem_with_id(id) {
    return document.getElementById(id)
}

function start_countdown() {
    countdown_time_intervalid = setInterval(update_countdown, 1000)
}

function update_countdown() {
    update_innerHTML(countdowndiv, countdown_time)
    if (countdown_time > 0) {
        countdown_time--;
    } else {
        stop_countdown()
        start_quiz()
        show(mdiv)
    }
}

function update_innerHTML(elem, content) {
    elem.innerHTML = content
}

function stop_countdown() {
    clearInterval(countdown_time_intervalid)
    update_innerHTML(countdowndiv, '')
    hide(countdowndiv)
}

function stop_timer() {
    clearInterval(intervalid)
    console.log('tiemer stopped')
}

function starttimer() {
    intervalid = setInterval(update_timer, 1000)
}

function update_timer() {
    update_innerHTML(timerdiv, timerval)
    if (timerval > 0) {
        timerval--;
    } else {
        // reduce life
        lives--;
        update_life(lives)

        timerval = qwindow
        // change to next question
        get_question().then(qdata => {
            update_and_display_question(qdata);
        })
    }
}

async function get_question() {
    try {
        const response = await fetch('https://opentdb.com/api.php?amount=1&type=multiple');
        const data = await response.json();
        // console.log(data.results[0])
        return data.results[0];
    } catch (error) {
        console.error('Error fetching question:', error);
        submit_quiz('we have run out of questions')
        return null;
    }
}

function update_and_display_question(qdata) {
    const qdiv = elem_with_id('qdiv');
    const obox = elem_with_id('obox');

    update_innerHTML(qdiv, qdata.question)
    update_innerHTML(obox, '')
    let  options = []
    options.push(
        {'body': qdata.correct_answer,
        'isc': true
        })

    qdata.incorrect_answers.forEach(optionval => {
        options.push(
            {'body': optionval,
            'isc': false
            })
    });
    options = shuffleArray(options)
    const fragment = document.createDocumentFragment();

    console.log(options)

    options.forEach(option => {
        const optiondiv = document.createElement('div');
        optiondiv.className = 'option';
        update_innerHTML(optiondiv, option.body);
        fragment.appendChild(optiondiv);
        optiondiv.addEventListener('click', () => response_handler(option.isc, optiondiv));
    });

    obox.appendChild(fragment)
}

function response_handler(is_correct, optiondiv) {
    console.log('clicked', { is_correct, optiondiv });
    if (is_correct) {
        optiondiv.className = 'option correct'
        score++;
        update_innerHTML(scorediv, score)
        timerval = qwindow
        get_question().then(qdata => {
            update_and_display_question(qdata);
        })
    } else {
        optiondiv.className = 'option incorrect'
        lives--;
        update_life(lives)
    }
}

function start_quiz() {
    console.log('start');

    update_innerHTML(lifediv, lives)
    // get the question
    get_question().then(qdata => {
        update_and_display_question(qdata)
        starttimer()
    })
}

function hide(elem) {
    elem.style.display = 'none';
}

function show(elem) {
    elem.style.display = 'block';
}

function displayMessage(message) {
    const mdiv = elem_with_id('messageDiv')
    update_innerHTML(mdiv, message)
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function submit_quiz(message) {
    stop_timer()
    hide(mdiv)
    displayMessage(message)
    show(mbox)
    update_innerHTML(resultsdiv, score)
    show()
}
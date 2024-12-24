document.addEventListener('DOMContentLoaded', () => {
    const timerdiv = document.getElementById('timer')
    const questionwindow = 4
    let initialtime = questionwindow
    const countdownDiv = document.getElementById('countdown'); // Countdown element
    let intervalid = null
    const mdiv = document.getElementById('main-div')
    const mbox = document.getElementById('mbox')
    let noq = 5;
    let lives = 3;
    let score = 0;

    function updateLives(current_life) {
        document.getElementById("lives").innerHTML = current_life;
        if (current_life === 0) {
            console.log('game over')
            hide(mdiv)
            displayMessage('game over')
            show(mbox)

        }
    }

    function startQuiz() {
        hide(countdownDiv)
        show(mdiv)
        intervalid = setInterval(fupdate, 1000);
        getAndDisplayQuestions()
        updateLives(lives)
        noq--;
    }

    function fupdate() {
        timerdiv.innerHTML = initialtime
        initialtime -= 1
        if (initialtime < 0) {
            if (noq <= 0) {
                timerdiv.innerHTML = 'This quiz is over'
                clearInterval(intervalid)
                hide(mdiv)
                show(mbox)

                displayMessage('This quiz is finished')
            } else {
                // reset timer
                noq--;
                lives--;
                updateLives(lives)
                console.log(noq)
                initialtime = questionwindow;
                getAndDisplayQuestions()
                // update question
            }
        }
    }

    async function getAndDisplayQuestions() {
        try {
            const qdata = await getquestion(); // Wait for the question data

            if (!qdata) {
                displayMessage("No more questions available."); // Call the function to display the message
                // nextbtn.value = 'finish'
                return; // Exit early if no data is available
            }

            console.log(qdata); // Log the fetched data
            updatequestion(qdata); // Update the UI or handle the question data
        } catch (error) {
            console.error('Error fetching or updating question:', error); // Handle any potential errors
        }
    }

    const nextbtn = document.getElementById('next-btn')
    nextbtn.addEventListener('click', getAndDisplayQuestions);

    async function getquestion() {
        const url = '/fetchidata/';
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching question:', error);
        }
    }



    function updatequestion(qdata) {
        const qdiv = document.getElementById('qdiv');
        const obox = document.getElementById('obox');

        // Update question text
        qdiv.innerHTML = qdata.question;
        obox.innerHTML = '';

        // Randomize the order of options
        const options = shuffleArray([...qdata.options]); // Use spread operator to avoid mutating the original array

        // Create a document fragment to minimize DOM manipulations
        const fragment = document.createDocumentFragment();

        // Render each option after shuffling
        options.forEach((option) => {
            const optiondiv = document.createElement('div');
            optiondiv.className = 'option'
            optiondiv.innerHTML = option.body;
            fragment.appendChild(optiondiv);
            optiondiv.addEventListener('click', () => response_handeler(option.isc, optiondiv))
        });

        obox.appendChild(fragment);
    }

    function response_handeler(is_correct, optiondiv) {
        console.log('clicked', { is_correct, optiondiv })
        if (is_correct) {
            optiondiv.className = 'option correct'
            score++;
            // display next question
            initialtime = questionwindow
            noq--;
            getAndDisplayQuestions()
            // reset timer
        } else {
            optiondiv.className = 'option incorrect'
            lives--;
            updateLives(lives)
        }
    }
})
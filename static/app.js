
const get_welcome = document.getElementById('chatbot-icon')
const bot_container = document.getElementById('chatbot-container') 
// Function to get the current time of the day
function getTimeOfDay() {
    const hour = new Date().getHours();
    if (hour >= 0 && hour < 12) {
        return "morning";
    } else if (hour >= 12 && hour < 18) {
        return "afternoon";
    } else {
        return "evening";
    }
}

// Function to speak the welcome message
function speakWelcomeMessage() {
    const timeOfDay = getTimeOfDay();
    const welcomeMessage = `Good ${timeOfDay}, Welcome to Intelligent Text Response System`;
    
    // Check if speech synthesis is supported by the browser
    if ('speechSynthesis' in window) {
        const speech = new SpeechSynthesisUtterance(welcomeMessage);
        speech.lang = 'en-US';
        speech.volume = 1; // 0 to 1
        speech.rate = 1; // 0.1 to 10
        speech.pitch = 1; //0 to 2
        window.speechSynthesis.speak(speech);
    } else {
        alert("Sorry, your browser doesn't support speech synthesis.");
    }
}

// Toggle the chatbot container when the icon is clicked
get_welcome.addEventListener('click', function() {
    bot_container.style.display = (bot_container.style.display === 'none') ? 'block' : 'none';
    });

// Speak the welcome message when the page is loaded
get_welcome.addEventListener('click', speakWelcomeMessage);


// --------------------------------------------------------------------------------------------------------------------




// JavaScript for speech recognition    

const speakButton = document.getElementById('speak-button')

// Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = 'en-US';

recognition.onstart = () => {
    console.log('Voice recognition activated. Speak into the microphone.');
};

recognition.onerror = (event) => {
    console.error('Error occurred in recognition: ' + event.error);
};

recognition.onresult = (event) => {
    const result = event.results[0][0].transcript;
    console.log('You said: ', result);
    //responseDiv.textContent = 'You: ' + result;

    // Here you can add logic to process the user's input and generate a response
    const bot_response = new chatbot();
    bot_response.return_response(result);

    // For demonstration, let's just echo back the input
    // responseDiv.textContent = 'Bot: ' + result;
    // speakResponse(result);
};

// Speak response
function speakResponse(response) {
    const utterance = new SpeechSynthesisUtterance(response);
    speechSynthesis.speak(utterance);
}

speakButton.addEventListener('click', () => {
    recognition.start();
});

// --------------------------------------------------------------------------------------------------------------

class chatbot{
    constructor(){
        this.messages = [];
    }

    return_response(result) {
        if (result === "") {
            return;
        }

        let msg1 = { name: "User", message: result };
        this.messages.push(msg1);

        fetch('/reply', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: result.toLowerCase() })
            })
            .then(r => r.text())
            .then(r => {
            let msg2 = { name: "Bot", message: r };
            this.messages.push(msg2);
            this.updateChatText()
        });
    }

    updateChatText() {
        var html_left = '';
        var html_right = '';

        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Bot")
            {
                html_right += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
                const chat_reply = document.querySelector('.chatbot-response');
                chat_reply.innerHTML = html_right;
                speakResponse(item.message);
            }
            else
            {
                html_left += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
                const chat_message = document.querySelector('.chatbot-messages');
                chat_message.innerHTML = html_left;
            }
        
            });
    }
}

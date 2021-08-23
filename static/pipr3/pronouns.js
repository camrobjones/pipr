/**
 * pronouns.js
 *
 * Load, run, and store results for PIPR experiment
 * 
 **/

/* === Setup === */

// Load Stimuli Data
const stimuli = JSON.parse(document.getElementById('stimuli')
    .textContent);

// Load Config Data
const conf = JSON.parse(document.getElementById('conf')
    .textContent);

// Detect touchscreens
window.mobileAndTabletCheck = function() {
  let check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};
const isTouch = window.mobileAndTabletCheck();

// if ("ontouchstart" in window || navigator.msMaxTouchPoints) {
//     isTouch = true;
// } else {
//     isTouch = false;
// }

var continueText = "the spacebar";
var continueText2 = "the spacebar";
var f = "f";
var j = "j";

if (isTouch) {
  var continueText = "here";
  var continueText2 = "continue";
  var f = "A";
  var j = "B";
}

var responseText = `Select your answer using the keyboard: use the <span class='key-demo'>f</span>
      key to indicate the choice on the <b>left</b>, and the 
      <span class='key-demo'>j</span> key to indicate the choice on the
      <b>right</b>.`;
if (isTouch) {
  var responseText = "Tap the selected answer to indicate your response.";
}

/* === Turk === */

var turkInfo = jsPsych.turk.turkInfo();

/* === Util Functions === */

function saveResults() {
  // POST user data to server
  let url = "/pipr3/save_results/";
  let csrftoken = Cookies.get('csrftoken');
  let headers = {"X-CSRFToken": csrftoken};
  let results = jsPsych.data.get().values();
  let data = {results: results};
  data.ppt_id = conf.ppt_id;
  axios.post(url, data, {headers: headers})
    .then(response => {
      // console.log(response.data);
    });
}

// Scroll to top
function scrollTop() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


function ua_data() {
    let data = {};
    data.ua_header = navigator.userAgent;
    data.width = window.innerWidth;
    data.height = window.innerHeight;
    data.ppt_id = conf.ppt_id;
    data.workerID = turkInfo.workerId;
    return data;
}

function send_ua_data() {
  let data = ua_data();
  let url = "/pipr3/ua_data/";
  let csrftoken = Cookies.get('csrftoken');
  let headers = {"X-CSRFToken": csrftoken};
  axios.post(url, data, {headers: headers})
    .then(response => {
      // console.log(response.data);
    });
}

function response(key_response) {
  document.querySelector('.jspsych-display-element')
  .dispatchEvent(new KeyboardEvent('keydown', {keyCode: key_response}));
  document.querySelector('.jspsych-display-element')
  .dispatchEvent(new KeyboardEvent('keyup', {keyCode: key_response}));
}

function copyToClipboard() {

  const el = document.createElement('textarea');
  el.value = conf.key;
  el.setAttribute('readonly', '');
  el.style.position = 'absolute';
  el.style.left = '-9999px';
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);

  var confirm = document.getElementById('copy-confirm');

  confirm.classList.add('show');

  setTimeout(function(){
    var confirm = document.getElementById('copy-confirm');
    confirm.classList.remove('show');
  }, 2000);

  /* Alert the copied text */
  // alert("Copied the text: " + copyText.value);
}

// CAPTCHA

function close_captcha() {
  let badges = document.getElementsByClassName('grecaptcha-badge');
  for (let badge of badges) {
    badge.style.visibility = "hidden";
  }
}

function validate_captcha(token) {
  // console.log(`validate_captcha(${token})`)
  let url = "/pipr3/validate_captcha/";
  let csrftoken = Cookies.get('csrftoken');
  let headers = {"X-CSRFToken": csrftoken};
  let data = {
    token: token,
    ppt_id: conf.ppt_id
  };
  axios.post(url, data, {headers: headers})
    .then(response => {
      // console.log(response.data);
      if (response.data.score > 0.2) {
        close_captcha();
        // jsPsych.finishTrial(response.data)
      } else {
        window.location.href = "/pipr3/error";
      }
    });
}

function ex_captcha() {
  grecaptcha.execute(
    '6Lc8nMwZAAAAAD9VUlj6EX69mgSSJ9ODDVPqrzJe',
    {action: 'submit'})
  .then(function(token) {
      // console.log(token)
      validate_captcha(token);
  });
}

var template = document.querySelector('#demographics');

/* --- Progress Bar --- */

// Initialise variables
if (conf.condition == "AM") {
  var total_trials = 13 + stimuli.length;
} else {
  // Two post-test q's missing
  var total_trials = 11 + stimuli.length;
}


// welcome, consent, instr, p1, p2, eop, stimuli, end_trials, demo, post * 5

var current_trial = 0;


function updateProgress() {
  // Increment progress and update progress bar

  // Increment progress
  current_trial += 1;
  let pc = Math.round(current_trial * 100 / total_trials);

  // Show progress container
  let container = document.getElementById('progress-container');
  container.classList.remove('hide');


  // Update bar
  let bar = document.getElementById('progress-bar');
  bar.style.width = pc + "%";

  // Update counter
  let label = document.getElementById('progress-label');
  label.innerText = pc + "%";

}

/* === JsPsych Code === */

/* --- Intro Components --- */

// Fullscreen
var start_fullscreen = {
  type: 'fullscreen',
  fullscreen_mode: true,
  post_trial_gap: 500
};

var end_fullscreen = {
  type: 'fullscreen',
  fullscreen_mode: false
};

// Welcome
var welcome = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: `
             <div class='instructions-container'>
              <h2 class='instructions-header'>Welcome</h2>
              <p class='welcome'>Thank you for your interest in this study.</p>
              <p class='welcome' ontouchstart="response(32)">
                <b>Press ${continueText} to continue</b>
              </p>
            </div>`,
  on_finish: updateProgress,
  on_load: function() {
    ex_captcha();
    scrollTop();
  }
};


// Consent
var consent = {
  type: "survey-html-form",
  html: `
             <div>
              <h2 class='instructions-header'>Consent</h2>
              <p class='instructions'>
              Please review the consent form below and check the box if
              you agree to participate.
              </p>

              <a target="_blank" href="/static/pipr3/consent_form.pdf">Open in a new tab</a>
              
              <div id='consent-container'>
                <iframe src="/static/pipr3/consent_form.pdf#view=FitH&zoom=FitH"
                width="100%", height="800px"></iframe>
              </div>

              <div class='input-group'>
                  <label for='consent'>I agree</label>
                  <input type='checkbox' name='consent' id='consent' required>
              </div>
            </div>`,
  on_finish: updateProgress,
  on_load: scrollTop
};

// Instructions
var instructions = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Instructions
    </h2>
    <p class='instructions'>
      In this experiment, you will be asked to read short 
      passages. Each passage has been broken up into
      small groups of words. You can reveal the next group of words
      by pressing the space bar. Your task is to silently
      read each passage by repeatedly pressing
      the space bar and reading each group of words
      until you finish the passage. Please read each
      passage at your normal reading speed.
    </p>

    <p class='instructions'>
      After some of the passages, a statement will appear on the screen.
      You will then have to indicate whether the statment is true or false.
      You can do this using the 'True' and 'False' buttons on the screen.
      Therefore it is important that you read each passage carefully and
      understand what it describes.
    </p>

    <p class='instructions'>
      First you will complete two practice passages. These are not part 
      of the actual experiment. Before you read each passage, you will
      see a small cross in the top left of the screen where the first
      group of words will appear. Fix your eyes on this cross and press
      the spacebar to begin reading.
    </p>

    <p class='instructions'>
      The experiment will last around 20 minutes.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press the spacebar to continue</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    send_ua_data();
    },
};


// Post Practice
var post_practice = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      End of practice
    </h2>
    <p class='instructions-c'>
      That concludes the practice part of the exercise.
    </p>

    <p class='instructions-c'>
      Press the spacebar to continue to the main experiment.
    </p>

  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    },
};


/* --- Test Components --- */

// Trial component functions

function getTVData(data, q_no) {
  // Add data from item to jsPsych data
  data.sent_id = jsPsych.timelineVariable('sent_id')();
  data.item_id = jsPsych.timelineVariable('item_id')();
  data.order = jsPsych.timelineVariable('order')();

  // Get question-level data
  let questions = jsPsych.timelineVariable('questions')();
  let question = questions[q_no];
  data.critical = question.critical;

  if (question.critical) {
    data.item_type = "critical";
  } else {
    data.item_type = "filler";
  }

  data.question_no = question.question_no;

  data.reversed = question.reversed;
   
}

function mapKeyCodes(data) {
  // Map key press codes to choices

  // Reverse mappings if response order was reversed
  let np1 = "NP1";
  let np2 = "NP2";
  if (data.reversed) {
    [np1, np2] = [np2, np1];
  }

  if (data.key_press == 70) {
    data.response = np1;
  } else if (data.key_press == 74) {
    data.response = np2;
  } else {
    data.response = "Other";
  }
}

function getPreferenceData(data) {
  // Add preference info to trial data
  data.expt_syntax_pref = jsPsych.timelineVariable(
    'expt_syntax_pref', true);
  data.expt_physics_pref = jsPsych.timelineVariable(
    'expt_physics_pref', true);

  // Add Syntax and Physics congruency data
  data.syntax_congruent = data.response == data.expt_syntax_pref
  data.physics_congruent = data.response == data.expt_physics_pref
}

// Data counter
var i = -1;

// Preview
var preview = {
  // Show sentence before question/responses

  // Meta data
  type: "html-keyboard-response",
  choices: [' '],
  // trial_duration: jsPsych.timelineVariable('time'),
  data: {trial_part: 'preview',
         item_id: jsPsych.timelineVariable('item_id')},

  // Build stimulus
  stimulus: function() {

    // Get trial variables
    let passage = jsPsych.timelineVariable('passage')();

    // Build trial template
    let s = `
      <div class='trial-container'>
        <p class='sent'>${passage}</p>

        <p class='instructions' id='continue' ontouchstart="response(32)">
          <b>Press ${continueText} to continue</b>
        </p>
      </div>`;

    return s;
  }
};

// Questions
// Stupid solution but I can't figure out how to access nested
// timeline variables
var q1 = {

  // Meta data
  type: "html-keyboard-response",
  choices: ['f', 'j'],
  data: {trial_part: 'trial'},

  // Build stimulus
  stimulus: function() {

    // Get trial variables
    let questions = jsPsych.timelineVariable('questions')();
    let question = questions[0];
    let prompt = question.prompt;
    let responses = question.responses;
    let np1 = responses[0];
    let np2 = responses[1];
    let reversed = question.reversed;

    // Randomize button order
    if (reversed) {
      [np1, np2] = [np2, np1];
      // this.data.reversed = true;
    }

    // Build trial template
    let s = `
      <div class='trial-container'>
        <p class='question'>${prompt}</p> 
        <div class='response-container'> 

          <div class='response np1' ontouchstart='response(70)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                ${f}
              </div>
            </div>

            <div class='response-label'>
              ${np1}
            </div>
            
          </div> 

          <div class='response np2' ontouchstart='response(74)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                ${j}
              </div>
            </div>
            
            <div class='response-label'>
              ${np2}
            </div>

          </div> 

        </div>
      </div>`;

    return s;
  },

  // Store data
  on_finish: function(data) {
    getTVData(data, 0);
    mapKeyCodes(data);
    // getPreferenceData(data);
  }
};

var q2 = {

  // Meta data
  type: "html-keyboard-response",
  choices: ['f', 'j'],
  data: {trial_part: 'trial'},

  // Build stimulus
  stimulus: function() {

    // Get trial variables
    let questions = jsPsych.timelineVariable('questions')();
    let question = questions[1];
    let prompt = question.prompt;
    let responses = question.responses;
    let np1 = responses[0];
    let np2 = responses[1];
    let reversed = question.reversed;

    // Randomize button order
    if (reversed) {
      [np1, np2] = [np2, np1];
      // this.data.reversed = true;
    }

    // Build trial template
    let s = `
      <div class='trial-container'>
        <p class='question'>${prompt}</p> 
        <div class='response-container'> 

          <div class='response np1' ontouchstart='response(70)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                ${f}
              </div>
            </div>

            <div class='response-label'>
              ${np1}
            </div>
            
          </div> 

          <div class='response np2' ontouchstart='response(74)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                ${j}
              </div>
            </div>
            
            <div class='response-label'>
              ${np2}
            </div>

          </div> 

        </div>
      </div>`;

    return s;
  },

  // Store data
  on_finish: function(data) {
    getTVData(data, 1);
    mapKeyCodes(data);
    // getPreferenceData(data);
  }
};

var q3 = {

  // Meta data
  type: "html-keyboard-response",
  choices: ['f', 'j'],
  data: {trial_part: 'trial'},

  // Build stimulus
  stimulus: function() {

    // Get trial variables
    let questions = jsPsych.timelineVariable('questions')();
    let question = questions[2];
    let prompt = question.prompt;
    let responses = question.responses;
    let np1 = responses[0];
    let np2 = responses[1];
    let reversed = question.reversed;

    // Randomize button order
    if (reversed) {
      [np1, np2] = [np2, np1];
      // this.data.reversed = true;
    }

    // Build trial template
    let s = `
      <div class='trial-container'>
        <p class='question'>${prompt}</p> 
        <div class='response-container'> 

          <div class='response np1' ontouchstart='response(70)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                ${f}
              </div>
            </div>

            <div class='response-label'>
              ${np1}
            </div>
            
          </div> 

          <div class='response np2' ontouchstart='response(74)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                ${j}
              </div>
            </div>
            
            <div class='response-label'>
              ${np2}
            </div>

          </div> 

        </div>
      </div>`;

    return s;
  },

  // Store data
  on_finish: function(data) {
    getTVData(data, 2);
    mapKeyCodes(data);
    updateProgress();
    // getPreferenceData(data);
  }
};

// Combine fixation, preview, and trial into one component


// End Trials
var end_trials = {
  type: "html-keyboard-response",
  stimulus: `
  <div class='instructions-container'>
      <h2 class='instructions-header'>
        Trials Complete
      </h2>
    <p class='instructions'>
      Thank you. You have completed all of the passages.
    </p>

    <p class='instructions'>
    You will now be asked a short series of questions about yourself and
    your thoughts about the experiment.</p>
    </p>

  <p class='instructions' ontouchstart="response(32)" id='next'>
      <b>Press ${continueText} to continue<b>
    </p>
  `,
  on_finish: updateProgress
};


var demographics = {

  // Demographics Trial
  type: "survey-html-form",
  html: template.innerHTML,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'demographics'},
  on_finish: updateProgress

};


var post_test_purpose = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>What did you think the experiment was about?</h3>
  
    <textarea class="form-control feedback" id="post_test_purpose" name="post_test_purpose" required></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    updateProgress();
  }
};


var post_test_inconsistent = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Did you think that any of the passages contained information that was
      potentially inconsistent or contradictory? If so, what sort of 
      examples did you notice and how did you resolve the inconsistency?
    </h3>
  
    <textarea class="form-control feedback" id="post_test_inconsistent"
    name="post_test_inconsistent" required></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    updateProgress();
  }
};


var post_test_pronoun = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Did you notice that some of the passages contained
      pronouns (e.g. "he", "she", "it") that could be interpreted
      in more than one way?
    </h3>
  
    <textarea class="form-control feedback" id="post_test_pronoun"
    name="post_test_pronoun" required></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    updateProgress();
  }
};


var post_test_example = {
  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Some of the passages contained sections like the following:
    </h3>

    <p class='question-subtitle'>
      When the glass plate fell on the steel plate, it broke. ... 
      Fortunately the glass plate was completely unharmed on the floor.
    </p>

    <h3 class='question-title'>
      Does this passage seem inconsistent to you? How did you understand  
      what had happened in passages like this?
    </h3>

    <textarea class="form-control feedback" id="post_test_example"
    name="post_test_example" required></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    updateProgress();
  }
};


var post_test_other = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Do you have any other feedback or thoughts about the 
      experiment?
      (optional)
    </h3>
  
    <textarea class="form-control feedback" id="post_test_other"
    name="post_test_other"></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    saveResults();
    updateProgress();
  }
};



/* --- Debrief Components --- */

var debrief_block = {
  type: "html-keyboard-response",
  choices: jsPsych.NO_KEYS,
  stimulus: function() {
    
    s = `
    <div class='instructions-container'>
      <h2 class='instructions-header'>
        Complete
      </h2>

      <p class='instructions'>
        Thank you for completing the experiment.
      </p>

      <p class='instructions'>
        Your completion code is:
      </p>

      <div class='code-container'>
      
        <div id='code'>${conf.key}</div>

        <div class='code-copy' title="Copy code" onclick="copyToClipboard()">
          <img src="/static/pipr3/content_copy-24px.svg">
          </img>
        </div>

        <div id='copy-confirm' class='hidden'>
          Code copied to clipboard!
        </div>

      </div>

      <p class='instructions'>
        In order to get credit for your participation, please fill out
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSfdhjhUpgRIgNM9YSsohySVheCQmtqmfIeuyxHaUnCpOPJS0A/viewform?usp=sf_link"
        target="_blank">this google form</a>. You will need your completion code.
      </p>

      <p class='instructions'>
        You can then close this window. Thanks again!
      </p>

    </div>`;

    return s;

  }
};

/* ==== SPR ==== */

function addStimulus(timeline, trial_info, trial_part) {
    if (typeof(trial_info.stimulus) !== "string") {
        console.error("trial_info.stimulus ain't no string...");
    }

    let fix_type = "FIX_CROSS";

    let fixcross = {
        type : 'spr-moving-window',
        stimulus : '+',
        background_color : "rgb(245, 245, 245)", // light gray
        choices : FIX_CHOICES,
        font_family : "Open Sans",
        font_size : 25,
        width : 950,
        height : 600,
        trial_duration : FIX_DUR,
        data : {
            id : trial_info.id,
            item_type : fix_type,
            uil_save : false,
            trial_part: trial_part
        }
    };

    let present_text = {
        type : 'spr-moving-window',
        stimulus : trial_info.stimulus,
        background_color : "rgb(245, 245, 245)", // light gray
        font_color : "rgb(0, 0, 0)", // black
        font_family : "Open Sans",
        font_size : 25,
        width : 950,
        height : 600,
        post_trial_gap : ISI,
        grouping_string : GROUPING_STRING,
        data : {
            id : trial_info.id,
            item_type : trial_info.item_type,
            continuation : trial_info.continuation,
            item_id : trial_info.item_id,
            order : trial_info.order,
            sent_id : trial_info.sent_id,
            unambiguous: trial_info.unambiguous,
            trial_part: trial_part,
            uil_save : true
        },
        on_finish: updateProgress
    }

    timeline.push(fixcross);
    timeline.push(present_text);
}

/**
 * Add a question to a jsPsych timeline.
 */

function addQuestion(timeline, trial_info, trial_part)
{
    if (typeof(trial_info.question) !== "string") {
        console.error("trial_info.question ain't no string...");
    }
    if (typeof(trial_info.qanswer) !== "string") {
        console.error("trial_info.qanswer ain't no string...");
    }

    let question = {
        type : 'html-button-response',
        stimulus : trial_info.question,
        choices : G_QUESTION_CHOICES,
        data : {
            id : trial_info.id,
            item_type : trial_info.item_type,
            expected_answer : trial_info.qanswer,
            uil_save : true,
            trial_part: trial_part
        },
        on_finish: function (data) {
            let choice = G_QUESTION_CHOICES[data.button_pressed];
            data.answer = choice;
            data.correct = choice == data.expected_answer;
        }
    };

    timeline.push(question);
}

function addStimuliToTimeline(timeline, stimuli, trial_part) {
    stimuli.forEach (
        stim_info => {
            addStimulus(timeline, stim_info, trial_part);
            if (stim_info.question !== "") {
                addQuestion(timeline, stim_info, trial_part);
            }
        }
    );
}

/* === Setup === */

/* --- Create Timeline --- */

var timeline = [];

let list_1 = {list_name : "list1", table : stimuli}.table;

var timeline = [welcome];

// timeline.push(consent);

// Fullscreen for non-touch
// timeline.push(start_fullscreen);

// Main expt timeline for all
// timeline.push(instructions);

// Add trial procedure
// addStimuliToTimeline(timeline, PRACTICE_ITEMS, "practice");

// timeline.push(post_practice);

// Add trial procedure
// addStimuliToTimeline(timeline, list_1, "trial");

// Post-test questions
timeline.push(end_trials, demographics, post_test_purpose,
              post_test_inconsistent);

if (conf.condition == "AM") {
  timeline.push(post_test_pronoun, post_test_example);
}

// End fullscreen for non-touch
timeline.push(post_test_other, end_fullscreen);

// Debrief block for all
timeline.push(debrief_block);

/* --- Prevent Back --- */

history.pushState(null, document.title, location.href);
window.addEventListener('popstate', function (event)
{
  goBack = confirm("Are you sure you want to go back? Your progress will be lost.");
  if (goBack) {
    window.history.back();
  } else {
    history.pushState(null, document.title, location.href);
  }
});

/* --- Launch jsPsych --- */
window.onload = function() {

  if (! isTouch) {

    jsPsych.init({
      timeline: timeline,
      experiment_width: 950,
      display_element: "expt-container",
      exclusions: {
                    min_width : MIN_WIDTH,
                    min_height : MIN_HEIGHT
                },
    });

  } else { // or bail out.
        let paragraph = document.getElementById("expt-container");
        paragraph.innerHTML = 
        `
        <div class='instructions-container'>
          <h2 class='instructions-header'>
            Mobile or Tablet detected
          </h2>

          <p class='instructions'>
            Please run this experiment on a desktop or laptop computer, not a mobile or tablet.
          </p>
        </div>
      `;
    }
};

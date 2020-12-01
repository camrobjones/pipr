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
if (isTouch) {
  var continueText = "here";
}

/* === Turk === */

var turkInfo = jsPsych.turk.turkInfo();

/* === Util Functions === */

function saveResults() {
  // POST user data to server
  let url = "/pronouns/save_results/";
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
  let url = "/pipr/ua_data/";
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
  for (badge of badges) {
    badge.style.visibility = "hidden";
  }
}

function validate_captcha(token) {
  // console.log(`validate_captcha(${token})`)
  let url = "/pronouns/validate_captcha/";
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
        close_captcha()
        // jsPsych.finishTrial(response.data)
      } else {
        window.location.href = "/pronouns/error"
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
if (conf.mode == "physics_norm") {
  var total_trials = 9 + stimuli.length;
} else {
  // Extra post_test trials
  var total_trials = 14 + stimuli.length;
}
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
  bar.style.width = pc + "%"

  // Update counter
  let label = document.getElementById('progress-label');
  label.innerText = pc + "%"

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
              <p class='welcome'>Thank you for participating in this study.</p>
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

              <a target="_blank" href="/static/pronouns/consent_form.pdf">Open in a new tab</a>
              
              <div id='consent-container'>
                <iframe src="/static/pronouns/consent_form.pdf#view=FitH&zoom=FitH"
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
      passages describing situations and then answer a question 
      about what happened.
    </p>

    <p class='instructions'>
      Each passage will appear for a few seconds to give you time to read it.
      Then a question will appear, with two possible answers.
      Select your answer using the keyboard: use the <span class='key-demo'>f</span>
      key to indicate the choice on the <b>left</b>, and the 
      <span class='key-demo'>j</span> key to indicate the choice on the
      <b>right</b>. If you are using a touchscreen, you can simply tap your selected
      answer.
    </p>
    <p class='instructions'>
      Read each sentence carefully and answer the questions as quickly
      and accurately as possible. The experiment will last around 20 minutes.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press ${continueText} to continue</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    send_ua_data();
    },
};

// Physics Instructions
var phys_instructions = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Instructions
    </h2>
    <p class='instructions'>
      In this experiment, you will be asked questions about hypothetical
      situations involving common objects.
    </p>

    <p class='instructions'>
      Each question will appear for a few seconds to give you time to read it.
      Then two possible answers will appear below it. Select your
      answer using the keyboard: use the <span class='key-demo'>f</span>
      key to indicate the choice on the <b>left</b>, and the 
      <span class='key-demo'>j</span> key to indicate the choice on the
      <b>right</b>. If you are using a touchscreen, you can simply tap your selected
      answer.
    </p>
    <p class='instructions'>
      Read each question carefully and answer as quickly
      and accurately as possible. The experiment will last around 20 minutes.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press ${continueText} to continue</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: function() {
    updateProgress();
    send_ua_data();
  }
};

// Example
var example = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Example
    </h2>
    <p class='instructions'>
      For example, the following might appear:
    </p>

    <div class='trial-container example'>
      <p class='sent'>John insulted Mary because he was jealous.</p> 
      <p class='question'>Who was jealous?</p> 
      <div class='response-container'> 

        <div class='response np1'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              f
            </div>
          </div>

          <div class='response-label'>
            Mary
          </div>
          
        </div> 

        <div class='response np2'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              j
            </div>
          </div>
          
          <div class='response-label'>
            John
          </div>

        </div> 

      </div>
    </div>

    <p class='instructions'>
      In this example, you would press <span class='key-demo'>j</span>
      to indicate that <b>John</b> was jealous.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press ${continueText} to continue<b>
    </p>

  </div>`,
  on_finish: updateProgress,
  on_load: scrollTop,
  post_trial_gap: 500,
};


// Example
var example_2 = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Example 2
    </h2>
    <p class='instructions'>
      Here is another example:
    </p>

    <div class='trial-container example'>
      <p class='sent'>
        The mechanic asked the customer a question, 
        but he didn't know the answer.
      </p> 
      <p class='question'>Who didn't know the answer?</p> 
      <div class='response-container'> 

        <div class='response np1'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              f
            </div>
          </div>

          <div class='response-label'>
            The customer
          </div>
          
        </div> 

        <div class='response np2'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              j
            </div>
          </div>
          
          <div class='response-label'>
            The mechanic
          </div>

        </div> 

      </div>
    </div>

    <p class='instructions'>
      In this example, you would press <span class='key-demo'>f</span>
      to indicate that <b>the customer</b> didn't know the answer.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>The experiment will begin on the next page.</b>
    </p>
    <p class='instructions' ontouchstart="response(32)">
      <b>Press ${continueText} to begin<b>
    </p>

  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: updateProgress,
};


// Physics Example
var phys_example = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Example
    </h2>
    <p class='instructions'>
      For example, the following might appear:
    </p>

    <div class='trial-container example'>
      <p class='sent'>If a steel ball and a styrofoam ball were
      placed into a bath of water, which would be more likely to sink?</p> 
      <p class='question'></p> 
      <div class='response-container'> 

        <div class='response np1'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              f
            </div>
          </div>

          <div class='response-label'>
            The styrofoam ball
          </div>
          
        </div> 

        <div class='response np2'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              j
            </div>
          </div>
          
          <div class='response-label'>
            The steel ball
          </div>

        </div> 

      </div>
    </div>

    <p class='instructions'>
      In this example, you would press <span class='key-demo'>j</span>
      to indicate that <b>the steel ball</b> is more likely to sink.
    </p>

    <p class='instructions' id='continue' ontouchstart="response(32)">
      <b>Press ${continueText} to continue<b>
    </p>

  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: updateProgress,
};

// Physics Example
var phys_example_2 = {
  type: "html-keyboard-response",
  choices: [' '],
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Example 2
    </h2>
    <p class='instructions'>
      Here is another example:
    </p>

    <div class='trial-container example'>
      <p class='sent'>
        If an apple and a leaf are dropped from a tall builiding
        at the same time, which is more likely to reach the ground
        first?
      </p> 
      <p class='question'></p> 
      <div class='response-container'> 

        <div class='response np1'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              f
            </div>
          </div>

          <div class='response-label'>
            The leaf
          </div>
          
        </div> 

        <div class='response np2'>

          <div class='key-reminder-container'>
            <div class='key-reminder'>
              j
            </div>
          </div>
          
          <div class='response-label'>
            The apple
          </div>

        </div> 

      </div>
    </div>

    <p class='instructions'>
      In this example, you would press <span class='key-demo'>j</span>
      to indicate that <b>the apple</b> is more likely to reach the ground
      first.
    </p>

    <p class='instructions' id='continue'>
      <b>The experiment will begin on the next page.</b>
    </p>
    <p class='instructions' ontouchstart="response(32)">
      <b>Press ${continueText} to begin<b>
    </p>

  </div>`,
  post_trial_gap: 500,
  on_load: scrollTop,
  on_finish: updateProgress,
};

/* --- Test Components --- */

var fixation = {

  // Fixation Trial
  type: "html-keyboard-response",
  stimulus: "<div class='fixation-cross'>+</div>",
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'fixation'},

  // Randomly sample trial duration
  trial_duration: function(){
    return jsPsych.randomization.sampleWithoutReplacement(
        [750, 1000, 1250, 1500], 1)[0];
  }
};

// Trial component functions

function getTVData(data) {
  // Add data from item to jsPsych data
  data.sent_id = jsPsych.timelineVariable('sent_id')();
  data.item_type = jsPsych.timelineVariable('item_type')();
  data.item_id = jsPsych.timelineVariable('item_id')();
  data.order = jsPsych.timelineVariable('order')();
  data.reversed = jsPsych.timelineVariable('reversed')();
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

// Preview
var preview = {
  // Show sentence before question/responses

  // Meta data
  type: "html-keyboard-response",
  choices: jsPsych.NO_KEYS,
  trial_duration: jsPsych.timelineVariable('time'),
  data: {trial_part: 'preview'},

  // Build stimulus
  stimulus: function() {

    // Get trial variables
    let sent = jsPsych.timelineVariable('sent')();
    let question = "";
    let np1 = "";
    let np2 = "";

    // Build trial template
    let s = `
      <div class='trial-container'>
        <p class='sent'>${sent}</p> 
        <p class='question'>${question}</p> 
        <div class='response-container'> 

          <div class='np1'>${np1}</div> 
          <div class='np2'>${np2}</div>

        </div>
      </div>`;

    return s;
  }
};

// Trial
var trial = {

  // Meta data
  type: "html-keyboard-response",
  choices: ['f', 'j'],
  data: {trial_part: 'trial'},

  // Build stimulus
  stimulus: function() {

    // Get trial variables
    let sent = jsPsych.timelineVariable('sent')();
    let question = jsPsych.timelineVariable('question')();
    let np1 = jsPsych.timelineVariable('NP1')();
    let np2 = jsPsych.timelineVariable('NP2')();
    let reversed = jsPsych.timelineVariable('reversed')();

    // Randomize button order
    if (reversed) {
      [np1, np2] = [np2, np1];
      // this.data.reversed = true;
    }

    // Build trial template
    let s = `
      <div class='trial-container'>
        <p class='sent'>${sent}</p> 
        <p class='question'>${question}</p> 
        <div class='response-container'> 

          <div class='response np1' ontouchstart='response(70)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                f
              </div>
            </div>

            <div class='response-label'>
              ${np1}
            </div>
            
          </div> 

          <div class='response np2' ontouchstart='response(74)'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                j
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
    getTVData(data);
    mapKeyCodes(data);
    updateProgress();
    // getPreferenceData(data);
  }
};


// Combine fixation, preview, and trial into one component
var trial_procedure = {
  timeline: [fixation, preview, trial],
  timeline_variables: stimuli,
  randomize_order: true,
};


// End Trials
var end_trials = {
  type: "html-keyboard-response",
  stimulus: `
  <div class='instructions-container'>
      <h2 class='instructions-header'>
        Trials Complete
      </h2>
    <p class='instructions'>
      Thank you. You have completed all of the comprehension questions.
    </p>

    <p class='instructions'>
    You will now be asked a short series of questions about yourself and
    your thoughts about the experiment.</p>
    </p>

  <p class='instructions' ontouchstart="response(32)" id='next'>
      <b>Press ${continueText} to begin<b>
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


var post_test_correct = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Did you think that any of the questions had more than one correct
      answer? Why or why not?
    </h3>
  
    <textarea class="form-control feedback" id="post_test_correct"
    name="post_test_correct" required></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    updateProgress();
  }
};


var post_test_rule = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Did you notice using any particular strategies to make your choice?
    </h3>
  
    <textarea class="form-control feedback" id="post_test_rule"
    name="post_test_rule" required></textarea>

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
      Did you notice that each question involved deciding what a given
      pronoun (e.g. "he", "she", "it") referred to?
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


var post_test_syntax = {
  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Did you notice that the position of words in the sentence
      influenced your answers? If so, how?
    </h3>
  
    <textarea class="form-control feedback" id="post_test_syntax"
    name="post_test_syntax" required></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: function() {
    updateProgress();
  }
};


var post_test_semantics = {
  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>
      Did you notice thinking about how the scenarios would 
      play out in the real world to make your choices?
    </h3>
  
    <textarea class="form-control feedback" id="post_test_semantics"
    name="post_test_semantics" required></textarea>

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
          <img src="/static/pronouns/content_copy-24px.svg">
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

/* === Setup === */

/* --- Create Timeline --- */

// Alter instructions for physics
if (conf.mode == "physics_norm") {
  instructions = phys_instructions;
  example = phys_example;
  example_2 = phys_example_2;
}

var timeline = [welcome, consent];

// Fullscreen for non-touch
if (!isTouch) {
  timeline.push(start_fullscreen);
}

// Main expt timeline for all
timeline.push(instructions, example, example_2, trial_procedure, 
              end_trials, demographics, post_test_purpose);

// Extra post test for syntax & expt condition
if (conf.mode != "physics_norm") {
  timeline.push(post_test_correct, post_test_rule, post_test_pronoun,
                post_test_syntax, post_test_semantics);
}

// post_test_other for all conditions
timeline.push(post_test_other);

// End fullscreen for non-touch
if (!isTouch) {
  timeline.push(end_fullscreen);
}

// Debrief block for all
timeline.push(debrief_block);

/* --- Prevent Back --- */

history.pushState(null, document.title, location.href);
window.addEventListener('popstate', function (event)
{
  goBack = confirm("Are you sure you want to go back? Your progress will be lost.")
  if (goBack) {
    window.history.back();
  } else {
    history.pushState(null, document.title, location.href);
  }
});

/* --- Launch jsPsych --- */
window.onload = function() {

  jsPsych.init({
    timeline: timeline,
    experiment_width: 800,
    display_element: "expt-container",
  });
};

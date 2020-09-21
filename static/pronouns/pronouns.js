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

/* === Util Functions === */

function saveResults() {
  // POST user data to server
  let url = "/pronouns/save_results/";
  let csrftoken = Cookies.get('csrftoken');
  let headers = {"X-CSRFToken": csrftoken};
  let results = jsPsych.data.get().values();
  let data = {results: results};
  axios.post(url, data, {headers: headers})
    .then(response => {
      console.log(response.data);
    });
}

var template = document.querySelector('#demographics');

/* --- Progress Bar --- */

// Initialise variables
var total_trials = 6 + stimuli.length;
var current_trial = 0;


function updateProgress() {
  // Increment progress and update progress bar

  // Increment progress
  current_trial += 1;
  let pc = Math.round(current_trial * 100 / total_trials)

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

// CAPTCHA

function close_captcha() {
  let badges = document.getElementsByClassName('grecaptcha-badge');
  for (badge of badges) {
    badge.style.visibility = "hidden"
  }
}

function validate_captcha(token) {
  // console.log(`validate_captcha(${token})`)
  let url = "/pronouns/validate_captcha/";
  let csrftoken = Cookies.get('csrftoken');
  let headers = {"X-CSRFToken": csrftoken};
  let data = {token: token};
  axios.post(url, data, {headers: headers})
    .then(response => {
      console.log(response.data)
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



/* === JsPsych Code === */

/* --- Intro Components --- */

// // captcha
// var captcha = {
//   type: "html-keyboard-response",
//   stimulus: `
//              <div class='instructions-container'>
//               <h2 class='instructions-header'></h2>
              
//             </div>`,
//   choices: jsPsych.NO_KEYS,
// };

// Fullscreen
var start_fullscreen = {
  type: 'fullscreen',
  fullscreen_mode: true,
  post_trial_gap: 500
}

var end_fullscreen = {
  type: 'fullscreen',
  fullscreen_mode: false
}

// Welcome
var welcome = {
  type: "html-keyboard-response",
  stimulus: `
             <div class='instructions-container'>
              <h2 class='instructions-header'>Welcome</h2>
              <p class='welcome'>Thank you for accepting this HIT.</p>
              <p class='welcome'><b>Press any key to continue</b></p>
            </div>`,
  on_finish: updateProgress,
  on_load: ex_captcha,
};

// Instructions
var instructions = {
  type: "html-keyboard-response",
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
      Then a question will appear, with two possible answers. Select your
      answer using the keyboard: use the <span class='key-demo'>f</span>
      key to indicate the choice on the <b>left</b>, and the 
      <span class='key-demo'>j</span> key to indicate the choice on the
      <b>right</b>.
    </p>
    <p class='instructions'>
      Read each sentence carefully and answer the questions as quickly
      and accurately as possible. The experiment will last around 20 minutes.
    </p>

    <p class='instructions' id='continue'>
      <b>Press any key to continue</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_finish: updateProgress,
};

// Physics Instructions
var phys_instructions = {
  type: "html-keyboard-response",
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Instructions
    </h2>
    <p class='instructions'>
      In this experiment, you will be asked to read questions 
      about common objects.
    </p>

    <p class='instructions'>
      Each question will appear for a few seconds to give you time to read it.
      Then two possible answers will appear below it. Select your
      answer using the keyboard: use the <span class='key-demo'>f</span>
      key to indicate the choice on the <b>left</b>, and the 
      <span class='key-demo'>j</span> key to indicate the choice on the
      <b>right</b>.
    </p>
    <p class='instructions'>
      Read each question carefully and answer as quickly
      and accurately as possible. The experiment will last around 20 minutes.
    </p>

    <p class='instructions' id='continue'>
      <b>Press any key to continue</b>
    </p>
  </div>`,
  post_trial_gap: 500,
  on_finish: updateProgress,
};

// Example
var example = {
  type: "html-keyboard-response",
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

    <p class='instructions' id='continue'>
      <b>Press any key to continue<b>
    </p>

  </div>`,
  on_finish: updateProgress,
  post_trial_gap: 500,
};


// Example
var example_2 = {
  type: "html-keyboard-response",
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

    <p class='instructions' id='continue'>
      <b>The experiment will begin on the next page.</b>
    </p>
    <p class='instructions'>
      <b>Press any key to begin<b>
    </p>

  </div>`,
  post_trial_gap: 500,
  on_finish: updateProgress,
};


// Physics Example
var phys_example = {
  type: "html-keyboard-response",
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
      to indicate that <b>The steel ball</b> is more likely to sink.
    </p>

    <p class='instructions' id='continue'>
      <b>Press any key to continue<b>
    </p>

  </div>`,
  post_trial_gap: 500,
  on_finish: updateProgress,
};

// Physics Example
var phys_example_2 = {
  type: "html-keyboard-response",
  stimulus: 
  `
  <div class='instructions-container'>
    <h2 class='instructions-header'>
      Example
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
      to indicate that <b>The apple</b> is more likely to reach the ground
      first.
    </p>

    <p class='instructions' id='continue'>
      <b>The experiment will begin on the next page.</b>
    </p>
    <p class='instructions'>
      <b>Press any key to begin<b>
    </p>

  </div>`,
  post_trial_gap: 500,
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
  data.sent_id = jsPsych.timelineVariable('sent_id')(),
  data.item_type = jsPsych.timelineVariable('item_type')(),
  data.item_id = jsPsych.timelineVariable('item_id')(),
  data.order = jsPsych.timelineVariable('order')(),
  data.reversed = jsPsych.timelineVariable('reversed')()
}

function mapKeyCodes(data) {
  // Map key press codes to choices

  // Reverse mappings if response order was reversed
  let np1 = "NP1";
  let np2 = "NP2";
  if (data.reversed) {
    [np1, np2] = [np2, np1]
  };

  if (data.key_press == 70) {
    data.response = np1
  } else if (data.key_press == 74) {
    data.response = np2
  } else {
    data.response = "Other"
  }
}

function getPreferenceData(data) {
  // Add preference info to trial data
  data.expt_syntax_pref = jsPsych.timelineVariable(
    'expt_syntax_pref', true)
  data.expt_physics_pref = jsPsych.timelineVariable(
    'expt_physics_pref', true)

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
  trial_duration: 3000,
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

          <div class='response np1'>${np1}</div> 
          <div class='response np2'>${np2}</div>

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

          <div class='response np1'>

            <div class='key-reminder-container'>
              <div class='key-reminder'>
                f
              </div>
            </div>

            <div class='response-label'>
              ${np1}
            </div>
            
          </div> 

          <div class='response np2'>

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

  <p>You have completed all of the completed all of the comprehension questions.</p>

  <p>You will now be asked a short series of questions about yourself and
     your thoughts about the experiment.</p>

  <p id='next'>Press any key to continue.</p>
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


var post_test = {

  // Post Test Questionnaire
  type: "survey-html-form",
  html: `<h3 class='title'>Feedback</h3>

  <div class='question'>
    <h3 class='question-title'>What did you the experiment was about overall?</h3>
  
    <textarea class="form-control feedback" id="feedback_1" name="feedback_1" required></textarea>

  </div>

  <div class='question'>
    <h3 class='question-title'>Do you have any other feedback or thoughts on the experiment? (optional)</h3>
  
    <textarea class="form-control feedback" id="feedback_2" name="feedback_2"></textarea>

  </div>`,
  choices: jsPsych.NO_KEYS,
  data: {trial_part: 'post_test'},
  on_finish: updateProgress
  // Randomly sample trial duration
};



/* --- Debrief Components --- */

var debrief_block = {
  type: "html-keyboard-response",
  stimulus: function() {

    // Get all response trials
    var trials = jsPsych.data.get().filter({trial_part: 'trial'});
    let n_trials = trials.count();

    // Count syntax and physics congruent
    var syntax_congruent = trials.filter({syntax_congruent: true});
    var physics_congruent = trials.filter({physics_congruent: true});

    // Get percentages
    var syntax_pct = Math.round(syntax_congruent.count() / 
      n_trials * 100);
    var physics_pct = Math.round(physics_congruent.count() / 
      n_trials * 100);

    // Get mean rt
    var rt = Math.round(trials.select('rt').mean());
    let s = `<p>Your average response time was ${rt}ms.</p>`

    // if (conf.mode == "expt") {
    //   s += `<p>Your responses were ${syntax_pct}% consistent with syntax, 
    //         and ${physics_pct}% consistent with physics.</p>`
    // }
    
    s = "<p>Press any key to complete the experiment. Thank you!</p>";

    return s;

  }
};

/* --- Setup --- */

// Alter instructions for physics
if (conf.mode == "physics_norm") {
  instructions = phys_instructions;
  example = phys_example;
  example_2 = phys_example_2;
}

// Create jsPsych timeline
var timeline = [start_fullscreen, welcome, instructions, example, example_2,
                trial_procedure, demographics, post_test, debrief_block,
                end_fullscreen]

// Launch jsPsych
window.onload = function() {
  jsPsych.init({
    timeline: timeline,
    experiment_width: 800,
    display_element: "expt-container",
    on_finish: function() {
        saveResults();
      }
  });
};

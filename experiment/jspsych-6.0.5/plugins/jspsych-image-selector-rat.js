/**
 * jspsych-image-selector
 *
 * Displays multiple images. The participant responds by clicking
 * on one of the images.
 * feedback is (optionally) provided after the user has responded
 *
 *  A default image style is defined within the trial. This can be
 * customised with the image_style parameter.
 **/

jsPsych.plugins['image-selector-rat'] = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('image-selector-rat', 'stimulus', 'image');

  plugin.info = {
    name: 'image-selector-rat',
    description: '',
    parameters: {
      stimulus: {
        type: jsPsych.plugins.parameterType.IMAGE,
        pretty_name: 'Stimulus',
        default: undefined,
        array: true,
        description: 'The images to be displayed.'
      },
      target_image_index: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Target image index',
        default: null,
        description: 'The index of the target image.'
      },
      correct_text: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Correct text',
        default: "<p>Correct</p>",
        description: 'String to show when correct answer is given.'
      },
      incorrect_text: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Incorrect text',
        default: "<p>Incorrect</p>",
        description: 'String to show when incorrect answer is given.'
      },
      prompt: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed below the stimulus.'
      },
      force_correct_button_press: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Force correct button press',
        default: false,
        description: 'If set to true, then the subject must click on the correct image after feedback in order to advance to next trial.'
      },
      show_stim_with_feedback: {
        type: jsPsych.plugins.parameterType.BOOL,
        default: true,
        no_function: false,
        description: ''
      },
      show_feedback_on_timeout: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Show feedback on timeout',
        default: false,
        description: 'If true, stimulus will be shown during feedback. If false, only the text feedback will be displayed during feedback.'
      },
      timeout_message: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Timeout message',
        default: "<p>Please respond faster.</p>",
        description: 'The message displayed on a timeout non-response.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show trial'
      },
      do_feedback: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Do feedback',
        default: false,
        description: 'If true, feedback will be shown after a response.'
      },
      feedback_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Feedback duration',
        default: 0,
        description: 'How long to show feedback.'
      },
      image_style: {
        type: jsPsych.plugins.parameterType.COMPLEX,
        pretty_name: 'Image style',
        default: null
      },
      show_border: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Show border',
        default: true,
        description: 'If true, a border is shown around each image'
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    // set the default image style
    trial.default_image_style = {
      border: '1px solid',
      display: 'flex',
      margin: '10px',
      padding: '5px',
      color: 'black'
    }

    display_element.innerHTML = show_images();

    // if prompt is set, show prompt
    if (trial.prompt !== null) {
      display_element.innerHTML += '<p>' + trial.prompt + '</p>';
    }

    // start timing
    var start_time = Date.now();

    // add event listeners to images
    for (var i = 0; i < trial.stimulus.length; i++) {
      display_element.querySelector('#jspsych-image-selector-' + i).addEventListener('click', function(e){
        var index = e.currentTarget.getAttribute('index'); // don't use dataset for jsdom compatibility
        after_response({
          index: index,
          rt: Date.now() - start_time
        });
      });
    }

    function show_images() {
      var style = trial.default_image_style;
      // iterate through the image style parameter
      // override defaults with user defined parameters
      // and add additional user defined parameters
      for(param in trial.image_style) {
          style[param] = trial.image_style[param];
      }

      var border_style = (trial.show_border) ?
                            'border:' + style.border +';': 'border: none;';

      var html = '<div style="display: ' + style.display + ';">'; // image container

      for(i=0;i<trial.stimulus.length;i++) {
        html += '<div style="display: flex;align-self: center;';

        for(s in style) {
          html += s + ':' + style[s] + ';';
        }
        html += '">';

        // can use image-unselected class to specify the look of images before
        // a selection has been made (in combination with image-selected classes)
        // if providing visual feedback.
      //  html += '<img src="' + trial.stimulus[i] + '" id="jspsych-image-selector-' + i
        //                      + '" class="image-unselected" index='+i+'></img>';
        html += '</div>';
      }
      html += '</div>'; // end image container

      return html;
    };

    var trial_data = {};

    // create response function
    var after_response = function(info) {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      var correct = (trial.target_image_index == info.index)

      // save data
      trial_data = {
        "rt": info.rt,
        "correct": correct,
        "stimulus": trial.stimulus,
        "image_click": info.index
      };

      display_element.innerHTML = '';

      var timeout = info.rt == null;
      doFeedback(correct, timeout);
    }

    // call after response if no response after trial duration time
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        after_response({
          index: null,
          rt: null
        });
      }, trial.trial_duration);
    }

    function doFeedback(correct, timeout) {

      if (timeout && !trial.show_feedback_on_timeout) {
        display_element.innerHTML += trial.timeout_message;
      }
      else if(trial.do_feedback) {
        // show image during feedback if flag is set
        if (trial.show_stim_with_feedback) {
          display_element.innerHTML = show_images();
        }

        // show the feedback text.
        var atext = "";
        if (correct) {
          atext = trial.correct_text;
        } else {
          atext = trial.incorrect_text;
        }

        // show the feedback
        display_element.innerHTML += atext;
      }
      // check if force correct choice  is set
      if (trial.force_correct_button_press && correct === false && ((timeout && trial.show_feedback_on_timeout) || !timeout)) {
        // not implemented
      }
      else {
        jsPsych.pluginAPI.setTimeout(function() {
          endTrial();
        }, trial.feedback_duration);
      }

    }

    function endTrial() {
      display_element.innerHTML = '';
      jsPsych.finishTrial(trial_data);
    }

  };

  return plugin;
})();
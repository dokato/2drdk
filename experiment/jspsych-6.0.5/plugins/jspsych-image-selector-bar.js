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

jsPsych.plugins['image-selector-bar'] = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('image-selector-bar', 'stimulus', 'image');

  plugin.info = {
    name: 'image-selector-bar',
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
      goal: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Goal',
        default: null,
        description: 'Number of points necessary to reach point bonus.'
      },
      bar_text: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Bar Text',
        default: null,
        description: 'Any content here will be displayed on the bar.'
      },
      left_pay: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Left Pay',
        default: null,
        description: 'Left Payoff.'
      },
      right_pay: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Right Pay',
        default: null,
        description: 'Right Payoff.'
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
        default: "<p>Too slow. Please respond faster.</p>",
        description: 'The message displayed on a timeout non-response.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show trial'
      },
      trial_no: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial num',
        default: null,
        description: 'Which trial out of a set'
      },
      trial_max: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial max',
        default: null,
        description: 'Max trials'
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
        default: 1300,
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
        default: false,
        description: 'If true, a border is shown around each image'
      }
    }
  }



  plugin.trial = function(display_element, trial) {

    // set the default image style
    trial.default_image_style = {
      border: '0px solid',
      display: 'flex',
      margin: '10px',
      padding: '5px',
      color: 'black',
    }

    display_element.innerHTML = show_images();

    //set trials
    if (trial.trial_no == 1) {
      points = 0;
      points2 = 0;
    };
    var trial_no = 'Choice ' + trial.trial_no + ' of ' + trial.trial_max;

    // Add countdown timer
    var countdownNumberEl = document.querySelectorAll('#countdown-number');
    var countdown = 5;
    countdownNumberEl.textContent = countdown;
    setInterval(function() {
      countdown = --countdown <= 0 ? 5 : countdown;

      countdownNumberEl.textContent = countdown;
      //console.log(countdownNumberEl.textContent);
    }, 1000);

    // start timing
    var start_time = Date.now();

    // add event listeners to images
    for (var i = 0; i < trial.stimulus.length; i++) {
      display_element.querySelector('#jspsych-image-selector-' + i).addEventListener('click', function(e) {
        var index = e.currentTarget.getAttribute('index'); // don't use dataset for jsdom compatibility
        after_response({
          index: index,
          rt: Date.now() - start_time
        });
      });
    }

    function show_images() {
      if (trial.trial_no == 1) {
        points = 0;
        points2 = 0;
      };
      var style = trial.default_image_style;
      // iterate through the image style parameter
      // override defaults with user defined parameters
      // and add additional user defined parameters
      for (param in trial.image_style) {
        style[param] = trial.image_style[param];
      }

      var border_style = (trial.show_border) ?
        'border:' + style.border + ';' : 'border: none;';

      var goal = '<font size="6">' + 'Bonus Progress: ' + points + '/' + trial.goal + "</font>";
      var trial_no = 'Choice ' + trial.trial_no + ' of ' + trial.trial_max;
      var html = goal;

      html += '<div id="countdown" <div id="countdown-number"></div> <svg style="margin-left:26.5em"><circle r = "18" cx = "20" cy = "20" ></circle></svg></div>';

<div '
      html += '<div style="display: ' + style.display + ';">'; // image container
      //'<img src ="'+trial.prompt+ '" id="jspsych-image-slider-2AFC-"></img>';


      for (i = 0; i < trial.stimulus.length; i++) {
        html += '<div style="display: flex;align-self: center;';

        for (s in style) {
          html += s + ':' + style[s] + ';';

        }
        html += '">';

        // can use image-unselected class to specify the look of images before
        // a selection has been made (in combination with image-selected classes)
        // if providing visual feedback.
      //  html += ' <div id="countdown-number"></div> <svg><circle r = "127" cx = "129" cy = "129" ></circle></svg>';
        html += '<img src="' + trial.stimulus[i] + '" id="jspsych-image-selector-' + i +
          '" class="image-unselected" style="position: relative; display: flex" index=' + i + '></img>';
        //  html += '<div style="align-self: center; position: absolute; margin-left:7.5em">' + '<font size="10">' + trial.left_pay + '</font></div>';
        if (i==0) {
          html += '<div id="countdown-number"></div> <svg><circle r = "18" cx = "20" cy = "20" ></circle></svg>';
          //html += '<div id="countdown-number"></div><strong>rdrd</strong>'
          };
        html += '</div>';
      }
      //  html += '<class="centered">'+trial.right_pay;
      html += '</div>'; // end image container

      html += '<div class="large"; style="display: grid"> <font size="6">' + trial_no + '</font></div>';

      //


      //add bar
      //bar width
      let root = document.documentElement;
      var scaled_points = points / trial.goal * 100;
      root.style.setProperty('--width', scaled_points);
      //goal:

      html += '<div class="progress-bar" style="position: relative"></div>';
    //  html += '<div> ' + points + ' </div>'; //  html +=  '<div class="w3-green" style="width:500px"></div>';
      html += '</div><br>';


      return html;
    };

    ///feedback screen
    function show_fb() {
      var style = trial.default_image_style;
      // iterate through the image style parameter
      // override defaults with user defined parameters
      // and add additional user defined parameters
      for (param in trial.image_style) {
        style[param] = trial.image_style[param];
      }

      var border_style = (trial.show_border) ?
        'border:' + style.border + ';' : 'border: none;';

      var goal = '<font size="6">' + 'Bonus Progress: ' + points + '/' + trial.goal + "</font>";

      var html = goal;
      html += '<div style="display: ' + style.display + ';">'; // image container
      //'<img src ="'+trial.prompt+ '" id="jspsych-image-slider-2AFC-"></img>';

      for (i = 0; i < trial.stimulus.length; i++) {
        html += '<div style="display: flex;align-self: center;';

        for (s in style) {
          html += s + ':' + style[s] + ';';

        }
        html += '">';

        // can use image-unselected class to specify the look of images before
        // a selection has been made (in combination with image-selected classes)
        // if providing visual feedback.
        html += '<img src="' + trial.stimulus[i] + '" id="jspsych-image-selector-' + i +
          '" class="image-unselected" style="position: relative; display: flex" index=' + i + '></img>';

        if (i==0) {
          html += '<div id="countdown-number" style="color:gray"></div> <svg><circle r = "18" cx = "20" cy = "20" style="stroke:transparent"></circle></svg>';
          };
        if (trial_data.image_click == 0 & i == 0) {
          html += '<div style="align-self: center; position: absolute; margin-left:6.5em">' + '<font size="10">' + trial.left_pay + '</font></div>';
        } else if (trial_data.image_click == 1 & i == 1) {
          html += '<div style="align-self: center; position: absolute; margin-left:6.5em">' + '<font size="10">' + trial.right_pay + '</font></div>';
        }
        html += '</div>';
      }
      //  html += '<class="centered">'+trial.right_pay;
      html += '</div>'; // end image container

      html += '<div class="large"; style="display: grid"> <font size="6">' + trial_no + '</font></div>'
      //add bar
      //bar width
      //  var points = global.points
      let root = document.documentElement;
      var scaled_points = points / trial.goal * 100;
      // console.log(trial.trial_no == trial.trial_max);
      // console.log(trial.trial_no);
      // console.log(trial.trial_max);
      root.style.setProperty('--width', scaled_points);

      //goal:

      html += '<div class="progress-bar">';
      //html += points;
      //  html +=  '<div class="w3-green" style="width:500px"></div>';
      html += '</div><br>';


      return html;
    };

    function show_final_fb() {
      var points_total = '<font size="6">End of game. Your score is ' + '<font color="green">' + (points + points2) + '</font>' + ' points</font>';

      var html = '<div>' + points_total + '</div>';
      return html;
    };

    //get data
    var trial_data = {};

    // create response function
    var after_response = function(info) {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      var correct = (trial.target_image_index == info.index)

      if (info.index == 0 & trial.MBleft == 1 ) { //
        points += trial.left_pay;
      } else if (info.index == 1 & trial.MBleft == 1) {
        points2 += trial.right_pay;
      } else if (info.index == 0 & trial.MBleft == 0) {
        points2 += trial.left_pay;
      } else if (info.index == 1 & trial.MBleft == 0 ) {
        points += trial.right_pay;
      };

      if (points>trial.goal) {
        console.log('yea');
        points=trial.goal;
      };
      // save data
      trial_data = {
        "rt": info.rt,
        "correct": correct,
        "stimulus": trial.stimulus,
        "image_click": info.index,
        "points": points,
        "points2": points2
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

       if (trial.do_feedback) {
        // show image during feedback if flag is set
        if (trial.trial_no === trial.trial_max) {
          trial.feedback_duration *= 3;
          display_element.innerHTML = show_fb();
          display_element.innerHTML += show_final_fb();
        } else if (timeout && !trial.show_feedback_on_timeout) {
          trial.feedback_duration *= 2;
          display_element.innerHTML += '<font size="18"' + trial.timeout_message + '</font>';
        } else if (trial.show_stim_with_feedback) {
          display_element.innerHTML = show_fb(); //change to show_images2
        };

      };


      // check if force correct choice  is set
      if (trial.force_correct_button_press && correct === false && ((timeout && trial.show_feedback_on_timeout) || !timeout)) {
        // not implemented
      } else {
        jsPsych.pluginAPI.setTimeout(function() {
          endTrial();
        }, trial.feedback_duration);
      };

    };

    function endTrial() {
      display_element.innerHTML = '';
      jsPsych.finishTrial(trial_data);
    };

  };

  return plugin;
})();

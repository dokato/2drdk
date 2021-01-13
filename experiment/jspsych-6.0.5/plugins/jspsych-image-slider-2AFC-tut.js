/**
 * jspsych-image-slider-response
 * a jspsych plugin for free response survey questions
 *
 * Josh de Leeuw
 *
 * documentation: docs.jspsych.org
 *
 */


jsPsych.plugins['image-slider-2AFC-tut'] = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('image-slider-2AFC-tut', 'stimulus', 'image');

  plugin.info = {
    name: 'image-slider-2AFC-tut',
    description: '',
    parameters: {
      stimulus: {
        type: jsPsych.plugins.parameterType.IMAGE,
        pretty_name: 'Stimulus',
        array: true,
        default: undefined,
        description: 'The image to be displayed'
      },
      min: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Min slider',
        default: 0,
        description: 'Sets the minimum value of the slider.'
      },
      max: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Max slider',
        default: 100,
        description: 'Sets the maximum value of the slider',
      },
      start: {
				type: jsPsych.plugins.parameterType.INT,
				pretty_name: 'Slider starting value',
				default: 50,
				description: 'Sets the starting value of the slider',
			},
      step: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Step',
        default: 1,
        description: 'Sets the step of the slider'
      },
      labels: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name:'Labels',
        default: [],
        array: true,
        description: 'Labels of the slider.',
      },
      button_label: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label',
        default:  'Confirm',
        array: false,
        description: 'Label of the button to advance.'
      },
      prompt: {
        type: jsPsych.plugins.parameterType.IMAGE,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed below the slider.'
      },
      stimulus_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Stimulus duration',
        default: null,
        description: 'How long to hide the stimulus.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show the trial.'
      },
      response_ends_trial: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Response ends trial',
        default: true,
        description: 'If true, trial will end when user makes a response.'
      },
    }
  }

  plugin.trial = function(display_element, trial) {

    trial.default_image_style = {
      border: '5px solid',
      display: 'flex',
      margin: '10px',
      padding: '8px',
      color: '#D3D3D3',
    }
    var style = trial.default_image_style;
    var border_style = (trial.show_border) ?
                            'border:' + style.border +';': 'border: none;';
   // var html = ''//'<div style="margin: 10px 0px;">'; //id="jspsych-image-slider-response-wrapper" +
   //if (trial.prompt !== null){
   var html = "<img src='judgeS.png', height='100px'></img>";

   //  }

    html += '<div style="display: ' + style.display + ';">'; // image container



    //html += '<div id="jspsych-image-slider-response-stimulus"><img src="' + trial.stimulus + '"></div>';
    var marg='style="width:500px;"' //set up var for which margin to add for image
    for(i=0;i<trial.stimulus.length;i++) {

        if (i==0) {
        html += '<div style="display:flex;align-self: center; '; //display:flex;align-self: center;
       } else {
        marg = 'style="width:500px;"';
        html += '<div style="display:flex;align-self: center; ';
       }

        for(s in style) {
          html += s + ':' + style[s] + ';';
        }
        html += '">';

        // can use image-unselected class to specify the look of images before
        // a selection has been made (in combination with image-selected classes)
        // if providing visual feedback.
        html += '<img ' + marg + ' src="' + trial.stimulus[i] + '" id="jspsych-image-selector-' + i
                              + '" class="image-unselected" index='+i+'></img>';
        html += '</div>';
        if (i==0){
          html += '<div><img class="symbol" style="opacity:1" src ="'+trial.prompt+ '"></img></div>';
        }
      }
      html += '</div>'; // end image container


    html += '<div>'
    //for(var j=0; j < trial.labels.length; j++){
     // var width = 100/(trial.labels.length-1);
     // var left_offset = (j * (100 /(trial.labels.length - 1))) - (width/2);
     // html += '<div style="display: inline-block; position: absolute; left:'+left_offset+'%; text-align: center; width: '+width+'%;">';
     // html += '<span style="text-align: center; font-size: 80%;">'+trial.labels[j]+'</span>';
     // html += '</div>'
    //}
    html += '</div>';
    html += '</div>';
    html += '</div>';

    html += '<div class="jspsych-image-slider-response-container" style="position:relative; top:20px">';
    html += '<input type="range" class="slider" value="'+trial.start+'" min="'+trial.min+'" max="'+trial.max+'" step="'+trial.step+'" onkeydown="event.preventDefault()" id="jspsych-image-slider-response-response"></input>';
     // add submit button
    html += '<button id="jspsych-image-slider-response-next" class="jspsych-btn" style="position:relative; top:25px">'+trial.button_label+'</button>';

      //add scale
   // html +=
    display_element.innerHTML = html;

    var response = {
      rt: null,
      response: null
    };


    display_element.querySelector('#jspsych-image-slider-response-next').addEventListener('click', function() {
      // measure response time
      var endTime = (new Date()).getTime();
      response.rt = endTime - startTime;
      response.response = display_element.querySelector('#jspsych-image-slider-response-response').value;

      if(trial.response_ends_trial){
        end_trial();
      } else {
        display_element.querySelector('#jspsych-image-slider-response-next').disabled = true;
      }

    });
    //add listerer to 1st slider click
    display_element.querySelector('#jspsych-image-slider-response-response').addEventListener('click', function() {
      // measure response time
      var endTime = (new Date()).getTime();
      response.click1_rt = endTime - startTime;
      response.click1_val = display_element.querySelector('#jspsych-image-slider-response-response').value;

      //if(trial.response_ends_trial){
       // end_trial();
      //} else {
       // display_element.querySelector('#jspsych-image-slider-response-response').disabled = true;
     // }

    });

    function end_trial(){

      jsPsych.pluginAPI.clearAllTimeouts();

      // save data
      var trialdata = {
        "rt": response.rt,
        "response": response.response,
        "first_click_rt": response.click1_rt,
        "first_click_val": response.click1_val
      };

      display_element.innerHTML = '';

      // next trial
      jsPsych.finishTrial(trialdata);
    }

    if (trial.stimulus_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        display_element.querySelector('#jspsych-image-slider-response-stimulus').style.visibility = 'hidden';
      }, trial.stimulus_duration);
    }

    // end trial if trial_duration is set
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.trial_duration);
    }

    var startTime = (new Date()).getTime();
  };

  return plugin;
})();

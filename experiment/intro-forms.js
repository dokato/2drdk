const info_sheet = "<div style='background: #d3d3d3;padding: 20px; font-size: 14px;'>" +
"<h2>General information sheet</h4>"+
"<b>Introduction.</b> You are being invited to take part in a research study. "+
"Before you decide it is important for you to understand why the research is being done and what it will involve. "+
"Please take time to read the following information carefully and discuss it with others if you wish. " +
"You are free to take as much time as you like to decide whether you wish to participate."+
"<br>"+
"<b>What is the purpose of the study?</b> The aim of this research is to understand more about how "+
"the human brain makes simple decisions."+
"<br>"+
"<b>Why have I been chosen?</b> As a volunteer you responded to our request for healthy adult subjects to participate in the study."+
"<br>"+
"<b>Who is organizing this study?</b> This study is organized by researchers at the School of Psychology, Cardiff University."+
"<br>"+
"<b>Do I have to take part?</b> It is up to you to decide whether or not to take part. "+
"If you do decide to take part, you will be asked to sign the consent form on the next page. " +
"If you decide to take part, you are still free to withdraw at any time and without giving a reason."+
"<br>"+
"<b>What does the general procedure involve?</b> "+
"Participants will be invited to complete some surveys and behavioural experiments online, "+
"using a computer with internet access and a keyboard or a mouse to respond. "+
"You would perform some psychological tests of decision making, after careful instruction and a chance to practice. "+
"Typically, participants would see dots moving on the screen and they have to decide towards which platform (red or blue) the dots are moving."+
"The experiment consists of 2 parts. The participants might get qualified to part 2 based on their performance from the part 1. "+
"Specific instructions will be given before each task. "+
"These tests do not use distressing material and are not designed to be stressful or to catch you out."+
"<br>"+
"<b>What are the possible benefits of taking part? </b>Since we are only studying healthy volunteers, there is no intended "+
"clinical benefit to you from taking part in this study. "+
"<br>"+
"<b>Are the procedure and results confidential?</b> All information that is collected about you during the course of this research will be kept anonymous. "+
"Demographic information (age, gender, etc.) will be paired with participants' IDs, "+
"which are not identifiable or traceable to individuals. "+
"We may share the anonymized research data we collect with other researchers. However, any shared data will not contain any personal "+
"information so that you cannot be recognised from it. In any sort of report we might publish we will "+
"not include information that will make it possible for other people to know your name or identify you in any way."+
"<br>The information provided will be held in compliance with GDPR regulations. Cardiff University is "+
"the Data Controller and is committed to respecting and protecting your personal data in "+
"accordance with your expectations and Data Protection legislation. The University has a Data "+
"Protection Officer who can be contacted at <i>inforequest@cardiff.ac.uk</i>. Further information about "+
"Data Protection, including your rights and details about how to contact the Information "+
"Commissioner’s Office should you wish to complain, can be found at the following: "+
"<i>https://www.cardiff.ac.uk/public-information/policies-and-procedures/data-protection.</i> "+
"<br>"+
"<b>What will happen to the results of the research study? </b>"+
"When data from volunteers are collected, they will be analysed and written up for publication in a "+
"scientific journal. Where appropriate, the results of this study will be presented at scientific "+
"conferences and the media. You will not be identified in any report or publication. "+
"<br>"+
"<b>Who has reviewed the study?</b> This study has been reviewed and approved by the Cardiff University School of Psychology Ethics Committee."+
"<br>"+
"<b>Contact for Further Information: </b> Dominik Krzeminski (<i>krzeminskidk@cardiff.ac.uk</i>)" +
"<br><br>Press <b>SPACE</b> to proceed</div>" + "</div>"


const demographic_form = "<div style='background: #d3d3d3;padding: 20px;'>" +
  "<p> Select your gender</p>"+
  '<div>' +
 '  <input type="radio" id="female" name="gender" value="female">' +
  '  <label for="female">female</label></div> ' +
  '<div>'+
  '  <input type="radio" id="male" name="gender" value="male">' +
  ' <label for="male">male</label></div>'+
  '<div>' +
  '  <input type="radio" id="other" name="gender" value="other">' +
    '<label for="other">other</label></div>'+
  "<br><p> Select your age</p>" +
   "<input name='age' type='number' min='18'/>"+
  "<p> Select your handedness</p>"+
  '<div>' +
  '  <input type="radio" id="right" name="hand" value="right">' +
  '  <label for="right">right-handed</label></div> ' +
  '<div>'+
  '  <input type="radio" id="left" name="hand" value="left">' +
  ' <label for="left">left-handed</label></div>'+
  '<div>' +
  '  <input type="radio" id="both" name="hand" value="both">' +
    '<label for="both">ambidextrous (both-handed)</label></div>'+
    "<p>If you signed up though Prolific, please provide your Prolific ID "+
    '<div>' +
    '  <input type="text" id="mail" name="mail" size="35">' +
    '</div></div>'


var consent_ops = ['<b>Yes</b>']

var consent_panel = {
      preamble: '<h4>Informed consent</h4>All fields necessary to participate - ' +
      "<u><i>if you do not agree with any of the statements, please exit the experiment by"+
      " closing the browser window.</u></i>",
      type: 'survey-multi-choice',
      questions: [
        {prompt: "I confirm that I have read, understood and accept the conditions contained in the information sheet for the above study and have had the opportunity to ask questions. ", options: consent_ops, required:true, horizontal:true},
      {prompt: "I confirm that the nature of the experiment has been explained to me and that I have agreed to take part the above study. ", options: consent_ops, required:true, horizontal:true},
      {prompt: "I agree that the scientific data from this experiment will be stored on a computer and may contribute to scientific papers and presentations. This data will not be linked to me as an individual in any papers or presentations.", options: consent_ops, required:true, horizontal:true},
      {prompt: "I understand that my participation is voluntary and that I am free to withdraw at any time, without giving any reason.", options: consent_ops, required:true, horizontal:true},
      {prompt: "I consent that the fully anonymised scientific data from this experiment may be shared with other researchers. This anonymised data will not be linked to me as an individual.", options: consent_ops, required:true, horizontal:true},
       ],
    };
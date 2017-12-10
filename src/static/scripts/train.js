// fork getUserMedia for multiple browser versions, for the future
// when more browsers support MediaRecorder

navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);

// set up basic variables for app

var record = document.querySelector('.record');
var stop = document.querySelector('.stop');
var finish = document.querySelector('.finish');
var send = document.querySelector('.send');
var soundClips = document.querySelector('.sound-clips');
var canvas = document.querySelector('.visualizer');
var test = document.querySelector('.test');
var quit = document.querySelector('.quit');

var CurrAudio = null;
var clipsSent = 0;

//var trainingArticle = document.getElementById('train');
var trainingIdx =0;
displayTrainingArticle(trainingIdx);

// disable stop button while not recording

stop.disabled = true;

// visualiser setup - create web audio api context and canvas

var audioCtx = new (window.AudioContext || webkitAudioContext)();
var canvasCtx = canvas.getContext("2d");

//main block for doing the audio recording
var constraints = { audio: true };
var encoder = new WavAudioEncoder(44100, 1);

audioContext = new AudioContext;

if (audioContext.createScriptProcessor == null) {
  audioContext.createScriptProcessor = audioContext.createJavaScriptNode;
}

var recorder;

if (navigator.getUserMedia) {
  console.log('getUserMedia supported.');

  var chunks = [];

  var onSuccess = function(stream) {
    var mediaRecorder = new MediaRecorder(stream);
    getsamplecount("gary");

    visualize(stream);
    
    var audioCon = new AudioContext();
    var source = audioCon.createMediaStreamSource(stream);
    //source.connect(audioCon.destination);
    recorder = new WebAudioRecorder(source, {
      workerDir: "static/worker/",     // must end with slash
      numChannels: 1,
      encoding: "wav"
    });
    recorder.setOptions({
      encodeAfterRecord: true
    })
    //recorder.onEncoderLoading = function(recorder, encoding) { ... }
    //recorder.onEncoderLoaded = function(recorder, encoding) { ... }
    //recorder.onTimeout = function(recorder) { ... }
    //recorder.onEncodingProgress = function (recorder, progress) { ... }
    //recorder.onEncodingCanceled = function(recorder) { ... }
    recorder.onComplete = function(recorder, blob) {
      CurrAudio = blob;
      console.log("Completed Encoding");
    }
    //recorder.onError = function(recorder, message) { ... }

    record.onclick = function() {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      console.log("recorder started");
      record.style.background = "red";
      stop.disabled = false;
      record.disabled = true;

      console.log("training article value reset");
      
      recorder.startRecording()
    }

    stop.onclick = function() {
      console.log("stopping");
      mediaRecorder.stop();
      console.log(mediaRecorder.state);
      console.log("recorder stopped");
      record.style.background = "";
      record.style.color = "";
      // mediaRecorder.requestData();

      stop.disabled = true;
      record.disabled = false;
      
      recorder.finishRecording()
    }
    
    send.onclick = function() {
      trainingIdx++;
      displayTrainingArticle(trainingIdx);
      sendPhoneme("gary", CurrAudio);
      clipsSent++;
      while (soundClips.firstChild) {
        soundClips.removeChild(soundClips.firstChild);
      }
    }

    finish.onclick = function() {
      var val = true;
      var recc = 25;
      if (clipsSent < recc) {
        val = confirm('You have not recorded enough audio (' + clipsSent + '/' + recc + ') Are you sure you want to submit for training?');
      }
      else {
        val = confirm('You have recorded (' + clipsSent + '/' + recc + ') Are you sure you want to submit for training?');
      }
      if (val) {
        traincall("gary", CurrAudio);
      }
    }

    quit.onclick = function() {
      window.location.href = '/home';
    }

    mediaRecorder.onstop = function(e) {
      console.log("data available after MediaRecorder.stop() called.");

      var clipName = 'Recording';//prompt('Enter a name for your sound clip?','My unnamed clip');
      console.log(clipName);
      var clipContainer = document.createElement('article');
      var clipLabel = document.createElement('p');
      var audio = document.createElement('audio');
      var deleteButton = document.createElement('button');
     
      clipContainer.classList.add('clip');
      audio.setAttribute('controls', 'controls');
      deleteButton.textContent = 'Delete';
      deleteButton.className = 'delete';

      if(clipName === null) {
        clipLabel.textContent = 'My unnamed clip';
      } else {
        clipLabel.textContent = clipName;
      }

      clipContainer.appendChild(audio);
      clipContainer.appendChild(clipLabel);
      //clipContainer.appendChild(deleteButton);
      while (soundClips.firstChild) {
        soundClips.removeChild(soundClips.firstChild);
      }
      soundClips.appendChild(clipContainer);

      audio.controls = true;
      var blob = new Blob(chunks, { 'type' : 'audio/wav;' });
      CurrAudio = blob;//new Blob(chunks, { 'type' : 'string;' });;
      chunks = [];
      var audioURL = window.URL.createObjectURL(blob);
      audio.src = audioURL;
      
      console.log("recorder stopped");

      deleteButton.onclick = function(e) {
        evtTgt = e.target;
        evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
      }
      clipLabel.onclick = function() {
        var existingName = clipLabel.textContent;
        var newClipName = prompt('Enter a new name for your sound clip?');
        if(newClipName === null) {
          clipLabel.textContent = existingName;
        } else {
          clipLabel.textContent = newClipName;
        }
      }
    }

    mediaRecorder.ondataavailable = function(e) {
      chunks.push(e.data);
    }
  }

  var onError = function(err) {
    console.log('The following error occured: ' + err);
  }

  navigator.getUserMedia(constraints, onSuccess, onError);
} else {
   console.log('getUserMedia not supported on your browser!');
}

function visualize(stream) {
  var source = audioCtx.createMediaStreamSource(stream);

  var analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  var bufferLength = analyser.frequencyBinCount;
  var dataArray = new Uint8Array(bufferLength);

  source.connect(analyser);
  //analyser.connect(audioCtx.destination);
  
  WIDTH = canvas.width;
  HEIGHT = canvas.height;

  draw()

  function draw() {

    requestAnimationFrame(draw);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(73, 207, 255)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 5;
    canvasCtx.strokeStyle = 'rgb(255, 255, 10)';

    canvasCtx.beginPath();

    var sliceWidth = WIDTH * 1.0 / bufferLength;
    var x = 0;


    for(var i = 0; i < bufferLength; i++) {
 
      var v = dataArray[i] / 128.0;
      var y = v * HEIGHT/2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();

  }
}


function getsamplecount(user) {
  var urlBase = 'api/numsamples';
  var url = [
    urlBase,
    "/",
    user,
  ].join('');

  $.ajax({
    url : url,
    type: 'GET',
    success : handledata
  })
  function handledata(data) {
    clipsSent = parseInt(data);
  }

}

function traincall(user) {
  var urlBase = 'api/train';
  var url = [
    urlBase,
    "/",
    user,
  ].join('');

  $.ajax({
    url : url,
    type: 'POST',
    success : handledata
  })
  function handledata(data) {
    console.log(data);
  }

  window.location.href = '/home';

}

function sendPhoneme(speaker, audio) {
  var urlBase = 'api/addtraindata';
  var url = [
    urlBase,
    "/",
    speaker,
  ].join('');
  


  var fd = new FormData();
  fd.append('file', audio);
  $.ajax({
    type: 'POST',
    url: url,
    data: fd,
    processData: false,
    contentType: false
  }).done(function(data) {
    console.log(data);
  });
  
}


function playaudio(speaker, txt) {
  var urlBase = 'api/tts';
  var url = [
    urlBase,
    "/",
    speaker,
  ].join('');

  $.ajax({
    url : url,
    type: 'GET',
    data: txt,
    success : handledata
  })
  
  function handledata(data) {
    console.log(data);
    console.log("Playing: " + txt)
    var audio = new Audio(data);
    audio.play();
  }
}

function displayTrainingArticle(idx){
  var articles = ["article 1", "article 2", "article 3"];
  //var index = idx % (articles.length);
  var index = idx % (articleText.length);
  if (idx > 0) {
    document.getElementById('train').innerHTML = '<p  class="animated fadeOutRight"><font size="5" style="color:#0b2b5e;"><b>' + articleText[index-1] + '</b></font></p>'; //articleList[index];
  }
  console.log("display Training Article: " + idx);
  setTimeout(function (){

  // Something you want delayed.
    document.getElementById('train').innerHTML = '<p  class="animated fadeInRight"><font size="5" style="color:#0b2b5e;"><b>' + articleText[index] + '</b></font></p>'; //articleList[index];

  }, 1000);
   //trainingArticle.textContent = "hello word! this is the text to train";
}


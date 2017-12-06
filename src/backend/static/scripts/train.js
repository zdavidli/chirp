// fork getUserMedia for multiple browser versions, for the future
// when more browsers support MediaRecorder

navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);

// set up basic variables for app

var record = document.querySelector('.record');
var stop = document.querySelector('.stop');
var accept = document.querySelector('.accept');
var soundClips = document.querySelector('.sound-clips');
var canvas = document.querySelector('.visualizer');
var test = document.querySelector('.test');

var CurrAudio = null;


//var trainingArticle = document.getElementById('train');
var trainingIdx =0;

// disable stop button while not recording

stop.disabled = true;

// visualiser setup - create web audio api context and canvas

var audioCtx = new (window.AudioContext || webkitAudioContext)();
var canvasCtx = canvas.getContext("2d");

//main block for doing the audio recording

if (navigator.getUserMedia) {
  console.log('getUserMedia supported.');

  var constraints = { audio: true };
  var chunks = [];

  var onSuccess = function(stream) {
    var mediaRecorder = new MediaRecorder(stream);

    visualize(stream);

    record.onclick = function() {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      console.log("recorder started");
      record.style.background = "red";
      stop.disabled = false;
      record.disabled = true;

      displayTrainingArticle(trainingIdx);
      trainingIdx++;
      console.log("training article value reset");
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
    }
    
    accept.onclick = function() {
      sendPhoneme("gary", CurrAudio);
    }
    
    test.onclick = function() {
      console.log("Test");
      playaudio("gary", "test sentence scott is the best");
    }

    mediaRecorder.onstop = function(e) {
      console.log("data available after MediaRecorder.stop() called.");

      var clipName = prompt('Enter a name for your sound clip?','My unnamed clip');
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
      clipContainer.appendChild(deleteButton);
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

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

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

function sendPhoneme(speaker, audio) {
  var urlBase = 'addtraindata';
  var url = [
    urlBase,
    "/",
    speaker,
  ].join('');
  
  //var arrayBuffer;
  //var fileReader = new FileReader();
  //fileReader.onload = function() {
  //  arrayBuffer = this.result;
  //  console.log(arrayBuffer);
  //};
  //fileReader.readAsArrayBuffer(audio);
  
  
  var formData = new FormData();
  
  var fd = new FormData();
  fd.append('fname', 'test.wav');
  var file = new File([audio], "name");
  fd.append('file', file);
  $.ajax({
    type: 'POST',
    url: url,
    data: fd,
    processData: false,
    contentType: false
  }).done(function(data) {
    console.log(data);
  });
  
  //$.ajax({
  //  url : url,
  //  type: 'POST',
  //  data: formData,
  //  processData: false,
  //  contentType: false,
  //  success : handledata
  //})
  //
  //
  //function handledata(data) {
  //  console.log(data);
  //}
  ///////////////////////////////////////////
}

function send(audio) {
  
}

function playaudio(speaker, txt) {
  var urlBase = 'tts';
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
    console.log("Playing: " + str(txt))
    var audio = new Audio(data);
    audio.play();
  }
}

function displayTrainingArticle(idx){
  var articles = ["article 1", "article 2", "article 3"];
  //var index = idx % (articles.length);
  var index = idx % (articleText.length);
  console.log("display Training Article");
  document.getElementById('train').innerHTML = articleText[index]; //articleList[index];
   //trainingArticle.textContent = "hello word! this is the text to train";
}


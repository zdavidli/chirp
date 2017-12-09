navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);

// set up basic variables for app
var canvas = document.querySelector('.visualizer');
var train = document.querySelector('.train');
train.onclick = function() {
  console.log("Test");
  window.location.href = '/train';
  //playaudio("gary", "test sentence scott is the best");
}

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var remainingAudio = 0;
var delay = 2000;
var prevTweet = "";
var tweet = "";
var playing = false;
setInterval(ttsRoutine, 2000);
function ttsRoutine() {
  console.log("Checking for new tweet");
  if (!playing) {
    prevTweet = tweet;
    tweet = getnexttweet("gary");
    if (tweet != prevTweet) {
      playaudio("gary", tweet);
    }
  } 
  
}

function getnexttweet(auth) {
  //var urlBase = 'api/tts';
  //var url = [
  //  urlBase,
  //  "/",
  //  speaker,
  //].join('');
//
  //$.ajax({
  //  url : url,
  //  type: 'GET',
  //  data: txt,
  //  success : handledata
  //})
  //
  //function handledata(data) {
  //  console.log(data);
  //}
  return "If you dont take risks, youll always have regret.";
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
    //var a = document.createElement("AUDIO");
    //a.src = data;
    var audio = new Audio(data);
    audio.addEventListener("ended", function(){
      playing = false;
      console.log("ended");
    });
    audio.play();
    //a.load();
    //a.play();
    playing = true;

    //visualize(audio.captureStream());
  }
}

// visualiser setup - create web audio api context and canvas

//var audioCtx = new (window.AudioContext || webkitAudioContext)();
//var canvasCtx = canvas.getContext("2d");
//
//if (navigator.getUserMedia) {
//  console.log('getUserMedia supported.');
//
//  var constraints = { audio: true };
//  var chunks = [];
//
//  var onSuccess = function(stream) {
//    var mediaRecorder = new MediaRecorder(stream);
//
//    visualize(stream);
//
//    
//    
//  }
//
//  var onError = function(err) {
//    console.log('The following error occured: ' + err);
//  }
//
//  navigator.getUserMedia(constraints, onSuccess, onError);
//} else {
//   console.log('getUserMedia not supported on your browser!');
//}

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

    canvasCtx.fillStyle = 'rgb(0, 188, 255)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 8;
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

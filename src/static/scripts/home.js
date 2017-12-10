navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);

// set up basic variables for app
var canvas = document.querySelector('.visualizer');
var train = document.querySelector('.train');

var getTweets = true;

var handle = undefined;
login();
// Obtain the handle
function login() {
  var urlBase = 'api/user_id';
  var url = [
   urlBase,
  ].join('');

  $.get({
   url : url,
   type: 'GET',
   success : handledata
  })
  function handledata(data) {
    console.log(data);
    handle = data;
    istraining(handle);
    ttsRoutine();
  }
}
//<blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/gamespot/status/939978080113872900"></a></blockquote>

//<blockquote class="twitter-tweet tw-align-center" lang="en"><p>If you don&#39;t take risks, you&#39;ll always have regret. <a href="https://twitter.com/search?q=%23justdoit&amp;src=hash">#justdoit</a></p>&mdash; Nike (@Nike) <a href="https://twitter.com/Nike/statuses/476008225859706880">June 9, 2014</a></blockquote>

train.onclick = function() {
  console.log("Test");
  window.location.href = '/train';
  //playaudio(handle, "test sentence scott is the best");
}

var delay = 60000;
var tweet = "";
var playing = false;
var requesting = false;
var queue = new Queue();
var used = new Queue();
setInterval(ttsRoutine, delay);
var attempts = 0;
var numTweets = 30;

function ttsRoutine() {
  if (!getTweets) {
    return;
  }
  if (handle == undefined) {
    return;
  }
  console.log("Checking for new tweet");
  attempts++;
  if (attempts % 10 == 1) {
    istraining(handle);
  }
  getnexttweets(handle);
  processqueue()
}

function processqueue() {
  console.log("Processing Queue");
  if (!playing && !requesting) {
    if (!queue.isEmpty()) {
      console.log("Queue is not empty!");
      tweet = queue.dequeue();
      used.enqueue(tweet);
      if (used.getLength() > 20) {
        used.dequeue();
      }
      setfeed(tweet);
      playaudio(handle, tweet);
    }
  }
}

// <blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/43815496/status/939975621513375700"></a></blockquote><blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/17217640/status/939974985988431900"></a></blockquote>

// <blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/elonmusk/status/937402084692975616"></a></blockquote>
//               <blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/elonmusk/status/938972633416306690"></a></blockquote>
//               <blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/elonmusk/status/937447589460426752"></a></blockquote>
//               <blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/elonmusk/status/937411489635241984"></a></blockquote>
//               <blockquote class="twitter-tweet tw-align-center" lang="en"><a href="https://twitter.com/elonmusk/status/937401166299774976"></a></blockquote>

function setfeed(tweet) {
  var tweetstoshow = 2;
  if (used.getLength() < tweetstoshow) {
    tweetstoshow = used.getLength();
  }
  var str = "";
  //str += "<blockquote class=\"twitter-tweet tw-align-center\" lang=\"en\"><a href=\"https://twitter.com/" + tweet.user.id + "/status/" + tweet.id;
  for (var i = 0; i < tweetstoshow; ++i) {
    var t = queue.get(i);
    str += "<blockquote class=\"twitter-tweet tw-align-center\" lang=\"en\"><a href=\"https://twitter.com/" + t.user.screen_name + "/status/" + t.id+ "\"></a></blockquote>";
  }
  //console.log(str);
  str += "<script async src=\"//platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>"
  str = "<blockquote class=\"twitter-tweet tw-align-center\" lang=\"en\"><a href=\"https://twitter.com/elonmusk/status/937402084692975616\"></a></blockquote>"
  document.getElementById('feed').innerHTML = str;
}

function getnexttweets(auth) {
  var urlBase = 'api/feed';
  var url = [
   urlBase,
   "/",
   numTweets,
  ].join('');

  $.ajax({
   url : url,
   type: 'GET',
   success : handledata
  })

  
  function handledata(data) {
    //console.log(data);
    var obj = JSON.parse(data);
    console.log(obj[0]);
    for (var i = 0; i < numTweets; ++i) { //TODO reverse order
      var t = obj[i];
      if (queue.getLength() > 100 || queue.contains(t) || used.contains(t)) {
        break;
      }
      else {
        queue.enqueue(t);
      }
    }
    console.log(queue.getLength());
    processqueue();
  }
  //queue.enqueue("Harold son, you are my herald, my son.");
}


function playaudio(speaker, tweet) {
  requesting = true;
  var txt = tweet.text;
  var usr = tweet.user.id;
  console.log("text: " + txt)
  console.log("user: " + usr)
  var urlBase = 'api/tts';
  var url = [
    urlBase,
    "/",
    speaker,
  ].join('');

  $.ajax({
    url : url,
    type: 'GET',
    data: {message:txt},
    success : handledata,
    error: err
  })
  
  function handledata(data) {
    console.log(data);
    requesting = false;
    console.log("Playing: " + txt)
    //Delay for generation
    setTimeout(function (){
      //random number for cache-busting!
      var randn = Math.floor(Math.random() * 100000000);
      var audio = new Audio(String(data) + "?" + String(randn));
      audio.addEventListener("ended", function(){
        playing = false;
        console.log("ended");
        processqueue();
      });
      audio.play();
      playing = true;
    }, 1000);
    

    //visualize(audio.captureStream());
  }

  function err(xhr) {
    playing = false;
    requesting = false;
    processqueue();
  }
}

function istraining(speaker) {
  var urlBase = 'api/istraining';
  var url = [
    urlBase,
    "/",
    speaker,
  ].join('');

  $.ajax({
    url : url,
    type: 'GET',
    success : handledata
  })
  
  function handledata(data) {
    console.log(data);
    var img = document.getElementById('load');
    if (data == "true") {
      img.style.visibility = 'visible';
    }
    else {
      img.style.visibility = 'hidden';
    }
  }
}

// visualiser setup - create web audio api context and canvas

var audioCtx = new (window.AudioContext || webkitAudioContext)();
var canvasCtx = canvas.getContext("2d");

if (navigator.getUserMedia) {
 console.log('getUserMedia supported.');

 var constraints = { audio: true };
 var chunks = [];

 var onSuccess = function(stream) {
   var mediaRecorder = new MediaRecorder(stream);

   visualize(stream);

   
   
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

    canvasCtx.fillStyle = 'rgb(0, 188, 255)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 4;
    //canvasCtx.strokeStyle = 'rgb(255, 255, 10)';
    canvasCtx.strokeStyle = 'rgb(49, 232, 255)';

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

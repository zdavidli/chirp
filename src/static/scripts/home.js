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
    handle = data;
    istraining(handle);
    ttsRoutine();
  }
}
train.onclick = function() {
  window.location.href = '/train';
  //playaudio(handle, "test sentence scott is the best");
}

var delay = 62000;
var tweet = undefined;
var playing = false;
var requesting = false;
var queue = new Queue();
var used = [];
setInterval(ttsRoutine, delay);
var attempts = 0;
var numTweets = 10;

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
}

function processqueue() {
  console.log("Processing Queue");
  if (!playing && !requesting) {
    if (!queue.isEmpty()) {
      tweet = queue.dequeue();
      used.push(tweet);
      playaudio(handle, tweet);
    }
  }
  setfeed(tweet);
}

// <ul> 
//   <li>
//     <div class="box" style="margin-bottom: 10px;">
//       <p align="left" style="margin-bottom: 10px;"><font size="5" style="color:#1343ae;">@RealDolandsRump</font></p>
//       <p align="left"><font size="3" style="color:#2363be;">Gyna</font></p>
//     </div>
//   </li>
//   <li>
//     <div class="box" style="margin-bottom: 10px;">
//       <p align="left" style="margin-bottom: 10px;"><font size="5" style="color:#1343ae;">@RealDolandsRump</font></p>
//       <p align="left"><font size="3" style="color:#2363be;">Gyna</font></p>
//     </div>
//   </li>
// </ul>

function setfeed(tweet) {
  var tweetstoshow = 10;
  if (used.length < tweetstoshow) {
    tweetstoshow = used.length;
  }
  var str = "<ul>";

  var t = undefined;
  //str += "<blockquote class=\"twitter-tweet tw-align-center\" lang=\"en\"><a href=\"https://twitter.com/" + tweet.user.id + "/status/" + tweet.id;
  for (var i = 0; i < tweetstoshow; ++i) {
    t = used[used.length - i - 1];
    str += "<li><div class=\"box\" style=\"margin-bottom: 10px;\"><p align=\"left\" style=\"margin-bottom: 10px;\"><font size=\"5\" style=\"color:#1343ae;\">";
    str += t.user.name;

    str += " </font><font size=\"3\" style=\"color:#666666;\"> @"
    str += t.user.screen_name
    str += "</p><p align=\"left\"><font size=\"3\" style=\"color:#2363be;\">"
    str += t.text;
    str += "</font></p></div></li>";
  }
  //console.log(str);
  str += "</ul>"
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
   success : handledata,
   err: err
  })

  
  function handledata(data) {
    console.log("Got tweets");
    var obj = JSON.parse(data);
    console.log(obj[0]);
    console.log("converted json");
    if (attempts == 1) {
      queue.enqueue(obj[0]);
      for (var i = 1; i < numTweets; ++i) {
        used.push(obj[obj.length - i]);
      }
    }
    else {
      console.log("calculating new tweets");
      var prequeue = [];
      for (var i = 0; i < numTweets; ++i) {
        console.log(i);
        if (obj[i].id == used[used.length - 1].id) {
          console.log("New tweet count: " + i);
          break;
        }
        prequeue.push(obj[i]);
      }
      while (prequeue.length != 0) {
        queue.enqueeu(prequeue.pop())
      }
      console.log("Finished calculating");

      // var i = numTweets - 1;
      // while (used.peek().id != obj[i]) {
      //   i--;
      // }
      // console.log(i);
      // while (--i >= 0) {
      //   queue.enqueue(obj[i]);
      // }


      //for (var i = numTweets - 1; i >= 0; --i) { //TODO reverse order
      //  var t = obj[i];
      //  if (queue.getLength() > 100 || queue.contains(t) || used.contains(t)) {
      //    break;
      //  }
      //  else {
      //    queue.enqueue(t);
      //  }
      //}
    }
    console.log(queue.getLength());
    processqueue();
  }

  function err(xhr) {
    processqueue();
  }
  //queue.enqueue("Harold son, you are my herald, my son.");
}


function playaudio(speaker, tweet) {
  requesting = true;
  var txt = tweet.text.replace(/(?:https?|ftp):\/\/[\n\S]+/g, '');
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

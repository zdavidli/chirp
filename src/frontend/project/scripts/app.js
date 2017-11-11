var app = (function () {


    /* Fetch tweet and update the view */
    var privateFetchTweet = function () {
        appModel.fetchTweet()
            .done(function (data) {
                tweetView.updateTweet(data);
            }).fail(function (jqXHR) {
                //appView.updateServerResponses('fetching the tweet', jqXHR.status, jqXHR.statusText, null);
            });
    };

    /* Play a new tts */
    var privateNewSpeech = function (voiceId) {
        appModel.playSpeech()
            .done(function (data) {
                voiceView.updateAudio(data);
            }).fail(function (jqXHR) {
                //appView.updateServerResponses('fetching the tweet', jqXHR.status, jqXHR.statusText, null);
            });

    }

    var privateUpdateState = function () {
        privateFetchTweet();
        privateNewSpeech();
    };


    /* Create a new voice model */
    var privateCreateVoice = function (voiceId) {
        appModel.newVoice()
            .done(function (data) {
                voiceView.createVoice(data);
            }).fail(function (jqXHR) {
                //appView.updateServerResponses('fetching the tweet', jqXHR.status, jqXHR.statusText, null);
            });
    }



    //The object
    return {
        joinVoice: privateCreateVoice;
        newSpeech: privateNewSpeech,
        newTweet: privateFetchTweet
        init: function() { },
        updateState: privateUpdateState
    };

})();

'use strict';

let ws       = new WebSocket('ws://localhost:8000/ws');
let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let audioSrc = null;
let playBtn  = document.querySelector('#playBtn')


ws.onmessage = (event) => {
    audioSrc = audioCtx.createBufferSource();
    event.data.arrayBuffer().then(arrayBuffer => {
        audioCtx.decodeAudioData(arrayBuffer, function(buffer) {
            console.log(`Song duration: ${Math.floor(buffer.duration / 60)}min ${Math.ceil(buffer.duration % 60)}sec`);
            audioSrc.buffer = buffer;
            audioSrc.connect(audioCtx.destination);
            audioSrc.loop = false;
        }, function(error) {
            console.log(error);
        });
    }).catch(error => {
        console.log(error);
    });
};

playBtn.onclick = (event) => {
    audioSrc.start(0);
    playBtn.setAttribute('disabled', 'disabled');
    audioSrc.onended = (event) => {
        audioSrc.stop();
        console.log("song ended");
    };
};

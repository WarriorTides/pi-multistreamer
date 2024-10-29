
const IP_ADRESS = window.location.href.split("/").filter((value) => (value.includes('.')))[0]

function toggleStream(streamId, url) {
  const checkbox = document.getElementById('checkbox' + streamId.slice(-1));
  const stream = document.getElementById(streamId);
  if (checkbox.checked) {
    stream.src = url;
    stream.style.display = 'block';
  } else {
    stream.src = '';
    stream.style.display = 'none';
  }
}

// function

function startup() {
  console.log(IP_ADRESS)
  fetch('http://' + IP_ADRESS + '/startup', {
    method: 'POST'
  }).then((response) => {
    console.log(response)
    getCams()
  });

}

function kill() {
  fetch('http://' + IP_ADRESS + '/killCameras', {
    method: 'POST'
  }).then(() => {
    getCams()
  });

}

function getCams() {
  fetch('http://' + IP_ADRESS + '/getProcesses', {
    method: 'GET'
  }).then((response) => response.json()).then(
    (value) => {
      ports = value.map((camera) => camera[2])
      console.log(ports)
      document.getElementById('stream-container').innerHTML = '';
      for (let i = 0; i < ports.length; i++) {
        document.getElementById('stream-container').innerHTML += `
        <div class="stream">
            <label for="checkbox1">Stream ${i}</label>
            <input type="checkbox" checked id="checkbox${i}" onclick="toggleStream('stream${i}', 'http://${IP_ADRESS}:${ports[i]}/stream')">
            <img id="stream${i}" src="http://${IP_ADRESS}:${ports[i]}/stream" alt="Stream ${i}">
        </div>
       
        
        `;
      }

    }
  );

}
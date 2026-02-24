function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loader").classList.add("hidden");
}

function showToast(message) {
    const toast = document.getElementById("toast");
    toast.innerText = message;
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 3000);
}

async function generateText() {
    showLoader();
    const topic = document.getElementById("textTopic").value;
    const depth = document.getElementById("textDepth").value;

    const response = await fetch("/generate-text", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({topic, depth})
    });

    const data = await response.json();
    document.getElementById("textResult").innerText = data.result;
    hideLoader();
    showToast("Text Generated Successfully!");
}

async function generateCode() {
    showLoader();
    const topic = document.getElementById("codeTopic").value;

    const response = await fetch("/generate-code", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({topic})
    });

    const data = await response.json();
    document.getElementById("codeResult").innerText = data.result;
    hideLoader();
    showToast("Code Generated Successfully!");
}

async function generateAudio() {
    showLoader();
    const topic = document.getElementById("audioTopic").value;

    const response = await fetch("/generate-audio", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({topic})
    });

    const data = await response.json();
    document.getElementById("audioResult").innerHTML =
        `<audio controls src="${data.audio_url}"></audio>`;
    hideLoader();
    showToast("Audio Generated Successfully!");
}
async function generateText() {
    const prompt = document.getElementById("topicInput").value;
    const level = document.getElementById("levelSelect").value;

    const response = await fetch("/generate-text", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: `Explain ${prompt} in ${level} level`
        })
    });

    const data = await response.json();

    document.getElementById("output").innerText = data.result;
}
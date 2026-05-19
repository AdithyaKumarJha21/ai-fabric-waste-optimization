const form = document.getElementById("prediction-form");
const statusBox = document.getElementById("status");

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function collectFormData() {
  const formData = new FormData(form);
  const data = {};

  for (const [key, value] of formData.entries()) {
    data[key] = value;
  }

  return data;
}

function showError(message) {
  statusBox.textContent = message;
  statusBox.classList.add("error");
}

function showResult(data) {
  const layout = data.layout;
  const prediction = data.prediction;

  statusBox.textContent = "Prediction completed successfully.";
  statusBox.classList.remove("error");

  setText("pieces", layout.pieces_possible);
  setText("waste", `${prediction.predicted_waste_percentage}%`);
  setText("utilization", `${prediction.predicted_utilization_percentage}%`);
  setText("efficiency", prediction.efficiency_level);
  setText("length-count", layout.pieces_along_length);
  setText("width-count", layout.pieces_along_width);
  setText("logic-waste", `${layout.waste_percentage}%`);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusBox.textContent = "Calculating layout and predicting waste...";
  statusBox.classList.remove("error");

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(collectFormData()),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Prediction failed.");
      return;
    }

    showResult(data);
  } catch (error) {
    showError("Backend is not running. Start Flask and try again.");
  }
});

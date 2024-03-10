function closeOverlay() {
  document.getElementById("coming-soon").style.display = "none";
}

document
  .querySelector("a[href='#coming-soon']")
  .addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("coming-soon").style.display = "flex";
  });

function adjustSize(action) {
  let frame = document.getElementById("pdfFrame");

  switch (action) {
    case "increase":
      frame.style.height = parseInt(frame.style.height) + 50 + "px";
      break;
    case "decrease":
      frame.style.height = parseInt(frame.style.height) - 50 + "px";
      break;
  }
}

function togglePdf() {
  let frame = document.getElementById("pdfFrame");
  if (frame.style.height !== "0px") {
    frame.style.height = "0px";
  } else {
    frame.style.height = "500px";
  }
}

function viewPdf(path) {
  document.getElementById("pdfFrame").src = path;
  document.getElementById("pdf-viewer").style.display = "flex";
}

function closePdf() {
  document.getElementById("pdfFrame").src = "";
  document.getElementById("pdf-viewer").style.display = "none";
}

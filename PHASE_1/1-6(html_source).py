<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Smart Guard System</title>

  <style>
    body {
      background-color: #111;
      color: white;
      font-family: Arial, sans-serif;
      text-align: center;
    }

    h1 {
      margin-top: 20px;
    }

    img {
      border: 3px solid #444;
      margin-top: 20px;
      width: 640px;
    }

    .status {
      margin-top: 20px;
      font-size: 18px;
    }
  </style>
</head>

<body>

<h1>Smart Guard System</h1>

<img src="/video_feed" />

<div class="status" id="status">
Loading...
</div>

<script>

async function updateStatus() {

  const response = await fetch("/status");
  const data = await response.json();

  document.getElementById("status").innerHTML =
  "Mode: " + data.mode +
  " | Motion: " + data.motion +
  " | Pixels: " + data.pixels +
  " | Faces: " + data.faces +
  " | Auth: " + data.auth +
  " | Servo Angle: " + data.servo_angle +
  " | Last Capture: " + data.last_capture;

}

setInterval(updateStatus, 1000);

</script>

</body>
</html>
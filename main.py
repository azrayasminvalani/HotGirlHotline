import webview
import pygame
import threading
import os
import http.server
import socketserver

base_dir = os.path.dirname(os.path.abspath(__file__))


html = """
<!DOCTYPE html>
<html>
  <head>
  
    <style>
  body {
    margin: 0;
    background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    overflow: hidden;
  }

  .controls {
    display: flex;
    flex-direction: row; 
    justify-content: center;
    align-items: center;
    gap: 15px; 
  }

  button {
    padding: 10px;
    font-size: 12px;
    background-color: white;
    border: none;
    border-radius: 50%;
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.15);
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
  }

  button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }
  .container {
  border: 2px solid #ec407a;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 12px rgba(0,0,0,0.25);
  background-color: #fff;
  position: relative;
  width: 210px;
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; 
}

#special-img {
  width: 200px;
  height: auto;
  border: 2px solid white;
  border-radius: 15px;
  box-shadow: 0 8px 16px rgba(236, 64, 122, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease; 
  cursor: pointer; 
  }

.header {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  margin-bottom: 8px;
}


.title {
  font-size: 15px;
  font-weight: bold;
  color: #ec407a;
  line-height: 1.2;
  
  font-family: 'Fredoka One', cursive;
}

.subtitle {
  font-size: 10px;
  color: #ec407a;
  margin-right: 10px;
}

.spacer {
  flex-grow: 1;
}

.close-btn {
  position: relative; 
  background: transparent;
  border: none;
  font-size: 8px;
  cursor: pointer;
  color: #888;
}
.minimize-btn{
  position: relative; 
  background: transparent;
  border: none;
  font-size: 8px;
  cursor: pointer;
  color: #888;
}

.close-btn:hover {
  color: #000;
}

  }

</style>

  
  </head>
  
  <body>
    <div class="header">
      <div class="title-subtitle">
      <span class="title">Hot Girl Hotline</span>
      <span class="subtitle">press play, feel seen</span>
    </div>
    <button onclick="minimizeApp()"class="minimize-btn">&#9472;</button>
    <button onclick="closeApp()" class="close-btn">&#10006;</button>
  </div>
  <div class="container">
  <img id="special-img" src="http://localhost:8000/sensitivegangsta.gif">

  



  
  <div class="controls">
  <button onclick="playAudio()" id="play"> ▶️ </button>
  <button onclick="previousAudio()"id="previous">⏮️</button>
  <button onclick="nextAudio()" id="next">⏭️</button>
  <button onclick="stopAudio()" id="stop">⏹️</button>
  </div>
  
<script>

  function playAudio(){
    window.pywebview.api.play_audio();
  }
  
  function stopAudio(){
    window.pywebview.api.stop_audio();
    updateImage("http://localhost:8000/sensitivegangsta.gif");

  }
  
  function nextAudio(){
    window.pywebview.api.next_audio();
    
  }
  function previousAudio(){
    window.pywebview.api.prev_audio();
    
  }
  
  function updateImage(newSrc) {
    document.querySelector("img").src = newSrc;
  }
  
  function closeApp(){
    window.pywebview.api.close_app();
  }
  
  function minimizeApp(){
    window.pywebview.api.minimize_app();
  }
    </script>
  </body>
</html>
"""


def start_image_server():
    image_dir = os.path.join(base_dir, 'images')
    os.chdir(image_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print("Serving images at http://localhost:8000")
        httpd.serve_forever()


class Api:
    def __init__(self):
        pygame.mixer.init()
        self.tracks = [
            os.path.join(base_dir, 'audio', '1.wav'),
            os.path.join(base_dir, 'audio', '2.wav'),
            os.path.join(base_dir, 'audio', '3.wav'),
            os.path.join(base_dir, 'audio', '4.wav'),
            os.path.join(base_dir, 'audio', '5.wav'),
            os.path.join(base_dir, 'audio', '6.wav'),
            os.path.join(base_dir, 'audio', '7.wav')
        ]

        self.images = [
            "http://localhost:8000/1.gif",
            "http://localhost:8000/2.gif",
            "http://localhost:8000/3.gif",
            "http://localhost:8000/4.gif",
            "http://localhost:8000/5.gif",
            "http://localhost:8000/6.gif",
            "http://localhost:8000/7.gif"
        ]
        self.current_index = 0
        pygame.mixer.music.load(self.tracks[self.current_index])

    def play_audio(self):
        pygame.mixer.music.play()
        window.evaluate_js("updateImage('{}')".format(self.images[self.current_index]))

    def stop_audio(self):
        pygame.mixer.music.stop()

    def next_audio(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        window.evaluate_js("updateImage('{}')".format(self.images[self.current_index]))

    def prev_audio(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        window.evaluate_js("updateImage('{}')".format(self.images[self.current_index]))

    def close_app(self):
      webview.windows[0].destroy()
        
    def minimize_app(self):
      window.hide()


api = Api()
window = webview.create_window("Sensitive Gangsta", html=html, js_api=api, width=300, height=450, resizable=False)

threading.Thread(target=start_image_server, daemon=True).start()

webview.start()

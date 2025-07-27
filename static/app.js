class DebateApp {
  constructor() {
    this.selectedTopic = ""
    this.selectedSide = ""
    this.selectedTheme = ""
    this.isRecording = false
    this.mediaRecorder = null
    this.audioChunks = []
    this.voiceStatus = null

    this.initializeEventListeners()
    this.checkVoiceStatus()
    this.checkBrowserCompatibility()
  }

  checkBrowserCompatibility() {
    console.log("🔍 Checking browser compatibility...")
    console.log("Navigator:", !!navigator)
    console.log("MediaDevices:", !!navigator.mediaDevices)
    console.log("getUserMedia:", !!navigator.mediaDevices?.getUserMedia)
    console.log(
      "Legacy getUserMedia:",
      !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia),
    )
    console.log("MediaRecorder:", !!window.MediaRecorder)
    console.log("Location protocol:", window.location.protocol)
    console.log("Location hostname:", window.location.hostname)
    console.log("Is secure context:", window.isSecureContext)

    const isLocalhost =
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1" ||
      window.location.hostname === "0.0.0.0"

    console.log("Is localhost:", isLocalhost)

    if (!window.isSecureContext && !isLocalhost) {
      console.warn("⚠️ Not in secure context and not localhost - microphone may not work")
    }

    // Test MediaDevices availability
    if (navigator.mediaDevices) {
      navigator.mediaDevices
        .enumerateDevices()
        .then((devices) => {
          const audioInputs = devices.filter((device) => device.kind === "audioinput")
          console.log("🎤 Audio input devices found:", audioInputs.length)
          audioInputs.forEach((device, index) => {
            console.log(`   ${index + 1}. ${device.label || "Unknown microphone"} (${device.deviceId})`)
          })
        })
        .catch((error) => {
          console.warn("⚠️ Could not enumerate devices:", error)
        })
    }
  }

  async checkVoiceStatus() {
    try {
      const response = await fetch("/voice_status")
      this.voiceStatus = await response.json()

      console.log("Voice Status:", this.voiceStatus)

      if (!this.voiceStatus.voice_recording_available) {
        this.disableVoiceFeatures("Voice transcription not available")
      }
    } catch (error) {
      console.error("Error checking voice status:", error)
      this.disableVoiceFeatures("Could not check voice status")
    }
  }

  initializeEventListeners() {
    document.querySelectorAll(".topic-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        this.selectTopic(e.target.dataset.topic)
      })
    })

    document.getElementById("use-custom-topic").addEventListener("click", () => {
      const customTopic = document.getElementById("custom-topic").value.trim()
      if (customTopic) {
        this.selectTopic(customTopic)
      }
    })

    document.getElementById("side-for").addEventListener("click", () => {
      this.selectSide("FOR")
    })

    document.getElementById("side-against").addEventListener("click", () => {
      this.selectSide("AGAINST")
    })

    document.querySelectorAll(".theme-card").forEach((card) => {
      card.addEventListener("click", (e) => {
        const theme = e.currentTarget.dataset.theme
        this.selectTheme(theme)
      })
    })

    document.getElementById("start-debate-btn").addEventListener("click", () => {
      this.startDebate()
    })

    document.getElementById("submit-argument").addEventListener("click", () => {
      this.submitArgument()
    })

    document.getElementById("argument-input").addEventListener("keypress", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()
        this.submitArgument()
      }
    })

    document.getElementById("record-btn").addEventListener("mousedown", (e) => {
      e.preventDefault()
      this.startRecording()
    })

    document.getElementById("record-btn").addEventListener("mouseup", (e) => {
      e.preventDefault()
      this.stopRecording()
    })

    document.getElementById("record-btn").addEventListener("mouseleave", (e) => {
      e.preventDefault()
      this.stopRecording()
    })

    document.getElementById("record-btn").addEventListener("touchstart", (e) => {
      e.preventDefault()
      this.startRecording()
    })

    document.getElementById("record-btn").addEventListener("touchend", (e) => {
      e.preventDefault()
      this.stopRecording()
    })

    document.getElementById("reset-debate").addEventListener("click", () => {
      this.resetDebate()
    })
  }

  selectTopic(topic) {
    this.selectedTopic = topic
    document.getElementById("topic-text").textContent = topic
    document.getElementById("selected-topic").classList.remove("hidden")
    document.getElementById("side-selection").classList.remove("hidden")

    document.querySelectorAll(".topic-btn").forEach((btn) => {
      btn.classList.remove("bg-indigo-900/50")
    })

    const selectedBtn = document.querySelector(`[data-topic="${topic}"]`)
    if (selectedBtn) {
      selectedBtn.classList.add("bg-indigo-900/50")
    }
  }

  selectSide(side) {
    this.selectedSide = side
    document.getElementById("side-text").textContent = side
    document.getElementById("selected-side").classList.remove("hidden")
    document.getElementById("theme-selection").classList.remove("hidden")

    document.querySelectorAll(".side-btn").forEach((btn) => {
      btn.classList.remove("bg-green-700/20", "bg-red-700/20")
    })

    if (side === "FOR") {
      document.getElementById("side-for").classList.add("bg-green-700/20")
    } else {
      document.getElementById("side-against").classList.add("bg-red-700/20")
    }
  }

  selectTheme(theme) {
    this.selectedTheme = theme

    const themeNames = {
      sassy: "😏 Sassy Coach",
      ruthless: "⚔️ Ruthless Veteran",
      sweet: "🥰 Sweet Friend",
      innocent: "🌸 Sweet Angel",
      bestie: "👯 Your Bestie",
      flirty: "😈 Charming Rival",
      objective: "🤖 Objective AI",
      teacher: "👩‍🏫 Strict Teacher",
      philosopher: "🧠 Deep Philosopher",
    }

    document.getElementById("theme-text").textContent = themeNames[theme]
    document.getElementById("selected-theme").classList.remove("hidden")
    document.getElementById("start-debate-btn").classList.remove("hidden")

    document.querySelectorAll(".theme-card").forEach((card) => {
      card.classList.remove("selected")
    })

    document.querySelector(`[data-theme="${theme}"]`).classList.add("selected")
  }

  async startDebate() {
    this.showLoading(true)

    try {
      const response = await fetch("/start_debate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: this.selectedTopic,
          side: this.selectedSide,
          theme: this.selectedTheme,
        }),
      })

      const data = await response.json()

      if (data.success) {
        document.getElementById("setup-phase").classList.add("hidden")
        document.getElementById("debate-phase").classList.remove("hidden")

        document.getElementById("debate-topic-display").textContent = this.selectedTopic
        document.getElementById("debate-side-display").textContent = this.selectedSide
        document.getElementById("debate-theme-display").textContent = document.getElementById("theme-text").textContent

        this.addMessage("ai", data.ai_response)

        this.enableTTS(data.ai_response, data.theme)
      }
    } catch (error) {
      console.error("Error starting debate:", error)
      alert("Failed to start debate. Please try again.")
    }

    this.showLoading(false)
  }

  async submitArgument() {
    const argumentInput = document.getElementById("argument-input")
    const argument = argumentInput.value.trim()

    if (!argument) return

    this.addMessage("user", argument)
    argumentInput.value = ""

    this.showLoading(true)

    try {
      const response = await fetch("/submit_argument", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          argument: argument,
        }),
      })

      const data = await response.json()

      if (data.success) {
        this.addMessage("ai", data.ai_response)

        this.enableTTS(data.ai_response, data.theme)
      }
    } catch (error) {
      console.error("Error submitting argument:", error)
      this.addMessage("system", "Sorry, there was an error processing your argument. Please try again.")
    }

    this.showLoading(false)
  }

  addMessage(sender, message) {
    const chatContainer = document.getElementById("chat-container")
    const messageDiv = document.createElement("div")

    if (sender === "user") {
      messageDiv.className = "flex justify-end"
      messageDiv.innerHTML = `
                <div class="chat-bubble-user text-white p-4 max-w-md">
                    <div class="flex items-start gap-3">
                        <div class="flex-1">
                            <div class="font-semibold mb-1">You</div>
                            <div>${this.formatMessage(message)}</div>
                        </div>
                        <div class="text-2xl">👤</div>
                    </div>
                </div>
            `
    } else if (sender === "ai") {
      messageDiv.className = "flex justify-start"
      messageDiv.innerHTML = `
                <div class="chat-bubble-ai text-white p-4 max-w-md">
                    <div class="flex items-start gap-3">
                        <div class="text-2xl">${this.getThemeEmoji()}</div>
                        <div class="flex-1">
                            <div class="font-semibold mb-1">AI Coach</div>
                            <div>${this.formatMessage(message)}</div>
                        </div>
                    </div>
                </div>
            `
    } else {
      messageDiv.className = "flex justify-center"
      messageDiv.innerHTML = `
                <div class="bg-purple-900/30 text-purple-200 p-3 rounded-lg text-sm">
                    ${message}
                </div>
            `
    }

    chatContainer.appendChild(messageDiv)
    chatContainer.scrollTop = chatContainer.scrollHeight
  }

  formatMessage(message) {
    return message
      .replace(/\n/g, "<br>")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
  }

  getThemeEmoji() {
    const emojis = {
      sassy: "😏",
      ruthless: "⚔️",
      sweet: "🥰",
      innocent: "🌸",
      bestie: "👯",
      flirty: "😈",
      objective: "🤖",
      teacher: "👩‍🏫",
      philosopher: "🧠",
    }
    return emojis[this.selectedTheme] || "🤖"
  }

  async startRecording() {
    if (this.isRecording) {
      console.log("Already recording, ignoring start request")
      return
    }

    console.log("🎤 Starting recording process...")

    // Check if we're running locally
    const isLocalhost =
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1" ||
      window.location.hostname === "0.0.0.0" ||
      window.location.hostname.startsWith("192.168.") ||
      window.location.hostname.startsWith("10.") ||
      window.location.hostname.endsWith(".local")

    console.log("🏠 Is localhost:", isLocalhost)
    console.log("🌐 Hostname:", window.location.hostname)
    console.log("🔒 Protocol:", window.location.protocol)

    // Basic browser checking
    if (!navigator) {
      this.showRecordingError("Navigator not available")
      return
    }

    if (isLocalhost && !navigator.mediaDevices) {
      console.log("⏳ Waiting for MediaDevices API to load...")
      await new Promise((resolve) => setTimeout(resolve, 1000))
    }

    if (!navigator.mediaDevices) {
      // Try the old getUserMedia API as fallback
      const getUserMedia =
        navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia

      if (getUserMedia) {
        console.log("📱 Using legacy getUserMedia API")
        this.startRecordingLegacy(getUserMedia.bind(navigator))
        return
      }

      this.showRecordingError("MediaDevices API not supported in this browser. Please update Chrome or try Firefox.")
      return
    }

    if (!navigator.mediaDevices.getUserMedia) {
      this.showRecordingError("getUserMedia not available. Please update your browser.")
      return
    }

    // Skip HTTPS check for localhost
    if (!isLocalhost && !window.isSecureContext) {
      this.showRecordingError("Microphone requires HTTPS. Please use https:// or run on localhost.")
      return
    }

    // Check MediaRecorder support
    if (!window.MediaRecorder) {
      this.showRecordingError("MediaRecorder not supported in this browser.")
      return
    }

    console.log("✅ All browser checks passed, requesting microphone access...")

    try {
      // Request microphone access with detailed constraints
      const constraints = {
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 44100,
          channelCount: 1,
        },
      }

      console.log("🔍 Requesting microphone with constraints:", constraints)

      const stream = await navigator.mediaDevices.getUserMedia(constraints)

      console.log("✅ Microphone access granted, stream:", stream)
      console.log("🎵 Audio tracks:", stream.getAudioTracks())

      // Check if we got audio tracks
      const audioTracks = stream.getAudioTracks()
      if (audioTracks.length === 0) {
        this.showRecordingError("No audio tracks available. Please check your microphone.")
        return
      }

      console.log("🎤 Audio track settings:", audioTracks[0].getSettings())

      // Determine the best MIME type
      let mimeType = "audio/webm;codecs=opus"
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = "audio/webm"
        if (!MediaRecorder.isTypeSupported(mimeType)) {
          mimeType = "audio/mp4"
          if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = "" // Let browser choose
          }
        }
      }

      console.log("🎵 Using MIME type:", mimeType)

      // Create MediaRecorder
      const options = mimeType ? { mimeType } : {}
      this.mediaRecorder = new MediaRecorder(stream, options)

      console.log("📹 MediaRecorder created:", this.mediaRecorder)
      console.log("📹 MediaRecorder state:", this.mediaRecorder.state)

      this.audioChunks = []

      // Set up event handlers
      this.mediaRecorder.ondataavailable = (event) => {
        console.log("📊 Data available:", event.data.size, "bytes")
        if (event.data && event.data.size > 0) {
          this.audioChunks.push(event.data)
        }
      }

      this.mediaRecorder.onstop = () => {
        console.log("⏹️ Recording stopped, processing...")
        this.processRecording()
      }

      this.mediaRecorder.onerror = (event) => {
        console.error("❌ MediaRecorder error:", event.error)
        this.showRecordingError(`Recording error: ${event.error?.message || "Unknown error"}`)
        this.stopRecording()
      }

      this.mediaRecorder.onstart = () => {
        console.log("▶️ Recording started successfully")
      }

      // Start recording
      this.mediaRecorder.start(1000) // Collect data every second
      this.isRecording = true

      // Update UI
      document.getElementById("recording-status").classList.remove("hidden")
      document.getElementById("record-btn").innerHTML = '<i class="fas fa-stop"></i><span>Release to Stop</span>'
      document.getElementById("record-btn").classList.add("recording-active")

      console.log("🎤 Recording started successfully!")
    } catch (error) {
      console.error("❌ Error starting recording:", error)

      let errorMessage = "Could not start recording: "

      if (error.name === "NotAllowedError") {
        errorMessage +=
          "Microphone access denied. Please click the microphone icon in your browser's address bar and allow access."
      } else if (error.name === "NotFoundError") {
        errorMessage += "No microphone found. Please connect a microphone and refresh the page."
      } else if (error.name === "NotReadableError") {
        errorMessage += "Microphone is being used by another application. Please close other apps using the microphone."
      } else if (error.name === "OverconstrainedError") {
        errorMessage += "Microphone doesn't support the required settings. Please try a different microphone."
      } else if (error.name === "SecurityError") {
        errorMessage += "Security error. Please ensure you're using HTTPS or localhost."
      } else {
        errorMessage += error.message || "Unknown error occurred."
      }

      this.showRecordingError(errorMessage)
    }
  }

  // Legacy getUserMedia fallback
  startRecordingLegacy(getUserMedia) {
    console.log("📱 Using legacy getUserMedia API")

    getUserMedia(
      { audio: true },
      (stream) => {
        console.log("✅ Legacy getUserMedia success")

        if (!window.MediaRecorder) {
          this.showRecordingError("MediaRecorder not supported. Please update your browser.")
          return
        }

        try {
          this.mediaRecorder = new MediaRecorder(stream)
          this.audioChunks = []

          this.mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
              this.audioChunks.push(event.data)
            }
          }

          this.mediaRecorder.onstop = () => {
            this.processRecording()
          }

          this.mediaRecorder.start(1000)
          this.isRecording = true

          document.getElementById("recording-status").classList.remove("hidden")
          document.getElementById("record-btn").innerHTML = '<i class="fas fa-stop"></i><span>Release to Stop</span>'
          document.getElementById("record-btn").classList.add("recording-active")

          console.log("🎤 Legacy recording started!")
        } catch (error) {
          console.error("❌ Legacy MediaRecorder error:", error)
          this.showRecordingError("Failed to start recording: " + error.message)
        }
      },
      (error) => {
        console.error("❌ Legacy getUserMedia error:", error)
        this.showRecordingError("Microphone access failed: " + error.message)
      },
    )
  }

  showRecordingError(message) {
    console.error("🚨 Recording Error:", message)

    // Show detailed error to user
    const errorDiv = document.createElement("div")
    errorDiv.className = "fixed top-4 right-4 bg-red-600 text-white p-4 rounded-lg shadow-lg z-50 max-w-md"
    errorDiv.innerHTML = `
      <div class="flex items-start gap-3">
        <i class="fas fa-exclamation-triangle text-xl"></i>
        <div>
          <div class="font-bold">Recording Error</div>
          <div class="text-sm mt-1">${message}</div>
          <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                  class="mt-2 px-3 py-1 bg-red-700 rounded text-xs hover:bg-red-800">
            Close
          </button>
        </div>
      </div>
    `

    document.body.appendChild(errorDiv)

    // Auto-remove after 10 seconds
    setTimeout(() => {
      if (errorDiv.parentElement) {
        errorDiv.remove()
      }
    }, 10000)

    // Also show in chat
    this.addMessage("system", `🚨 ${message}`)
  }

  stopRecording() {
    if (!this.isRecording || !this.mediaRecorder) {
      console.log("Not recording, ignoring stop request")
      return
    }

    console.log("⏹️ Stopping recording...")

    try {
      if (this.mediaRecorder.state === "recording") {
        this.mediaRecorder.stop()
      }

      // Stop all tracks
      if (this.mediaRecorder.stream) {
        this.mediaRecorder.stream.getTracks().forEach((track) => {
          track.stop()
          console.log("🛑 Stopped track:", track.kind)
        })
      }
    } catch (error) {
      console.error("Error stopping recording:", error)
    }

    this.isRecording = false

    // Update UI
    document.getElementById("recording-status").classList.add("hidden")
    document.getElementById("record-btn").innerHTML = '<i class="fas fa-microphone"></i><span>Hold to Record</span>'
    document.getElementById("record-btn").classList.remove("recording-active")

    console.log("✅ Recording stopped")
  }

  async processRecording() {
    console.log("🔄 Processing recording...")
    console.log("📊 Audio chunks:", this.audioChunks.length)

    if (this.audioChunks.length === 0) {
      console.warn("⚠️ No audio chunks to process")
      this.addMessage("system", "No audio recorded. Please try holding the button longer.")
      return
    }

    // Calculate total size
    const totalSize = this.audioChunks.reduce((size, chunk) => size + chunk.size, 0)
    console.log("📊 Total audio size:", totalSize, "bytes")

    if (totalSize === 0) {
      console.warn("⚠️ Audio chunks are empty")
      this.addMessage("system", "No audio data recorded. Please check your microphone.")
      return
    }

    this.showLoading(true)

    try {
      // Create blob from chunks
      const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" })
      console.log("📦 Created audio blob:", audioBlob.size, "bytes, type:", audioBlob.type)

      // Create form data
      const formData = new FormData()
      formData.append("audio", audioBlob, "recording.wav")

      console.log("📤 Sending audio for transcription...")

      const response = await fetch("/transcribe_audio", {
        method: "POST",
        body: formData,
      })

      console.log("📥 Transcription response status:", response.status)

      const data = await response.json()
      console.log("📝 Transcription result:", data)

      if (data.success && data.transcription) {
        document.getElementById("argument-input").value = data.transcription
        this.addMessage("system", `🎤 Transcribed: "${data.transcription}"`)
        console.log("✅ Transcription successful:", data.transcription)
      } else {
        console.error("❌ Transcription failed:", data)
        this.addMessage("system", "❌ Transcription failed. Please try again or type your argument.")
      }
    } catch (error) {
      console.error("❌ Error processing recording:", error)
      this.addMessage("system", "❌ Recording processing failed. Please try again.")
    }

    this.showLoading(false)
  }

  async enableTTS(text, theme) {
    if (!this.voiceStatus?.tts_available) {
      return
    }

    try {
      const response = await fetch("/text_to_speech", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
          theme: theme,
        }),
      })

      const data = await response.json()

      if (data.success && data.audio_path) {
        const playBtn = document.getElementById("play-ai-response")
        playBtn.classList.remove("hidden")

        playBtn.onclick = () => {
          const audio = new Audio(data.audio_path)
          audio.play()
        }
      }
    } catch (error) {
      console.error("TTS error:", error)
    }
  }

  async resetDebate() {
    if (confirm("Are you sure you want to start a new debate?")) {
      try {
        await fetch("/reset_debate", { method: "POST" })
        location.reload()
      } catch (error) {
        console.error("Error resetting debate:", error)
        location.reload()
      }
    }
  }

  showLoading(show) {
    const overlay = document.getElementById("loading-overlay")
    if (show) {
      overlay.classList.remove("hidden")
    } else {
      overlay.classList.add("hidden")
    }
  }

  disableVoiceFeatures(reason) {
    const recordBtn = document.getElementById("record-btn")
    const voiceControls = recordBtn.parentElement

    recordBtn.disabled = true
    recordBtn.innerHTML = '<i class="fas fa-microphone-slash"></i><span>Voice Unavailable</span>'
    recordBtn.classList.add("opacity-50", "cursor-not-allowed")

    const infoDiv = document.createElement("div")
    infoDiv.className = "text-sm text-purple-300 text-center"
    infoDiv.textContent = `${reason}. Run ULTIMATE_FIX.bat to fix.`
    voiceControls.appendChild(infoDiv)
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new DebateApp()
})

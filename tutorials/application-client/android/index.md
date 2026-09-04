# Android Tutorial

Running OpenVidu?

OpenVidu is a self-hosted, LiveKit-compatible platform. If that is what you are running, read the [OpenVidu version of this tutorial](https://openvidu.io/latest/docs/tutorials/application-client/android/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=tutorial-cross-link) .

[Source code](https://github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/application-client/openvidu-android)

This tutorial is a simple video-call application built for **Android**, using **Kotlin**, that allows:

- Joining a video call room by requesting a token from any [application server](https://livekit-tutorials.openvidu.io/tutorials/application-server/index.md).
- Publishing your camera and microphone.
- Subscribing to all other participants' video and audio tracks automatically.
- Leaving the video call room at any time.

It uses the [LiveKit Android Kotlin SDK](https://docs.livekit.io/reference/client-sdk-android/) to connect to the LiveKit server and interact with the video call room.

## Running this tutorial

### 1. Run LiveKit Server

You can run [LiveKit locally](https://docs.livekit.io/transport/self-hosting/local/) or you can use their free tier of [LiveKit Cloud](https://cloud.livekit.io/) .

Alternatively, you can use OpenVidu, which is a fully compatible LiveKit distribution designed specifically for on-premises environments. It brings notable improvements in terms of performance, observability and development experience. For more information, visit [What is OpenVidu?](https://livekit-tutorials.openvidu.io/about-openvidu/index.md).

**Run OpenVidu locally**

1. Download OpenVidu

   ```bash
   git clone https://github.com/OpenVidu/openvidu-local-deployment
   ```

1. Configure the local deployment

   **Windows**

   ```powershell
   cd openvidu-local-deployment/community
   .\configure_lan_private_ip_windows.bat
   ```

   **macOS**

   ```bash
   cd openvidu-local-deployment/community
   ./configure_lan_private_ip_macos.sh
   ```

   **Linux**

   ```bash
   cd openvidu-local-deployment/community
   ./configure_lan_private_ip_linux.sh
   ```

1. Run OpenVidu

   ```bash
   docker compose up
   ```

**Deploy OpenVidu**

To use a production-ready OpenVidu deployment, visit the official [OpenVidu deployment guide](https://openvidu.io/latest/docs/self-hosting/deployment-types/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=deploy-step) .

Configure Webhooks

All [application servers](https://livekit-tutorials.openvidu.io/tutorials/application-server/index.md) have an endpoint to receive webhooks from LiveKit. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server](https://openvidu.io/latest/docs/self-hosting/how-to-guides/enable-webhooks/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=deploy-step#send-webhooks-to-a-local-application-server) section for more information.

**Run LiveKit locally**

Follow the official instructions to run [LiveKit locally](https://docs.livekit.io/transport/self-hosting/local/) .

Configure Webhooks

All [application servers](https://livekit-tutorials.openvidu.io/tutorials/application-server/index.md) have an endpoint to receive webhooks from LiveKit. For this reason, when using LiveKit locally you need to configure webhooks to point to your application server in order to make it work. Check the [Webhooks](https://openvidu.io/latest/docs/reference/webhooks/) section from the official documentation and follow the instructions to configure webhooks.

**Use LiveKit Cloud**

Use your account in [LiveKit Cloud](https://cloud.livekit.io/) .

Configure Webhooks

All [application servers](https://livekit-tutorials.openvidu.io/tutorials/application-server/index.md) have an endpoint to receive webhooks from LiveKit. For this reason, when using LiveKit Cloud you need to configure webhooks to point to your local application server in order to make it work. Check the [Webhooks](https://openvidu.io/latest/docs/reference/webhooks/) section from the official documentation and follow the instructions to configure webhooks.

Expose your local application server

In order to receive webhooks from LiveKit Cloud on your local machine, you need to expose your local application server to the internet. Tools like [Ngrok](https://ngrok.com/) , [LocalTunnel](https://localtunnel.github.io/www/) , [LocalXpose](https://localxpose.io/) and [Zrok](https://zrok.io/) can help you achieve this.

These tools provide you with a public URL that forwards requests to your local application server. You can use this URL to receive webhooks from LiveKit Cloud, configuring it as indicated above.

### 2. Download the tutorial code

```bash
git clone https://github.com/OpenVidu/openvidu-livekit-tutorials.git
```

### 3. Run a server application

**Node.js**

To run this server application, you need [Node.js](https://nodejs.org/en/download) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/node
   ```

1. Install dependencies

   ```bash
   npm install
   ```

1. Run the application

   ```bash
   npm start
   ```

For more information, check the [Node.js tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/node/index.md).

**Go**

To run this server application, you need [Go](https://go.dev/doc/install) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/go
   ```

1. Run the application

   ```bash
   go run main.go
   ```

For more information, check the [Go tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/go/index.md).

**Ruby**

To run this server application, you need [Ruby](https://www.ruby-lang.org/en/documentation/installation/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/ruby
   ```

1. Install dependencies

   ```bash
   bundle install
   ```

1. Run the application

   ```bash
   ruby app.rb
   ```

For more information, check the [Ruby tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/ruby/index.md).

**Java**

To run this server application, you need [Java](https://www.java.com/en/download/manual.jsp) and [Maven](https://maven.apache.org) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/java
   ```

1. Run the application

   ```bash
   mvn spring-boot:run
   ```

For more information, check the [Java tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/java/index.md).

**Python**

To run this server application, you need [Python 3](https://www.python.org/downloads/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/python
   ```

1. Create a python virtual environment

   ```bash
   python -m venv venv
   ```

1. Activate the virtual environment

   **Windows**

   ```powershell
   .\venv\Scripts\activate
   ```

   **macOS**

   ```bash
   . ./venv/bin/activate
   ```

   **Linux**

   ```bash
   . ./venv/bin/activate
   ```

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

1. Run the application

   ```bash
   python app.py
   ```

For more information, check the [Python tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/python/index.md).

**Rust**

To run this server application, you need [Rust](https://rust-lang.org/tools/install/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/rust
   ```

1. Run the application

   ```bash
   cargo run
   ```

For more information, check the [Rust tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/rust/index.md).

**PHP**

To run this server application, you need [PHP](https://www.php.net/manual/en/install.php) and [Composer](https://getcomposer.org/download/) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/php
   ```

1. Install dependencies

   ```bash
   composer install
   ```

1. Run the application

   ```bash
   composer start
   ```

Warning

LiveKit PHP SDK requires library [BCMath](https://www.php.net/manual/en/book.bc.php) . This is available out-of-the-box in PHP for Windows, but a manual installation might be necessary in other OS. Run **`sudo apt install php-bcmath`** or **`sudo yum install php-bcmath`**

For more information, check the [PHP tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/php/index.md).

**.NET**

To run this server application, you need [.NET](https://dotnet.microsoft.com/en-us/download) installed on your device.

1. Navigate into the server directory

   ```bash
   cd openvidu-livekit-tutorials/application-server/dotnet
   ```

1. Run the application

   ```bash
   dotnet run
   ```

Warning

This .NET server application needs the `LIVEKIT_API_SECRET` env variable to be at least 32 characters long. Make sure to update it [here](https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-server/dotnet/appsettings.json#L11) and in your [LiveKit Server](#1-run-livekit-server).

For more information, check the [.NET tutorial](https://livekit-tutorials.openvidu.io/tutorials/application-server/dotnet/index.md).

### 4. Run the client application

To run the client application tutorial, you need [Android Studio](https://developer.android.com/studio) installed on your development computer.

1. Open Android Studio and import the project located at `openvidu-livekit-tutorials/application-client/openvidu-android`.
1. Run the application in an emulator or a physical device by clicking the "Run" button in Android Studio. Check out the [official documentation](https://developer.android.com/studio/run) for further information.

The application will initiate as a native Android program. Once the application is opened, you should see a screen like this:

URL configuration of the Android tutorial app

This screen allows you to configure the URLs of the application server and the LiveKit server. You need to set them up for requesting tokens to your application server and connecting to the LiveKit server.

Connecting real Android device to application server running in you local network

One advantage of [running OpenVidu locally](#run-openvidu-locally) is that you can test your application client in a real Android device and be able to reach the application server very easily without worrying about SSL certificates if they are both running in the same local network. For more information, see section [Accessing your app from other devices in your network](https://livekit-tutorials.openvidu.io/openvidu-vs-livekit/#accessing-your-app-from-other-devices-in-your-network).

Once you have configured the URLs, you can join a video call room by providing a room name and a user name. After joining the room, you will be able to see your own video and audio tracks, as well as the video and audio tracks of the other participants in the room.

Join screen of the Android tutorial app

Video call room of the Android tutorial app

## Understanding the code

This Android project has been generated with Android Studio. You may come across various configuration files and other items that are not essential for this tutorial. Our focus will be on the key files located within the `app/src/main/java` directory:

- `MainActivity.kt`: This file defines the main activity of the application, which allows the user to join a video call room by providing a room name and a user name.
- `RoomLayoutActivity.kt`: Activity responsible for managing the video call room, including publishing and subscribing to video and audio tracks.
- `PaticipantAdapter.kt` and `ParticipantViewHolder.kt`: These files define the **Adapter** and **ViewHolder** for the **RecyclerView** that displays the participants video tracks in the video call room.
- `Urls.kt`: Object that contains the URLs of the application server and the LiveKit server.
- `ConfigureUrlsActivity.kt`: Activity that allows the user to configure the URLs of the application server and the LiveKit server.

The activity layout files are located in the `app/src/main/res/layout` directory.

To use LiveKit in an Android application, you need to add the [LiveKit Android Kotlin SDK](https://docs.livekit.io/reference/client-sdk-android/) as a dependency in the `build.gradle.kts` file. This dependecy provides the necessary classes and methods to interact with the LiveKit server:

<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-android/app/build.gradle.kts#L43' target='_blank'>build.gradle.kts</a>

```text
dependencies {
    implementation 'io.livekit:livekit-android:2.5.0'
}
```

You will also need JitPack as a repository in the `settings.gradle.kts` file:

<a href='https://github.com/OpenVidu/openvidu-livekit-tutorials/blob/master/application-client/openvidu-android/settings.gradle.kts#L19' target='_blank'>settings.gradle.kts</a>

```text
dependencyResolutionManagement {
    //...
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
}
```

______________________________________________________________________

### Android specific requirements

In order to be able to test the application on an Android device, the application must ask for the necessary permissions to access the device's camera and microphone.

First, you need to add the following permissions to the `AndroidManifest.xml` file located in the `app/src/main` directory:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
```

Then, the app need to request these permissions when the user joins the video call room. This is done in the `RoomLayoutActivity.kt` file by calling the `requestNeededPermissions` method in the `onCreate` method:

```kotlin
private fun requestNeededPermissions(onHasPermissions: () -> Unit) {
    val requestPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { grants ->
            var hasDenied = false

            // Check if any permissions weren't granted
            for (grant in grants.entries) {
                if (!grant.value) {
                    Toast.makeText(this, "Missing permission: ${grant.key}", Toast.LENGTH_SHORT)
                        .show()

                    hasDenied = true
                }
            }

            if (!hasDenied) {
                onHasPermissions()
            }
        }

    // Assemble the needed permissions to request
    val neededPermissions =
        listOf(Manifest.permission.RECORD_AUDIO, Manifest.permission.CAMERA).filter {
            ContextCompat.checkSelfPermission(
                this, it
            ) == PackageManager.PERMISSION_DENIED
        }.toTypedArray()

    if (neededPermissions.isNotEmpty()) {
        requestPermissionLauncher.launch(neededPermissions)
    } else {
        onHasPermissions()
    }
}
```

______________________________________________________________________

### Configuring URLs

The `Urls.kt` file defines an object that contains the following URLs required for the application:

- `applicationServerUrl`: The URL of the application server. This variable is used to make requests to the server to obtain a token for joining the video call room.
- `livekitUrl`: The URL of the LiveKit server. This variable is used to connect to the LiveKit server and interact with the video call room.

You should configure these URLs according to your deployment settings. In case you are [running OpenVidu locally](#run-openvidu-locally), you can set the `applicationServerUrl` to `https://xxx-yyy-zzz-www.openvidu-local.dev:6443` and the `livekitUrl` to `wss://xxx-yyy-zzz-www.openvidu-local.dev:7443`, where `xxx-yyy-zzz-www` part of the domain is the LAN private IP address of the machine running OpenVidu, with dashes (-) instead of dots (.).

If these URLs are left empty, the user will be prompted to enter the URLs when the application starts. This configuration is managed in the `ConfigureUrlsActivity.kt` file:

URL configuration of the Android tutorial app

When the user clicks the `Save` button, the `onSaveUrls()` method is called, which saves the URLs in the `Urls` object and finishes the activity, returning to the MainActivity:

```kotlin
private fun onSaveUrls() {
    val serverUrl = binding.serverUrl.text.toString()
    val livekitUrl = binding.livekitUrl.text.toString()

    if (serverUrl.isNotEmpty() && livekitUrl.isNotEmpty()) {
        Urls.livekitUrl = binding.livekitUrl.text.toString()
        Urls.applicationServerUrl = binding.serverUrl.text.toString()
        finish()
    } else {
        Toast.makeText(this, "Please fill in all fields", Toast.LENGTH_SHORT).show()
    }
}
```

______________________________________________________________________

### Joining a room

Before joining a room, the user must provide a room name and a user name. After the user specifies them, when they click the `Join` button, the `navigateToRoomLayoutActivity()` method of the `MainActivity.kt` file is called, which simply set the values of the participant name and room name in the intent and starts the `RoomLayoutActivity`:

```kotlin
private fun navigateToRoomLayoutActivity() {
    binding.joinButton.isEnabled = false

    val participantName = binding.participantName.text.toString()
    val roomName = binding.roomName.text.toString()

    if (participantName.isNotEmpty() && roomName.isNotEmpty()) {
        val intent = Intent(this, RoomLayoutActivity::class.java)
        intent.putExtra("participantName", participantName)
        intent.putExtra("roomName", roomName)
        startActivity(intent)
    } else {
        Toast.makeText(this, "Please fill in all fields", Toast.LENGTH_SHORT).show()
    }

    binding.joinButton.isEnabled = true
}
```

Now let's see the code of the `RoomLayoutActivity.kt` file:

```kotlin
data class TrackInfo( // (1)!
    val track: VideoTrack,
    val participantIdentity: String,
    val isLocal: Boolean = false
)

class RoomLayoutActivity : AppCompatActivity() {
    private lateinit var binding: ActivityRoomLayoutBinding // (2)!
    private lateinit var participantAdapter: ParticipantAdapter // (3)!

    private lateinit var room: Room // (4)!
    private val participantTracks: MutableList<TrackInfo> = mutableListOf() // (5)!

    private val client = HttpClient(CIO) { // (6)!
        expectSuccess = true
        install(ContentNegotiation) {
            json()
        }
    }
```

1. `TrackInfo` data class, which groups a video track with the participant's identity.
1. The binding object for the activity layout.
1. The adapter for the RecyclerView that displays the participants' video tracks.
1. The room object, which represents the video call room.
1. A list of `TrackInfo` objects, which represent the video tracks of the participants in the room.
1. The HTTP client used to make requests to the application server.

The `RoomLayoutActivity.kt` file defines the following variables:

- `room`: The room object, which represents the video call room.
- `participantTracks`: A list of `TrackInfo` objects, which represent the video tracks of the participants in the room.

When the activity is created, the `onCreate` method is called. This method initializes the activity layout, create a `Room` object, initializes the `RecyclerView` and request needed permissions:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    binding = ActivityRoomLayoutBinding.inflate(layoutInflater)
    setContentView(binding.root)

    binding.loader.visibility = View.VISIBLE
    binding.leaveButton.setOnClickListener {
        leaveRoom()
    }

    // Create Room object
    room = LiveKit.create(applicationContext)

    initRecyclerView()

    // Check for audio and camera permissions before connecting to the room
    requestNeededPermissions { connectToRoom() }
}
```

After the application check if the user has granted permissions, the `connectToRoom()` method is called:

```kotlin
private fun connectToRoom() {
    // Get the room name and participant name from the intent
    val participantName = intent.getStringExtra("participantName") ?: "Participant1" // (1)!
    val roomName = intent.getStringExtra("roomName") ?: "Test Room"

    binding.roomName.text = roomName // (2)!

    lifecycleScope.launch {
        // Specify the actions when events take place in the room
        launch {
            room.events.collect { event ->
                when (event) {
                    // On every new Track received...
                    is RoomEvent.TrackSubscribed -> onTrackSubscribed(event) // (3)!
                    // On every new Track destroyed...
                    is RoomEvent.TrackUnsubscribed -> onTrackUnsubscribed(event) // (4)!
                    else -> {}
                }
            }
        }

        try {
            // Get token from your application server with the room name and participant name
            val token = getToken(roomName, participantName) // (5)!

            // Connect to the room with the LiveKit URL and the token
            room.connect(Urls.livekitUrl, token) // (6)!

            // Publish your camera and microphone
            val localParticipant = room.localParticipant
            localParticipant.setMicrophoneEnabled(true) // (7)!
            localParticipant.setCameraEnabled(true)

            // Add local video track to the participantTracks list
            launch {
                localParticipant::videoTrackPublications.flow
                    .collect { publications ->
                        val videoTrack = publications.firstOrNull()?.second as? VideoTrack

                        if (videoTrack != null) {
                            participantTracks.add( // (8)!
                                0,
                                TrackInfo(videoTrack, participantName, true)
                            )
                            participantAdapter.notifyItemInserted(0)
                        }
                    }
            }

            binding.loader.visibility = View.GONE
        } catch (e: Exception) {
            println("There was an error connecting to the room: ${e.message}")
            Toast.makeText(this@RoomLayoutActivity, "Failed to join room", Toast.LENGTH_SHORT)
                .show()
            leaveRoom()
        }
    }
}
```

1. Get the room name and participant name from the intent.
1. Set the room title in the layout.
1. Event handling for when a new track is received in the room.
1. Event handling for when a track is destroyed.
1. Get a token from the application server with the room name and participant name.
1. Connect to the room with the LiveKit URL and the token.
1. Publish your camera and microphone.
1. Add local video track to the `participantTracks` list

The `connectToRoom()` method performs the following actions:

1. It retrieves the room name and participant name from the intent.

1. Set the room title in the layout.

1. Event handling is configured for different scenarios within the room. These events are fired when new tracks are subscribed to and when existing tracks are unsubscribed.

   - **`RoomEvent.TrackSubscribed`**: This event is triggered when a new track is received in the room. It manages the storage of the new track in the `participantTracks` list if it is a video track and notify the Adapter that a new item has been inserted.

   ```kotlin
   private fun onTrackSubscribed(event: RoomEvent.TrackSubscribed) {
       val track = event.track

       // If the track is a video track, add it to the participantTracks list
       if (track is VideoTrack) {
           participantTracks.add(TrackInfo(track, event.participant.identity!!.value))
           participantAdapter.notifyItemInserted(participantTracks.size - 1)
       }
   }
   ```

   - **`RoomEvent.TrackUnsubscribed`**: This event occurs when a track is destroyed, and it takes care of removing the video track from the `participantTracks` list and notify the Adapter that an item has been removed.

   ```kotlin
   private fun onTrackUnsubscribed(event: RoomEvent.TrackUnsubscribed) {
       val track = event.track

       // If the track is a video track, remove it from the participantTracks list
       if (track is VideoTrack) {
           val index = participantTracks.indexOfFirst { it.track.sid == track.sid }

           if (index != -1) {
               participantTracks.removeAt(index)
               participantAdapter.notifyItemRemoved(index)
           }
       }
   }
   ```

   These event handlers are essential for managing the behavior of tracks within the video call.

   Take a look at all events

   You can take a look at all the events in the [Room events reference](https://openvidu.io/latest/docs/reference/client-sdk/#room-events)

1. It requests a token from the application server using the room name and participant name. This is done by calling the `getToken()` method:

   ```kotlin
   /**
    * --------------------------------------------
    * GETTING A TOKEN FROM YOUR APPLICATION SERVER
    * --------------------------------------------
    * The method below request the creation of a token to
    * your application server. This prevents the need to expose
    * your LiveKit API key and secret to the client side.
    *
    * In this sample code, there is no user control at all. Anybody could
    * access your application server endpoints. In a real production
    * environment, your application server must identify the user to allow
    * access to the endpoints.
    */
   private suspend fun getToken(roomName: String, participantName: String): String {
       val response = client.post(Urls.applicationServerUrl + "token") {
           contentType(ContentType.Application.Json)
           setBody(TokenRequest(participantName, roomName))
       }
       return response.body<TokenResponse>().token
   }
   ```

   This method sends a POST request using [Ktor Client](https://ktor.io/docs/client-create-and-configure.html) to the application server's `/token` endpoint. The request body contains the room name and participant name. The server responds with a token that is used to connect to the room.

1. It connects to the room using the LiveKit URL and the token.

1. It publishes the camera and microphone tracks to the room using `setMicrophoneEnabled()` and `setCameraEnabled()` methods from `room.localParticipant`.

1. It adds the local video track to the `participantTracks` list.

______________________________________________________________________

### Displaying Video Tracks

In order to display the video tracks of the participants in the room, the `RoomLayoutActivity` uses a `RecyclerView` with a custom `Adapter` and `ViewHolder`. This allows the application to load and display the video tracks dynamically as they are received.

Whenever a new video track is added to the `participantTracks` list, the `ParticipantAdapter` is notified that a new item has been inserted. The `ParticipantAdapter` then updates the `RecyclerView` to display the new video track by calling the `render` method of the `ParticipantViewHolder`:

```kotlin
fun render(trackInfo: TrackInfo, room: Room) {
    val participantIdentity = if (trackInfo.isLocal) {
        trackInfo.participantIdentity + " (You)"
    } else {
        trackInfo.participantIdentity
    }

    binding.identity.text = participantIdentity // (1)!

    // Only initialize the renderer once
    if (!used) {
        room.initVideoRenderer(binding.renderer) // (2)!
        used = true
    }

    trackInfo.track.addRenderer(binding.renderer) // (3)!
}
```

1. Set the participant identity in the layout.
1. Initialize the video renderer for the participant.
1. Add the video track to the renderer.

The `render` method performs the following actions:

- It sets the participant identity in the layout.
- It initializes the video renderer for the participant. This is done only once for each participant.
- It adds the video track to the renderer.

______________________________________________________________________

### Leaving the room

When the user wants to leave the room, they can click the `Leave Room` button. This action calls the `leaveRoom()` method:

```kotlin
private fun leaveRoom() {
    // Leave the room by calling 'disconnect' method over the Room object
    room.disconnect() // (1)!

    client.close() // (2)!

    // Go back to the previous activity.
    finish() // (3)!
}

override fun onDestroy() { // (4)!
    super.onDestroy()
    leaveRoom()
}
```

1. Disconnect the user from the room.
1. Close the HTTP client.
1. Finish the activity and go back to the previous activity.
1. Call the `leaveRoom()` method when the activity is destroyed.

The `leaveRoom()` method performs the following actions:

- It disconnects the user from the room by calling the `disconnect()` method on the `room` object.
- It closes the HTTP client.
- It finishes the activity and goes back to the previous activity.

The `onDestroy()` lifecycle method is used to ensure that the user leaves the room when the activity is destroyed.

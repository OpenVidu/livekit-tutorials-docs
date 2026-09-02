# Application Server Tutorials

Running OpenVidu?

OpenVidu is a self-hosted, LiveKit-compatible platform. If that is what you are running, read the [OpenVidu version of this tutorial](https://openvidu.io/latest/docs/tutorials/application-server/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=tutorial-cross-link) .

Every application server below has two specific purposes:

- Generate LiveKit tokens on demand for any [application client](https://livekit-tutorials.openvidu.io/tutorials/application-client/index.md).
- Receive LiveKit [webhook events](https://openvidu.io/latest/docs/reference/webhooks/) .

To do so they all define two REST endpoints:

- `/token`: takes a room and participant name and returns a token.
- `/webhook`: for receiving webhook events from LiveKit Server.

They use the proper [LiveKit Server SDK](https://docs.livekit.io/reference/) for their language, if available.

[**Node.js**](https://livekit-tutorials.openvidu.io/tutorials/application-server/node/index.md)

[**Go**](https://livekit-tutorials.openvidu.io/tutorials/application-server/go/index.md)

[**Ruby**](https://livekit-tutorials.openvidu.io/tutorials/application-server/ruby/index.md)

[**Java**](https://livekit-tutorials.openvidu.io/tutorials/application-server/java/index.md)

[**Python**](https://livekit-tutorials.openvidu.io/tutorials/application-server/python/index.md)

[**Rust**](https://livekit-tutorials.openvidu.io/tutorials/application-server/rust/index.md)

[**PHP**](https://livekit-tutorials.openvidu.io/tutorials/application-server/php/index.md)

[**.NET**](https://livekit-tutorials.openvidu.io/tutorials/application-server/dotnet/index.md)

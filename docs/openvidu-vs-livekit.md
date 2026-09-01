---
title: "OpenVidu vs LiveKit for local development"
description: "Compare OpenVidu and LiveKit for local development: HTTPS on your LAN, bundled Egress and S3 storage, and testing a WebRTC app from real devices."
---

# Running OpenVidu vs LiveKit locally

If you want to run the tutorials on this site locally without the need to create an account on [LiveKit Cloud :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.livekit.io/){:target="_blank"}, we recommend **running OpenVidu locally**. OpenVidu is 100% compatible with LiveKit, and it offers many **advantages** for local development:

- Egress and Ingress services already integrated with a Redis instance. [See more](#egress-and-ingress-out-of-the-box).
- S3 compatible storage for Egress recordings. [See more](#s3-compatible-storage).
- Administration dashboard to monitor your Rooms. [See more](#administration-dashboard).
- OpenVidu Call: a ready-to-use app. [See more](#openvidu-call).
- Access your application from any device in your local network. [See more](#accessing-your-app-from-other-devices-in-your-network).

Whenever you are ready to deploy your real-time application, OpenVidu for production brings awesome features. Visit [What is OpenVidu?](./about-openvidu.md) to learn more.

=== "Run OpenVidu locally"

	--8<-- "tutorials/run-openvidu-locally.md"

## Egress and Ingress out of the box

LiveKit allows you to export media from a Room (for example recording it) or import media into a Room (for example ingesting a video file), using [Egress :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/reference/egress/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=comparison-page){:target="_blank"} and [Ingress :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/reference/ingress/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=comparison-page){:target="_blank"} services respectively. These modules are independent of LiveKit Server and must be correctly configured and connected via a shared Redis.

When running OpenVidu locally you will have all these services properly integrated, so you can focus on developing your app without worrying about anything else.

## S3 compatible storage

If you are planning to make use of the [Egress :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/reference/egress/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=comparison-page){:target="_blank"} service to export media out of your Rooms, you will need an S3 compatible bucket to store the generated files, and configure your LiveKit deployment to use it.

When running OpenVidu locally you will have an S3 compatible storage available right away ([MinIO :fontawesome-solid-external-link:{.external-link-icon}](https://www.min.io/){:target="_blank"}).

## Administration dashboard

OpenVidu comes with an administration dashboard that allows you to monitor the status of your Rooms. Not only in real time, but also historically: the number of participants, the number of published tracks, Egress and Ingress processes... This is a great tool to have when developing your app, as it can help spotting issues and debugging your application's logic.

## OpenVidu Call

When running OpenVidu locally a default application will be available for you to try. We have named this application **OpenVidu Call**, and it gathers the most important features that advanced videonconference apps would require: camera selection, screen sharing, virtual backgrounds, chat, recording...

You can use OpenVidu Call to help develop your own application, joining participants to shared rooms between your app and OpenVidu Call, and seeing how your app behaves.

## Accessing your app from other devices in your network

Testing WebRTC applications can be challenging because devices require a secure context (HTTPS) to access the camera and microphone. When using LiveKit Open Source, this isn't an issue if you access your app from the same computer where the LiveKit Server is running, as `localhost` is considered a secure context even over plain HTTP. Consider the following architecture:

![Architecture of a LiveKit application: the application client and application server both talk to LiveKit Server, using the client and server SDKs](./assets/images/livekit-architecture.svg){ .round-corners width="450" }

The simplest way to test your application is:

1. Run LiveKit Server on your computer.
2. Connect your app to LiveKit Server through `localhost`.
3. Serve both your application client and server from the same computer.
4. Access your app from `localhost` in a browser on the same computer.

This setup is straightforward, but what if you need to test your app from multiple devices simultaneously, including real mobile devices? In this case, you must use a secure context (HTTPS), which introduces two challenges:

1. LiveKit Server open source does not natively support HTTPS. You'll need a reverse proxy to serve LiveKit Server over HTTPS.
2. Even with HTTPS, your SSL certificate might not be valid for local network addresses. You'll need to accept it in the browser for web apps, and install it on mobile devices.

[OpenVidu Local Deployment :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/self-hosting/local/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=comparison-page){:target="_blank"} addresses these issues by providing a magic domain name `openvidu-local.dev` that resolves to any IP specified as a subdomain and provides a valid wildcard certificate for HTTPS. This is similar to services like [nip.io :fontawesome-solid-external-link:{.external-link-icon}](https://nip.io){:target="_blank"}, [traefik.me :fontawesome-solid-external-link:{.external-link-icon}](https://traefik.me){:target="_blank"}, or [localtls :fontawesome-solid-external-link:{.external-link-icon}](https://github.com/Corollarium/localtls){:target="_blank"}.

When using OpenVidu Local Deployment, you can access OpenVidu Server (which is 100% LiveKit compatible) and your app from any device on your local network with a valid HTTPS certificate. The following table shows the URLs to access the deployment and your application locally and from other devices on your network:

|                                   | Local access                                                   | Access from devices in your local network                                                                                      |
| --------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Usage                             | Access only from the development machine                       | Access from any device connected to your local network. In the URLs below, replace **`xxx-yyy-zzz-www`{.nowrap}** with the local IP address of the development machine, replacing the dots (`.`) with dashes (`-`). You can find the configured local IP in the **`.env`** file in the **`LAN_PRIVATE_IP`** variable |
| Application Client (frontend)     | [http://localhost:5080](http://localhost:5080)                 | `https://xxx-yyy-zzz-www.openvidu-local.dev:5443`                            |
| Application Server (backend)      | [http://localhost:6080](http://localhost:6080)                 | `https://xxx-yyy-zzz-www.openvidu-local.dev:6443`                            |
| OpenVidu (LiveKit Compatible) URL | [http://localhost:7880](http://localhost:7880)                 | `https://xxx-yyy-zzz-www.openvidu-local.dev:7443`                            |

!!! info
    
    - If you are developing locally, use `localhost` to access the services, but if you want to test your application from other devices on your network, use the `openvidu-local.dev` URLs.
    - Replace `xxx-yyy-zzz-www` with your local IP address. You can find it in the `.env` file in the `LAN_PRIVATE_IP` variable.

!!! warning
    
    If the URL isn't working because the IP address is incorrect or the installation script couldn't detect it automatically, you can update the `LAN_PRIVATE_IP` value in the `.env` file and restart the deployment with `docker compose up`.


When developing web applications with this deployment, you can use the following code snippet to dynamically determine the appropriate URLs for the application server and the LiveKit server based on the browser's current location. This approach allows you to seamlessly run your application on both your development machine and other devices within your local network without needing to manually adjust the URLs in your code.

```javascript
if (window.location.hostname === "localhost") {
  APPLICATION_SERVER_URL = "http://localhost:6080";
  LIVEKIT_URL = "ws://localhost:7880";
} else {
  APPLICATION_SERVER_URL = "https://" + window.location.hostname + ":6443";
  LIVEKIT_URL = "wss://" + window.location.hostname + ":7443";
}
```

### About `openvidu-local.dev` domain and SSL certificates

This setup simplifies the configuration of local OpenVidu deployments with SSL, making it easier to develop and test your applications securely on your local network by using the `openvidu-local.dev` domain and a wildcard SSL certificate valid for `*.openvidu-local.dev`. However, it’s important to note that these certificates are publicly available and do not provide an SSL certificate for production use.

The HTTPS offered by `openvidu-local.dev` is intended for development or testing purposes with the only goal of making your local devices trust your application (which is mandatory in WebRTC applications). For any other use case, it should be treated with the same security considerations as plain HTTP.

For production deployments, you should follow the [official OpenVidu installation guide :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/self-hosting/deployment-types/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=comparison-page){:target="_blank"}.

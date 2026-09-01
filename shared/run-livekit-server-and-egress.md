You can run [LiveKit :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/self-hosting/local/){:target="_blank"} and [Egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/self-hosting/egress/){:target="_blank"} locally or you can use their free tier of [LiveKit Cloud :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.livekit.io/){:target="_blank"}, which already includes both services.

Alternatively, you can use OpenVidu, which is a fully compatible LiveKit distribution designed specifically for on-premises environments. It brings notable improvements in terms of performance, observability and development experience. For more information, visit [What is OpenVidu?](../../about-openvidu.md){:target="_blank"}.

=== "Run OpenVidu locally"

    --8<-- "shared/run-openvidu-locally.md"

=== "Deploy OpenVidu"

    To use a production-ready OpenVidu deployment, visit the official [OpenVidu deployment guide :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/self-hosting/deployment-types/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=deploy-step){:target="_blank"}.

    !!! info "Configure Webhooks"

        This tutorial have an endpoint to receive webhooks from LiveKit. For this reason, when using a production deployment you need to configure webhooks to point to your local application server in order to make it work. Check the [Send Webhooks to a Local Application Server :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/self-hosting/how-to-guides/enable-webhooks/?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=deploy-step#send-webhooks-to-a-local-application-server){:target="_blank"} section for more information.

=== "Run LiveKit locally"

    Follow the official instructions to run [LiveKit :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/self-hosting/local/){:target="_blank"} and [Egress :fontawesome-solid-external-link:{.external-link-icon}](https://docs.livekit.io/transport/self-hosting/egress/){:target="_blank"} locally.

    !!! info "Configure Webhooks"

        This tutorial have an endpoint to receive webhooks from LiveKit. For this reason, when using LiveKit locally you need to configure webhooks to point to your application server in order to make it work. Check the [Webhooks :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/reference/webhooks/){:target="_blank"} section from the official documentation and follow the instructions to configure webhooks.

=== "Use LiveKit Cloud"

    Use your account in [LiveKit Cloud :fontawesome-solid-external-link:{.external-link-icon}](https://cloud.livekit.io/){:target="_blank"}.

    !!! info "Configure Webhooks"

        This tutorial have an endpoint to receive webhooks from LiveKit. For this reason, when using LiveKit Cloud you need to configure webhooks to point to your local application server in order to make it work. Check the [Webhooks :fontawesome-solid-external-link:{.external-link-icon}](https://openvidu.io/latest/docs/reference/webhooks/){:target="_blank"} section from the official documentation and follow the instructions to configure webhooks.

    !!! warning "Expose your local application server"

        In order to receive webhooks from LiveKit Cloud on your local machine, you need to expose your local application server to the internet. Tools like [Ngrok :fontawesome-solid-external-link:{.external-link-icon}](https://ngrok.com/){:target="_blank"}, [LocalTunnel :fontawesome-solid-external-link:{.external-link-icon}](https://localtunnel.github.io/www/){:target="_blank"}, [LocalXpose :fontawesome-solid-external-link:{.external-link-icon}](https://localxpose.io/){:target="_blank"} and [Zrok :fontawesome-solid-external-link:{.external-link-icon}](https://zrok.io/){:target="_blank"} can help you achieve this. 
        
        These tools provide you with a public URL that forwards requests to your local application server. You can use this URL to receive webhooks from LiveKit Cloud, configuring it as indicated above.

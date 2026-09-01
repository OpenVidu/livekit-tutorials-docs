# Keep these pins in step with openvidu.io's (publish-tool/pyproject.toml and its
# Dockerfile): the two sites publish the same tutorials, so they must render them
# with the same theme and extensions.
FROM squidfunk/mkdocs-material:9.7.6
RUN pip install mkdocs==1.6.1 pymdown-extensions==11.0.1 pygments==2.19.2 mkdocs-glightbox==0.5.2 mkdocs-llmstxt==0.5.0
ENTRYPOINT ["/sbin/tini", "--", "mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000", "--livereload", "--dirty"]

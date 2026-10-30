# Keep these pins in step with openvidu.io's (publish-tool/pyproject.toml and its
# Dockerfile): the two sites publish the same tutorials, so they must render them
# with the same theme and extensions.
FROM squidfunk/mkdocs-material:9.8.0
RUN pip install mkdocs==1.6.1 pymdown-extensions==12.3 pygments==2.21.0 mkdocs-glightbox==0.5.3 mkdocs-llmstxt==0.5.1
ENTRYPOINT ["/sbin/tini", "--", "mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000", "--livereload", "--dirty"]

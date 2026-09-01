# Keep these pins in step with openvidu.io's (publish-tool/pyproject.toml and its
# Dockerfile): the two sites publish the same tutorials, so they must render them
# with the same theme and extensions.
FROM squidfunk/mkdocs-material:9.7.6
RUN pip install mkdocs==1.6.1 pymdown-extensions==11.0.1 mkdocs-glightbox==0.5.2

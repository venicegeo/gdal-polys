#!/bin/bash
docker run -it --rm \
	 -p 8787:8787 \
	 -v $('pwd'):/home \
	 -w /home \
	 venicegeo/beachfront:latest \
	 /bin/bash \


# ScalaTion Kernel Dockerfile

Docker is the easiest way to get up and running with Jupyter and ScalaTion
Kernel. When using a Docker container, the only dependency is Docker.
To get started, follow the instructions below.

## Step 1: Use the Default Machine

NOTE: Most users may be able to skip this step.

```
$ docker-machine stop default
$ docker-machine start default
$ docker-machine ls
$ eval "$(docker-machine env default)"
```

## Step 2: Build and Run Docker Image
```
$ docker build -t scalation_kernel .
$ docker run -it --rm -p 8888:8888 scalation_kernel
```

You should be able to access Jupyter with ScalaTion Kernel support using
the URL provided in the output. If you cannot access it using that 
link, then run `docker-machine ls` to identify the IP address of your
container (e.g., `tcp://IP:PORT`). Next, try the URL again, replacing
`localhost` with `IP`.

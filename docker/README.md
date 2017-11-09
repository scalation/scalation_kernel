
# ScalaTion Kernel Dockerfile

## Use the Default Machine
```
$ docker-machine stop default
$ docker-machine start default
$ docker-machine ls
$ eval "$(docker-machine env default)"
```

## Build and Run Docker Image
```
$ docker build -t scalation_kernel .
$ docker run -it --rm -p 8888:8888 scalation_kernel
```

You should be able to access Jupyter with ScalaTion Kernel support using
the URL provided in the output. If you cannot access it using it that 
link, then run `docker-machine ls` to identify the IP address of your
container (e.g., `tcp://IP:PORT`). Next, try the URL again, replacing
`localhost` with `IP`.

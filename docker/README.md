
# ScalaTion Kernel Dockerfile

```
$ docker-machine stop default
$ docker-machine start default
$ docker-machine ls
$ eval "$(docker-machine env default)"
$ docker build -t scalation_kernel .
$ docker run -t --rm -p 8888:8888 scalation_kernel
```


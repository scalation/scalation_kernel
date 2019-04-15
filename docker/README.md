# ScalaTion Kernel Dockerfile

[Docker](https://www.docker.com) is the easiest way to get up and running with 
Jupyter and ScalaTion Kernel. When using this project's Docker image to create
a container, the only dependency is Docker. The image includes all of the 
additional dependencies needed to run Jupyter with support for the ScalaTion
big data framework. 

To get started, follow the instructions below.

## Getting Started 

1. Verify that the the default machine exists and is running:

   ```
   $ docker-machine ls
   ```

   If the "default" machine does not exist, then consult Docker's documentation
   to create it. If the machine does exist but is not running, then start it:

   ```
   $ docker-machine start default
   ```

   On some systems, you may need to execute the following additional command
   to ensure the commands in the next step assume the default machine:

   ```
   $ eval "$(docker-machine env default)"
   ```
   
2. Get the latest copy of the Docker image using the following command:

   ```
   $ docker pull mepcotterell/scalation_kernel:latest
   ```

   Alternatively, you can build the Docker images using the provided [`Dockerfile`](Dockerfile):

   ```
   $ cd docker/scalation_kernel/v1.6
   $ docker build -t scalation_kernel .
   ```

   This process may take some time as the image is built from scratch. At the
   time of this writing, the total image size after building is a little under 
   1GB. Users may require more disk space than this during the actual build
   process.

3. Run the Docker image:

   ```   
   $ docker run -it --rm -p 8888:8888 scalation_kernel
   ```

4. To open Jupter, copy the URL provided in the output and replace the 'placeholder 
   IP' ('e87f137a781d or 127.0.0.1') with 'docker-machine IP' and try the URL in the browser.
   To know the docker-machine IP, run 'docker-machine ls' command and identify the IP 
   address of your docker-machine (e.g., 'tcp://IP:PORT').

5. Start using ScalaTion notebooks! Consult the 
   [User Guide](https://github.com/scalation/scalation_kernel/blob/master/USER.md)
   for information on how to use ScalaTion in your Jupyter notebooks using
   ScalaTion Kernel.


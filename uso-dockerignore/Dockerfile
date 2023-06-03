FROM openjdk:17
COPY HelloWorld.java /tmp
COPY librerias /tmp/
WORKDIR /tmp
RUN ["javac", "HelloWorld.java"]
ENTRYPOINT ["java","HelloWorld"]
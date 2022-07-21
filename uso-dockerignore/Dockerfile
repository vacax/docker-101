FROM openjdk:17
COPY HelloWorld.java /tmp
WORKDIR /tmp
RUN ["javac", "HelloWorld.java"]
ENTRYPOINT ["java","HelloWorld"]
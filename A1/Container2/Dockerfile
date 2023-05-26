FROM openjdk
EXPOSE 6001
ADD target/container2.jar container2.jar
ENTRYPOINT ["java", "-jar","container2.jar", "--server.port=6001"]
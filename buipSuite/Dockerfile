FROM openjdk:11-jre-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y wget

# Download Burp Suite (Community Edition in this case)
RUN wget https://portswigger.net/burp/releases/download?product=community&version=2023.10.1&type=Linux --output-document=burpsuite_community.jar

# Expose the default Burp Suite port
EXPOSE 8080

# Set the entry point to run Burp Suite
ENTRYPOINT ["java", "-jar", "burpsuite_community.jar"]

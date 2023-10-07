sudo apt-get purge openjdk* -y
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update -y
sudo apt install openjdk-8-jre-headless -y
sudo apt-get install openjdk-8-jdk -y

# 设置JAVA_HOME
cat >> ~/.bashrc  << EOF

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

export PATH=\$PATH:\$JAVA_HOME/bin

EOF

source ~/.bashrc

sudo apt-get -y install maven

# 检测 Java 和 mvn 版本
java -version
javac -version
mvn --version

FROM kalilinux/kali

RUN apt-get update && \
    apt-get install -y python \
            metasploit-framework

RUN git clone https://github.com/grafov/hulk.git && \
    git clone https://github.com/entynetproject/quack.git && \
        cd quack && \
        chmod +x install.sh && \
        ./install.sh

CMD ["/bin/bash"]
# CMD ["python", "hulk/hulk.py", "$VICTIM"]
# CMD ["quack --tool HTTP --target http://victim --timeout 10 --threads 10"]"]
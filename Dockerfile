FROM golang:latest

WORKDIR /app

COPY . .

RUN go mod download

RUN go get github.com/cosmtrek/air
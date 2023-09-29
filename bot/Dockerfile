FROM golang:1.21

WORKDIR /linebot

COPY ./ ./

# RUN go mod tidy
RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -o /go-linebot

EXPOSE 8080

CMD ["/go-linebot"]
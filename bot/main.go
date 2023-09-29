package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/line/line-bot-sdk-go/v7/linebot"
)

func main() {
	bot, err := linebot.New("9ec5ac50f1f41274f7dfb9bd90713d33", "/wYYsAGUddNpoR4pUb5QvHw3iLR8OoRo4L+7CAck7S6rovJwlyP1kRQGfct69fQd8d+ewr2u8llcLuPY4+zPPImxs90Cp4appITyyWcc9MNMX2j0hJ0XRsbF01IOInrwk8BCk3dH+ue8YaOLkdsWGwdB04t89/1O/w1cDnyilFU=")
	if err != nil {
		log.Fatal(err)
	}
	http.HandleFunc("/test", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "This is a healthy handler!")
	})

	http.HandleFunc("/callback", func(w http.ResponseWriter, r *http.Request) {
		events, err := bot.ParseRequest(r)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Println(r)
		for _, event := range events {
			if event.Type == linebot.EventTypeMessage {
				fmt.Println("get message")
			}
		}
	})

	http.ListenAndServe(":8080", nil)
}

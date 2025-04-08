package com.example.apipogoda2;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.effect.ImageInput;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.json.HTTP;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class HelloApplication extends Application {
    public String klucz = " --> Tutaj wstaw klucz do API openweathermap <-- ";
    @Override
    public void start(Stage stage) throws IOException {
        VBox main = new VBox();
        GridPane inputPane = new GridPane();
        Label cityLabel = new Label("Nazwa miasta : ");
        TextField cityInput = new TextField();
        cityInput.setPrefWidth(560);
        Button getWeatherButton = new Button("🔍");
        Button closeAppButton = new Button("❌");
        TextArea output = new TextArea(". . .");
        output.setEditable(false);
        output.setPrefHeight(350);
        GridPane icon = new GridPane();
        icon.setStyle("-fx-background-color: #269ac7;");

        getWeatherButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                String urlString = "https://api.openweathermap.org/data/2.5/weather?q=" + cityInput.getText() + "&units=metric&appid="+klucz+"&lang=pl";
                String jsonString = null;
                System.out.println(urlString);

                HttpURLConnection connection = null;
                BufferedReader reader = null;
                try {
                    URL url = new URL(urlString);
                    connection = (HttpURLConnection) url.openConnection();
                    connection.connect();
                    InputStream stream = connection.getInputStream();
                    Scanner scan = new Scanner(stream).useDelimiter("\\A");
                    jsonString = scan.next();
                    scan.close();
                    connection.disconnect();
                } catch (Exception e) {
                    e.printStackTrace();
                }
                //icon.getChildren().clear();
                JSONObject jo = new JSONObject(jsonString);
                output.setText("Pogoda : " + jo.getJSONArray("weather").getJSONObject(0).getString("description") + "\n");
                output.appendText("\"main\": {" + "\n");
                output.appendText("    \"temp\" : " + jo.getJSONObject("main").getDouble("temp") + ",\n");
                output.appendText("    \"feels_like\" : " + jo.getJSONObject("main").getDouble("feels_like") + ",\n");
                output.appendText("    \"temp_mix\" : " + jo.getJSONObject("main").getDouble("temp_min") + ",\n");
                output.appendText("    \"temp_max\" : " + jo.getJSONObject("main").getDouble("temp_max") + ",\n");
                output.appendText("    \"pressure\" : " + jo.getJSONObject("main").getInt("pressure") + ",\n");
                output.appendText("    \"humidity\" : " + jo.getJSONObject("main").getInt("humidity") + ",\n");
                output.appendText("    \"sea_level\" : " + jo.getJSONObject("main").getInt("sea_level") + ",\n");
                output.appendText("    \"grnd_level\" : " + jo.getJSONObject("main").getInt("grnd_level") + "\n");
                output.appendText("}" + "\n");
                output.appendText("Widoczność : "+jo.getInt("visibility")/100.00+"%\n");
                output.appendText("Prędkość wiatru : "+jo.getJSONObject("wind").getDouble("speed")+"m/s\n");
                if(!jo.isNull("rain")){
                    output.appendText("Deszcz : "+jo.getJSONObject("rain").getDouble("1h")+"mm\n");
                } else {
                    output.appendText("Brak deszczu. \n");
                }
                if(!jo.isNull("snow")){
                    output.appendText("Śnieg : "+jo.getJSONObject("snow").getDouble("1h")+"mm\n");
                } else {
                    output.appendText("Brak śniegu. \n");
                }
                output.appendText("Zachmurzenie : "+jo.getJSONObject("clouds").getInt("all")+"%\n");
                output.appendText("Nazwa : "+jo.getString("name")+"\n");
                //output.setText(jo.getJSONObject("main").getBigDecimal("temp").toString());
                icon.getChildren().clear();
                switch (jo.getJSONArray("weather").getJSONObject(0).getString("icon")){
                    case "01d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\01d@2x.png")), 0,0);
                        break;
                    case "02d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\02d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "03d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\03d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "04d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\04d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "09d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\09d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "10d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\10d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "11d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\11d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "13d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\13d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "50d":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\50d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "01n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\01n@2x.png")), 0,0);
                        break;
                    case "02n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\02n@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "03n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\03d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "04n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\04d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "09n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\09d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "10n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\10n@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "11n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\11d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "13n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\13d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "50n":
                        icon.add(new ImageView(new Image("E:\\,ZSEL\\3TP\\Aplikacje Desktopowe\\ApiPogoda\\ApiPogoda2\\ApiPogoda2\\icons\\50d@2x.png", 50, 50, true, false)), 0,0);
                        break;
                    case "x":
                        icon.add(new Label("❌"), 0,0);
                        break;
                    default:
                }
            }
        });

        closeAppButton.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                System.exit(0);
            }
        });

        inputPane.add(cityLabel, 0,0);
        inputPane.add(cityInput, 1,0);
        inputPane.add(getWeatherButton, 3,0);
        inputPane.add(closeAppButton, 4,0);
        main.getChildren().addAll(inputPane, output, icon);
        Scene scene = new Scene(main, 700, 450);
        stage.setTitle("Pogodynka");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
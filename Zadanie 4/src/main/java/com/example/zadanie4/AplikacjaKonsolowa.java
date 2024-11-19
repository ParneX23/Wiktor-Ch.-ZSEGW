package com.example.zadanie4;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Random;

public class AplikacjaKonsolowa extends Application {

    // Stałe wartości

    private final int minIloscOczek = 1;
    private final int maxIloscOczek = 6;
    private final int minIloscDoZliczenia = 2;
    private final int minIloscKosci = 3;
    private final int maxIloscKosci = 10;
    private final int minWynik = 3;
    private final int maxWynik = 10;

    // Zmienne

    private int liczbaLosowan = 0;

    // Funkcja odpowiedzialna za losowanie kości

    public int[] rzut(int ilosc) {
        int[] kosci = new int[ilosc];
        for(int i = 0; i < ilosc; i++){
            kosci[i] = new Random().nextInt(minIloscOczek, maxIloscOczek);
        }
        return kosci;
    }

    // Funkcja odpowiedzialna za liczenie wyniku

    public int licz(int[] kosci) {
        int punkty = 0;
        for(int i = minIloscOczek; i <= maxIloscOczek ; i++){
            int razy = 0;
            for(int j = 0; j < kosci.length; j++) if(kosci[j] == i) razy++;
            if(razy >= minIloscDoZliczenia) punkty += i*razy;
        }
        return punkty;
    }

    @Override
    public void start(Stage stage) throws IOException {

        // Panel przycisków

        GridPane sterowanie = new GridPane();
        sterowanie.setPadding(new Insets(10,10,10,10));
        sterowanie.setVgap(5);
        sterowanie.setHgap(5);

        Label iloscLabel = new Label("Podaj ilość rzucanych kości");
        TextField iloscKosci = new TextField();
        Button losuj = new Button("losuj");
        Button resetuj = new Button("resetuj");
        Label wynikLabel = new Label("Łączny wynik : ");
        Label wynik = new Label("0");

        sterowanie.add(iloscLabel, 0,0);
        sterowanie.add(iloscKosci,1,0);
        sterowanie.add(losuj,0,1);
        sterowanie.add(resetuj,1,1);
        sterowanie.add(wynikLabel, 0, 2);
        sterowanie.add(wynik, 1, 2);

        // Panel kości
        ScrollPane scrollPane = new ScrollPane();
        scrollPane.setPrefSize(300,200);
        GridPane kosci = new GridPane();
        kosci.setPadding(new Insets(10,10,10,10));
        kosci.setVgap(5);
        kosci.setHgap(5);

        scrollPane.setContent(kosci);

        // Panel główny

        GridPane main = new GridPane();
        main.setPadding(new Insets(10,10,10,10));
        main.setMinSize(500, 300);
        main.setAlignment(Pos.TOP_CENTER);
        main.setVgap(5);
        main.setHgap(5);

        main.add(sterowanie, 0, 0);
        main.add(scrollPane, 0,1);

        // Funkcjonalność przycisku losuj

        losuj.setOnMouseClicked((new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                //kosci.getChildren().clear();
                if(Integer.parseInt(iloscKosci.getText()) >= minIloscKosci && Integer.parseInt(iloscKosci.getText()) <= maxIloscKosci){
                    int[] wylosowane = rzut(Integer.parseInt(iloscKosci.getText()));
                    liczbaLosowan++;
                    for(int i = 0; i <= wylosowane.length; i++){
                        if(i == wylosowane.length){
                            kosci.add(new Label(String.valueOf(licz(wylosowane))), 0+i, 0+liczbaLosowan);
                        } else {
                            try {
                                kosci.add(new ImageView(new Image(new FileInputStream(String.valueOf(wylosowane[i])+".png"), 20, 20, true, false )),0+i,0+liczbaLosowan);
                            } catch (FileNotFoundException e) {
                                throw new RuntimeException(e);
                            }
                        }
                    }

                    wynik.setText(String.valueOf(Integer.valueOf(wynik.getText())+licz(wylosowane)));
                    if(licz(wylosowane) >= minWynik && licz(wylosowane) <= maxWynik) {
                        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
                        alert.setTitle("Dobry wynik");
                        alert.setHeaderText("Udało ci się wylosować sumę oczek \n z przedziału od "+minWynik+" do "+maxWynik+"!\n Chcesz zakończyć działanie programu?");
                        ((Button) alert.getDialogPane().lookupButton(ButtonType.OK)).setText("Zakończ");
                        ((Button) alert.getDialogPane().lookupButton(ButtonType.OK)).setOnAction(new EventHandler<ActionEvent>() {
                            @Override
                            public void handle(ActionEvent actionEvent) {
                                Platform.exit();
                            }
                        });
                        ((Button) alert.getDialogPane().lookupButton(ButtonType.CANCEL)).setText("Wróć");
                        alert.show();
                    }
                } else if(Integer.parseInt(iloscKosci.getText()) < minIloscKosci) {
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("Błąd!");
                    alert.setHeaderText("Minimalna ilość kości do rzucenia musi wynosić co najmniej "+minIloscKosci);
                    alert.show();
                } else {
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("Błąd!");
                    alert.setHeaderText("Maxymalna ilość kości do rzucenia nie może przekraczać "+maxIloscKosci);
                    alert.show();
                }
            }
        }));

        resetuj.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                liczbaLosowan = 0;
                wynik.setText("0");
                kosci.getChildren().clear();
            }
        });

        // Scena 

        Scene scene = new Scene(main, 350, 300);
        stage.setTitle("Kości");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
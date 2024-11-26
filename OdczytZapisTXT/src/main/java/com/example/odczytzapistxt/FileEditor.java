package com.example.odczytzapistxt;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;

/*
public static void main(String[] args) {
    String fileRead = "example.txt";
    String fileToWrite = "output.txt";

    try {
        System.out.println("Odczyt pliku: " + fileRead);
        List<String> fileContent = readFile(fileRead);
        fileContent.forEach(System.out::println);

        fileContent.add("To jest nowa linia zapisana do pliku.");

        System.out.println("\nZapis do pliku: " + fileToWrite);
        writeFile(fileToWrite, fileContent);

        System.out.println("Dane zapisano pomyslnie do: " + fileToWrite);

    } catch (IOException e) {
        System.err.println("WystÄpiĹ bĹÄd podczas pracy z plikiem: " +e.getMessage());
    }
}
 */

public class FileEditor extends Application {
    public static List<String> readFile(String filePath) throws IOException {
        Path path = Paths.get(filePath);
        return Files.readAllLines(path);
    }

    public static void writeFile(String filePath, List<String> lines) throws IOException {
        Path path = Paths.get(filePath);
        Files.write(path, lines);
    }

    public void start(Stage stage) throws IOException {

        GridPane main = new GridPane();
        main.setPadding(new Insets(10, 10, 10, 10));
        main.setVgap(5);
        main.setHgap(5);
        main.setAlignment(Pos.TOP_LEFT);

        Label pathLabel = new Label("Ścieżka pliku : ");
        TextField pathInput = new TextField();
        GridPane pathPane = new GridPane();
        pathPane.add(pathLabel, 0,0);
        pathPane.add(pathInput, 1,0);

        TextArea ioField = new TextArea();

        ButtonBar buttons = new ButtonBar();
        Button save = new Button("Zapisz");
        Button load = new Button("Wczytaj");
        Button close = new Button("Zamknij");
        buttons.getButtons().addAll(save, load, close);

        GridPane newButtons = new GridPane();
        ImageView saveImage = new ImageView(new Image(new FileInputStream("save.png"), 50, 50, false, false));
        ImageView loadImage = new ImageView(new Image(new FileInputStream("load.png"), 50, 50, false, false));

        newButtons.add(saveImage, 0, 0);
        newButtons.add(loadImage, 1, 0);

        main.add(pathPane, 0, 0);
        main.add(ioField, 0, 1);
        main.add(buttons, 0, 2);
        main.add(newButtons, 0, 3);

        // działalność przycisków

        save.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                try {
                    writeFile(pathInput.getText(), Collections.singletonList(ioField.getText()));
                } catch (IOException e) {
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("Błąd");
                    alert.setHeaderText("Wystąpił błąd podczas pracy z plikiem : ");
                    alert.setContentText(e.getMessage());
                }
            }
        });

        load.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                ioField.clear();
                try {
                    List<String> fileContent = readFile(pathInput.getText());
                    for (int i = 0; i < fileContent.size(); i++) {
                        ioField.appendText(fileContent.get(i));
                        ioField.appendText("\n");
                    }
                } catch (IOException e) {
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("Błąd");
                    alert.setHeaderText("Wystąpił błąd podczas pracy z plikiem : ");
                    alert.setContentText(e.getMessage());
                }
            }
        });

        loadImage.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                ioField.clear();
                try {
                    List<String> fileContent = readFile(pathInput.getText());
                    for (int i = 0; i < fileContent.size(); i++) {
                        ioField.appendText(fileContent.get(i));
                        ioField.appendText("\n");
                    }
                } catch (IOException e) {
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("Błąd");
                    alert.setHeaderText("Wystąpił błąd podczas pracy z plikiem : ");
                    alert.setContentText(e.getMessage());
                }
            }
        });

        saveImage.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                try {
                    writeFile(pathInput.getText(), Collections.singletonList(ioField.getText()));
                } catch (IOException e) {
                    Alert alert = new Alert(Alert.AlertType.ERROR);
                    alert.setTitle("Błąd");
                    alert.setHeaderText("Wystąpił błąd podczas pracy z plikiem : ");
                    alert.setContentText(e.getMessage());
                }
            }
        });

        close.setOnMouseClicked(new EventHandler<MouseEvent>() {
            @Override
            public void handle(MouseEvent mouseEvent) {
                Platform.exit();
            }
        });

        Scene scene = new Scene(main, 320, 240);
        stage.setTitle("FileEditor");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}